import os
import json
from pathlib import Path
from typing import Dict, Any

import yaml

# Generates basic expectation suites per table from the contract into 5.GX_code/expectations

SUITE_TMPL = {
    "data_asset_type": None,
    "expectation_suite_name": "",
    "ge_cloud_id": None,
    "expectations": [],
    "meta": {"notes": "Auto-generated from contract.yaml"}
}

MOSTLY = float(os.environ.get("GX_MOSTLY", "0.99"))


def suite_for_table(tname: str, tspec: Dict[str, Any]):
    exps = []
    fields: Dict[str, Any] = tspec.get("fields", {})
    for fname, fs in fields.items():
        if fs.get("enum"):
            exps.append({
                "expectation_type": "expect_column_values_to_be_in_set",
                "kwargs": {"column": fname, "value_set": fs["enum"], "mostly": MOSTLY}
            })
        if fs.get("pattern"):
            exps.append({
                "expectation_type": "expect_column_values_to_match_regex",
                "kwargs": {"column": fname, "regex": fs["pattern"], "mostly": MOSTLY}
            })
        if fs.get("min") is not None:
            exps.append({
                "expectation_type": "expect_column_min_to_be_between",
                "kwargs": {"column": fname, "min_value": fs["min"]}
            })
    for exp in tspec.get("expectations", []):
        if "not_null" in exp:
            for col in exp["not_null"]:
                exps.append({
                    "expectation_type": "expect_column_values_to_not_be_null",
                    "kwargs": {"column": col, "mostly": MOSTLY}
                })
        if "unique" in exp:
            cols = exp["unique"]
            if isinstance(cols, list) and len(cols) == 1:
                exps.append({
                    "expectation_type": "expect_column_values_to_be_unique",
                    "kwargs": {"column": cols[0]}
                })
            else:
                exps.append({
                    "expectation_type": "expect_compound_columns_to_be_unique",
                    "kwargs": {"column_list": cols}
                })
    suite = SUITE_TMPL.copy()
    suite["expectation_suite_name"] = f"{tname}.suite"
    suite["expectations"] = exps
    return suite


def main():
    contract_path = Path("1.Data_contract/olist_mini/contract.yaml")
    out_dir = Path("5.GX_code/expectations")
    out_dir.mkdir(parents=True, exist_ok=True)
    contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    for tname, tspec in contract["schemas"].items():
        suite = suite_for_table(tname, tspec)
        (out_dir / f"{tname}.json").write_text(json.dumps(suite, indent=2), encoding="utf-8")
    print(f"Generated suites in {out_dir} with mostly={MOSTLY}")


if __name__ == "__main__":
    main()
