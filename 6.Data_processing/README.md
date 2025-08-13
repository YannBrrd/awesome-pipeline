# 6. Data processing

Purpose
- Transform raw data into modeled, curated layers guided by contracts.

What goes here
- Transformation code (SQL/dbt/Spark/etc.), tests, and orchestration hooks.

Inputs
- Raw/landing data from `../3.Ingestion/` and contract-driven schemas.

Outputs
- Modeled tables/views (silver/gold) ready for discovery and BI.

Notes
- Keep lineage and quality checks (GX) wired into the workflow.
