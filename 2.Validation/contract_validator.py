import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

import yaml
from pydantic import BaseModel, Field, model_validator


class FieldSpec(BaseModel):
    type: str
    required: bool = False
    enum: Optional[List[str]] = None
    min: Optional[float] = None
    max: Optional[float] = None
    # New: optional regex/pattern support
    pattern: Optional[str] = None


class ForeignKey(BaseModel):
    field: str
    ref_table: str
    ref_field: str


class TableSpec(BaseModel):
    description: Optional[str] = None
    primary_key: List[str]
    foreign_keys: List[ForeignKey] = Field(default_factory=list)
    fields: Dict[str, FieldSpec]
    expectations: List[Dict[str, Any]] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_keys_exist(self) -> "TableSpec":
        missing_pk = [k for k in self.primary_key if k not in self.fields]
        if missing_pk:
            raise ValueError(f"Primary key fields not in fields: {missing_pk}")
        for fk in self.foreign_keys:
            if fk.field not in self.fields:
                raise ValueError(f"Foreign key field '{fk.field}' not defined in fields")
        return self


class Contract(BaseModel):
    name: str
    version: str
    owner: Dict[str, Any]
    lifecycle: Dict[str, Any]
    refresh: Dict[str, Any]
    privacy: Dict[str, Any]
    schemas: Dict[str, TableSpec]
    checks: Optional[List[Dict[str, Any]]] = None

    @model_validator(mode="after")
    def validate_fk_refs(self) -> "Contract":
        for t_name, t in self.schemas.items():
            for fk in t.foreign_keys:
                if fk.ref_table not in self.schemas:
                    raise ValueError(f"FK in {t_name}.{fk.field} references unknown table '{fk.ref_table}'")
                ref = self.schemas[fk.ref_table]
                if fk.ref_field not in ref.fields:
                    raise ValueError(f"FK in {t_name}.{fk.field} references unknown field '{fk.ref_table}.{fk.ref_field}'")
        return self


def load_contract(path: Path) -> Contract:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Contract(**data)


def compile_json_schemas(contract: Contract) -> Dict[str, Dict[str, Any]]:
    """Produce simple JSON Schema per table for downstream generators."""
    type_map = {
        "string": {"type": "string"},
        "integer": {"type": "integer"},
        "number": {"type": "number"},
        "date": {"type": "string", "format": "date"},
        "timestamp": {"type": "string", "format": "date-time"},
    }
    compiled: Dict[str, Dict[str, Any]] = {}
    for t_name, t in contract.schemas.items():
        props: Dict[str, Any] = {}
        required: List[str] = []
        for fname, fs in t.fields.items():
            base_type = fs.type.split("(")[0].strip()
            schema = type_map.get(base_type, {"type": "string"})
            if fs.enum:
                schema = {"type": "string", "enum": fs.enum}
            if fs.pattern:
                schema["pattern"] = fs.pattern
            if fs.min is not None:
                schema["minimum"] = fs.min
            if fs.max is not None:
                schema["maximum"] = fs.max
            props[fname] = schema
            if fs.required:
                required.append(fname)
        compiled[t_name] = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": t_name,
            "type": "object",
            "properties": props,
            "required": required,
            "additionalProperties": True,
        }
    return compiled


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("Usage: python contract_validator.py <path-to-contract.yaml> [<out-dir>]")
        return 2
    contract_path = Path(argv[1]).resolve()
    out_dir = Path(argv[2]).resolve() if len(argv) > 2 else contract_path.parent / "_artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        contract = load_contract(contract_path)
    except Exception as e:
        print(f"Invalid contract: {e}")
        return 1

    compiled = compile_json_schemas(contract)
    (out_dir / "compiled.schemas.json").write_text(json.dumps(compiled, indent=2), encoding="utf-8")
    (out_dir / "contract.normalized.json").write_text(contract.model_dump_json(indent=2), encoding="utf-8")
    print(f"Validated. Artifacts written to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
