from pathlib import Path
from typing import Dict, Any, List, Set

import yaml

SQL_TYPES = {
    "string": "TEXT",
    "integer": "BIGINT",
    "number": "DOUBLE PRECISION",
    "date": "DATE",
    "timestamp": "TIMESTAMP",
}


def map_type(t: str) -> str:
    base = t.split("(")[0].strip()
    if base.startswith("decimal"):
        inside = t[t.find("(")+1:t.find(")")] if "(" in t and ")" in t else "10,2"
        return f"DECIMAL({inside})"
    return SQL_TYPES.get(base, "TEXT")


def generate_create_table(tname: str, tspec: Dict[str, Any]) -> str:
    cols = []
    for fname, fs in tspec.get("fields", {}).items():
        col = f'  "{fname}" {map_type(fs.get("type", "string"))}'
        cols.append(col)
    pk = tspec.get("primary_key", [])
    constraints: List[str] = []
    if pk:
        constraints.append(f"  PRIMARY KEY ({', '.join(f'\"{c}\"' for c in pk)})")
    for i, fk in enumerate(tspec.get("foreign_keys", []), start=1):
        field = fk.get("field")
        ref_table = fk.get("ref_table")
        ref_field = fk.get("ref_field")
        cname = f"fk_{tname}_{field}_{ref_table}_{ref_field}"[:60]
        constraints.append(
            f'  CONSTRAINT "{cname}" FOREIGN KEY ("{field}") REFERENCES {ref_table} ("{ref_field}")'
        )
    all_lines = cols + constraints
    return f"CREATE TABLE IF NOT EXISTS {tname} (\n" + ",\n".join(all_lines) + "\n);\n"


def topo_sort_tables(schemas: Dict[str, Any]) -> List[str]:
    # Kahn's algorithm
    deps: Dict[str, Set[str]] = {t: set() for t in schemas.keys()}
    rdeps: Dict[str, Set[str]] = {t: set() for t in schemas.keys()}  # reverse deps
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
    # append any remaining (cycle fallback)
    remaining = [t for t, d in deps.items() if d]
    return ordered + remaining


def main():
    contract_path = Path("1.Data_contract/olist_mini/contract.yaml")
    out_dir = Path("4.DDL_for_catalogs/ddl")
    out_dir.mkdir(parents=True, exist_ok=True)
    contract = yaml.safe_load(contract_path.read_text(encoding='utf-8'))
    schemas: Dict[str, Any] = contract["schemas"]

    # Per-table files
    for tname, tspec in schemas.items():
        sql = generate_create_table(tname, tspec)
        (out_dir / f"create_{tname}.sql").write_text(sql, encoding="utf-8")

    # Combined create_all.sql in dependency order
    ordered = topo_sort_tables(schemas)
    combined = "-- Auto-generated. Creation order respects foreign key dependencies.\n\n" + "\n".join(
        generate_create_table(t, schemas[t]) for t in ordered
    )
    (out_dir / "create_all.sql").write_text(combined, encoding="utf-8")
    print(f"Generated DDL in {out_dir} (including create_all.sql)")


if __name__ == "__main__":
    main()
