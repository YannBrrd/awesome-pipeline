import argparse
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import yaml

# Dialects supported: databricks (unity), bigquery, snowflake, postgres

TypeMap = Dict[str, str]

TYPE_MAPS: Dict[str, TypeMap] = {
    "databricks": {
        "string": "STRING",
        "integer": "BIGINT",
        "number": "DOUBLE",
        "date": "DATE",
        "timestamp": "TIMESTAMP",
        "decimal": "DECIMAL",  # will append (p,s)
    },
    "bigquery": {
        "string": "STRING",
        "integer": "INT64",
        "number": "FLOAT64",
        "date": "DATE",
        "timestamp": "TIMESTAMP",
        "decimal": "NUMERIC",
    },
    "snowflake": {
        "string": "VARCHAR",
        "integer": "NUMBER(38,0)",
        "number": "DOUBLE",
        "date": "DATE",
        "timestamp": "TIMESTAMP_NTZ",
        "decimal": "NUMBER",
    },
    "postgres": {
        "string": "TEXT",
        "integer": "BIGINT",
        "number": "DOUBLE PRECISION",
        "date": "DATE",
        "timestamp": "TIMESTAMP",
        "decimal": "DECIMAL",
    },
}


def parse_decimal(t: str) -> Tuple[str, str | None]:
    base = t.split("(")[0].strip()
    if base.startswith("decimal") or base.startswith("DECIMAL"):
        inside = None
        if "(" in t and ")" in t:
            inside = t[t.find("(") + 1 : t.find(")")]
        return "decimal", inside
    return base, None


def map_type(dialect: str, t: str) -> str:
    base, inside = parse_decimal(t)
    m = TYPE_MAPS[dialect]
    if base == "decimal":
        typ = m["decimal"]
        return f"{typ}({inside or '10,2'})"
    return m.get(base, m["string"])  # default to string


def topo_sort_tables(schemas: Dict[str, Any]) -> List[str]:
    deps: Dict[str, Set[str]] = {t: set() for t in schemas.keys()}
    rdeps: Dict[str, Set[str]] = {t: set() for t in schemas.keys()}
    for tname, tspec in schemas.items():
        for fk in tspec.get("foreign_keys", []):
            ref = fk.get("ref_table")
            if ref and ref in deps and ref != tname:
                deps[tname].add(ref)
                rdeps[ref].add(tname)
    no_incoming = [t for t, d in deps.items() if not d]
    ordered: List[str] = []
    while no_incoming:
        n = no_incoming.pop()
        ordered.append(n)
        for m in list(rdeps[n]):
            deps[m].discard(n)
            rdeps[n].discard(m)
            if not deps[m]:
                no_incoming.append(m)
    remaining = [t for t, d in deps.items() if d]
    return ordered + remaining


def fq_table_name(dialect: str, catalog: str | None, schema: str | None, table: str) -> str:
    if dialect == "bigquery":
        # project.dataset.table or dataset.table; we'll emit dataset.table for simplicity
        if schema:
            return f"{schema}.{table}"
        return table
    if dialect == "databricks":
        # Unity Catalog: catalog.schema.table when provided
        if catalog and schema:
            return f"{catalog}.{schema}.{table}"
        if schema:
            return f"{schema}.{table}"
        return table
    # snowflake and postgres: schema.table
    if schema:
        return f"{schema}.{table}"
    return table


def emit_preamble(dialect: str, catalog: str | None, schema: str | None) -> str:
    stmts: List[str] = []
    if dialect == "databricks":
        if catalog:
            stmts.append(f"CREATE CATALOG IF NOT EXISTS {catalog};")
            stmts.append(f"USE CATALOG {catalog};")
        if schema:
            stmts.append(f"CREATE SCHEMA IF NOT EXISTS {schema};")
            stmts.append(f"USE SCHEMA {schema};")
    elif dialect == "bigquery":
        if schema:
            stmts.append(f"CREATE SCHEMA IF NOT EXISTS `{schema}`;")
    elif dialect == "snowflake":
        if schema:
            stmts.append(f"CREATE SCHEMA IF NOT EXISTS {schema};")
            stmts.append(f"USE SCHEMA {schema};")
    elif dialect == "postgres":
        if schema:
            stmts.append(f"CREATE SCHEMA IF NOT EXISTS {schema};")
            stmts.append(f"SET search_path TO {schema};")
    return "\n".join(stmts) + ("\n\n" if stmts else "")


def generate_create_table(dialect: str, catalog: str | None, schema: str | None, tname: str, tspec: Dict[str, Any]) -> str:
    cols = []
    for fname, fs in tspec.get("fields", {}).items():
        col = f'  "{fname}" {map_type(dialect, fs.get("type", "string"))}'
        cols.append(col)
    pk = tspec.get("primary_key", [])
    constraints: List[str] = []
    if pk and dialect in ("postgres", "snowflake", "databricks"):
        constraints.append(f"  PRIMARY KEY ({', '.join(f'\"{c}\"' for c in pk)})")
    # BigQuery does not support PK/FK constraints; skip
    if dialect in ("postgres", "snowflake"):
        for fk in tspec.get("foreign_keys", []):
            field = fk.get("field")
            ref_table = fk.get("ref_table")
            ref_field = fk.get("ref_field")
            constraints.append(
                f'  FOREIGN KEY ("{field}") REFERENCES {fq_table_name(dialect, None, schema, ref_table)} ("{ref_field}")'
            )
    # Databricks/Spark constraints are informational; include PK only, omit FKs by default
    all_lines = cols + constraints
    table_full = fq_table_name(dialect, catalog, schema, tname)
    return f"CREATE TABLE IF NOT EXISTS {table_full} (\n" + ",\n".join(all_lines) + "\n);\n"


def main():
    ap = argparse.ArgumentParser(description="Generate DDL from contract for multiple catalogs/warehouses")
    ap.add_argument("contract", nargs="?", default="1.Data_contract/olist_mini/contract.yaml")
    ap.add_argument("--dialect", choices=list(TYPE_MAPS.keys()), required=True)
    ap.add_argument("--catalog", help="Catalog/Project (Unity Catalog / optional)")
    ap.add_argument("--schema", help="Schema/Dataset (or BigQuery dataset)")
    ap.add_argument("--out", dest="out_dir", default="4.DDL_for_catalogs/ddl_multi", help="Output directory")
    args = ap.parse_args()

    contract_path = Path(args.contract)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    schemas: Dict[str, Any] = contract["schemas"]

    ordered = topo_sort_tables(schemas)

    # Write preamble and per-table files
    combined_parts: List[str] = []
    pre = emit_preamble(args.dialect, args.catalog, args.schema)
    if pre.strip():
        combined_parts.append(pre)
    for t in ordered:
        sql = generate_create_table(args.dialect, args.catalog, args.schema, t, schemas[t])
        (out_dir / f"create_{t}_{args.dialect}.sql").write_text(sql, encoding="utf-8")
        combined_parts.append(sql)

    (out_dir / f"create_all_{args.dialect}.sql").write_text("\n".join(combined_parts), encoding="utf-8")
    print(f"Generated {args.dialect} DDL in {out_dir}")


if __name__ == "__main__":
    main()
