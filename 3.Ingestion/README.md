# 3. Ingestion

Purpose
- Implement DLT-based pipelines to land raw data using validated contracts.

What goes here
- dlt project files (pipelines, resources, loaders, config).
- Connection/config templates (use env vars or secrets, do not commit secrets).

Inputs
- Validated/compiled artifacts from `../2.Validation/` and sample data.

Outputs
- Raw landing tables/objects in the target platform (bronze/raw layer).

Notes
- Keep pipeline code contract-aware (schemas, keys, SLAs) and idempotent.
