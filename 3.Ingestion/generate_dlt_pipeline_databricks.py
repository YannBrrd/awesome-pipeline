import re
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

TEMPLATE = """
# Auto-generated for Databricks from {contract_path}
import os
from pathlib import Path
import dlt
import pandas as pd

DATA_DIR = Path(os.environ.get("OLIST_DATA_DIR", "data/olist_mini")).resolve()
DESTINATION = "databricks"
DATASET = os.environ.get("DLT_DATASET", "raw_olist")
CHUNKSIZE = int(os.environ.get("INGEST_CHUNKSIZE", "50000"))

# Map common env names to Databricks SQL connector variables if missing
if os.environ.get("DATABRICKS_SERVER_HOSTNAME") is None and os.environ.get("DATABRICKS_HOST"):
    os.environ["DATABRICKS_SERVER_HOSTNAME"] = os.environ["DATABRICKS_HOST"]
if os.environ.get("DATABRICKS_ACCESS_TOKEN") is None and os.environ.get("DATABRICKS_TOKEN"):
    os.environ["DATABRICKS_ACCESS_TOKEN"] = os.environ["DATABRICKS_TOKEN"]

REQUIRED = ["DATABRICKS_SERVER_HOSTNAME", "DATABRICKS_HTTP_PATH", "DATABRICKS_ACCESS_TOKEN"]
missing = [k for k in REQUIRED if not os.environ.get(k)]
if missing:
    raise RuntimeError(f"Missing Databricks env vars: {missing}. Set them before running.")

# Simple expectations helpers derived from contract

def assert_not_null(df: pd.DataFrame, columns):
    mask = df[columns].isnull().any(axis=1)
    return df[~mask], df[mask]

def assert_unique(df: pd.DataFrame, columns):
    deduped = df.drop_duplicates(subset=columns, keep="first")
    rejected = df[~df.index.isin(deduped.index)]
    return deduped, rejected

def assert_min(df: pd.DataFrame, column: str, min_value: float):
    mask = pd.to_numeric(df[column], errors='coerce') < min_value
    return df[~mask], df[mask]


def assert_enum(df: pd.DataFrame, column: str, allowed):
    mask = ~df[column].isin(allowed)
    return df[~mask], df[mask]


def assert_pattern(df: pd.DataFrame, column: str, pattern: str):
    pat = re.compile(pattern)
    mask = ~df[column].fillna("").astype(str).str.match(pat)
    return df[~mask], df[mask]


def read_csv_chunks(path: Path):
    if not path.exists():
        return
    for chunk in pd.read_csv(path, dtype=str, keep_default_na=True, na_values=["", "null", "None"], chunksize=CHUNKSIZE):
        yield chunk


# Resources
{resources}

def run_all():
    pipeline = dlt.pipeline(pipeline_name="olist_mini", destination=DESTINATION, dataset_name=DATASET)
    total = pipeline.run([{calls}])
    print(total)

if __name__ == "__main__":
    run_all()
"""

RESOURCE_TMPL = """
@dlt.resource(name="{table}", write_disposition="merge", primary_key={pk})
def {table}_res():
    rejects_dir = Path("data/olist_mini/rejects")
    rejects_dir.mkdir(parents=True, exist_ok=True)
    csv_path = DATA_DIR / "{table}.csv"
    for chunk in read_csv_chunks(csv_path):
        df = chunk.copy()
        rejs = []
        # casts for numeric columns when we have min constraints
{casts}
        # not_null expectations
{not_null}
        # unique expectations
{unique}
        # min constraints
{mins}
        # enum constraints
{enums}
        # pattern constraints
{patterns}
        if rejs:
            pd.concat(rejs).to_csv(rejects_dir / "{table}_rejects.csv", mode="a", index=False)
        yield df.to_dict(orient="records")
"""


def snake(s: str) -> str:
    s = re.sub(r"[^0-9a-zA-Z_]+", "_", s)
    s = re.sub(r"_+", "_", s)
    return s.strip("_").lower()


def main(argv):
    if len(argv) < 2:
        print("Usage: python generate_dlt_pipeline_databricks.py <path-to-contract.yaml> [<out-py>]")
        return 2
    cpath = Path(argv[1]).resolve()
    out_py = Path(argv[2]).resolve() if len(argv) > 2 else Path(__file__).parent / "pipelines" / f"{cpath.stem}_databricks_pipeline.py"
    contract = yaml.safe_load(cpath.read_text(encoding="utf-8"))
    schemas: Dict[str, Any] = contract["schemas"]

    resources_code = []
    calls = []
    for tname, tspec in schemas.items():
        table = snake(tname)
        pk = tspec.get("primary_key", [])
        pk_py = repr(pk[0] if len(pk) == 1 else pk)
        fields = tspec.get("fields", {})
        expectations = tspec.get("expectations", [])

        casts, mins, not_null, unique, enums, patterns = [], [], [], [], [], []

        for fname, fs in fields.items():
            min_v = fs.get("min")
            typ = fs.get("type", "string")
            enum_vals = fs.get("enum")
            pattern = fs.get("pattern")
            if min_v is not None:
                casts.append(f"        df['{fname}'] = pd.to_numeric(df['{fname}'], errors='coerce')")
                mins.append(f"        df, r = assert_min(df, '{fname}', {float(min_v)})\n        rejs.append(r)")
            elif typ in ("integer", "number") or typ.startswith("decimal"):
                casts.append(f"        df['{fname}'] = pd.to_numeric(df['{fname}'], errors='ignore')")
            if enum_vals:
                enums.append(f"        df, r = assert_enum(df, '{fname}', {enum_vals})\n        rejs.append(r)")
            if pattern:
                patterns.append(f"        df, r = assert_pattern(df, '{fname}', r'{pattern}')\n        rejs.append(r)")

        for exp in expectations:
            if "not_null" in exp:
                cols = exp["not_null"]
                not_null.append(f"        df, r = assert_not_null(df, {cols})\n        rejs.append(r)")
            if "unique" in exp:
                cols = exp["unique"]
                unique.append(f"        df, r = assert_unique(df, {cols})\n        rejs.append(r)")

        res_code = RESOURCE_TMPL.format(
            table=table,
            pk=pk_py,
            casts="\n".join(casts) or "        # no numeric casts",
            mins="\n".join(mins) or "        # no min checks",
            not_null="\n".join(not_null) or "        # no not_null checks",
            unique="\n".join(unique) or "        # no unique checks",
            enums="\n".join(enums) or "        # no enum checks",
            patterns="\n".join(patterns) or "        # no pattern checks",
        )
        resources_code.append(res_code)
        calls.append(f"{table}_res()")

    final_py = TEMPLATE.format(
        contract_path=str(cpath),
        resources="\n".join(resources_code),
        calls=", \\n        ".join(calls)
    )
    out_py.write_text(final_py, encoding="utf-8")
    print(f"Generated: {out_py}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
