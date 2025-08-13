# 2. Validation

Purpose
- Validate data contracts and generate compiled artifacts for downstream use.

What goes here
- Validation scripts/config for Data Contracts tooling.
- Generated artifacts (e.g., compiled schema, JSON/YAML, docs) committed or ignored per your policy.

Inputs
- Contracts from `../1.Data_contract/`.

Outputs (examples)
- Compiled contract JSON/YAML
- Derived schemas (Avro/Parquet/DDL-ready)
- Quality rule templates for GX
- Human-readable docs

Flow
1) Read contracts. 2) Run validation/compilation. 3) Publish artifacts for ingestion, DDL, and GX.
