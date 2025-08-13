# TODO

A concise backlog to take this pipeline from demo to robust.

## Priority P0 (next)
- [ ] Run synthetic data generation and a full end-to-end ingest once
  - py .\\scripts\\generate_olist_mini.py
  - py .\\2.Validation\\contract_validator.py .\\1.Data_contract\\olist_mini\\contract.yaml
  - py .\\4.DDL_for_catalogs\\generate_ddl.py
  - py .\\3.Ingestion\\generate_dlt_pipeline.py .\\1.Data_contract\\olist_mini\\contract.yaml
  - $env:OLIST_DATA_DIR = "data/olist_mini"; py .\\3.Ingestion\\pipelines\\contract_pipeline.py
- [ ] Commit generated DDL (4.DDL_for_catalogs\\ddl\\create_all.sql) and GX suites (5.GX_code\\expectations)
- [ ] Orchestrator: launch Dagster and run job `build_and_ingest` once
  - dagster dev -m 7.Orchestrator.orchestrator

## Contracts (1.Data_contract)
- [ ] Add/confirm regex patterns and enums where applicable (ids, states, categories)
- [ ] Add cross-table checks to `contract.yaml` (payments vs items, timestamps order) as documented checks
- [ ] Versioning policy: bump versions and add changelog on contract changes

## Validation (2.Validation)
- [ ] Emit per-table JSON Schema files (one file per table) in `_artifacts/`
- [ ] Optional: JSON Schema validate a small sample of each CSV (fast feedback)
- [ ] Unit tests for model validation (keys exist, FK refs valid)

## Ingestion (3.Ingestion)
- [ ] Extend generator to include: max constraints, basic FK existence checks (warn/reject)
- [ ] Partition rejects by reason (not_null/unique/enum/pattern/min) and by date
- [ ] Add typed casting map from contract types (decimal/date/timestamp) instead of best-effort casts
- [ ] Support additional destinations via env (bigquery, snowflake) and doc required creds
- [ ] Lightweight logging/metrics (row counts, rejects) per table

## DDL (4.DDL_for_catalogs)
- [ ] Add platform flavors: Postgres, BigQuery, Snowflake type mapping and DDL emitters
- [ ] Emit indexes for PKs and common FKs; optional unique constraints for natural keys
- [ ] Emit comments from field descriptions (if present)
- [ ] Generate DROP/CREATE and ALTER migration stubs

## Great Expectations (5.GX_code)
- [ ] Scaffold a GX project (datasource, checkpoint, data docs) targeting DuckDB
- [ ] Generate and run checkpoints per table pre/post load
- [ ] Parameterize tolerance (mostly) via env and persist in checkpoint configs
- [ ] Translate cross-table SQL check into a GX validation (custom expectation or QueryExpectation)

## Data processing (6.Data_processing)
- [ ] Add a couple of example transformations (order totals, delivery SLAs, review aggregates)
- [ ] Add tests for transformations (row-count and value spot checks)

## Orchestrator (7.Orchestrator)
- [ ] Add a daily schedule and a file sensor for new CSV drops
- [ ] Split into two jobs: build (validate+DDL+GX+codegen) and ingest (per dataset)
- [ ] Add run config schema (data_dir, destination, dataset) and defaults via resources
- [ ] Persist Dagster run storage and event logs (e.g., sqlite/duckdb)

## CI/CD
- [ ] GitHub Actions: lint/type-check, validate contract, generate DDL, run unit tests
- [ ] Optional nightly E2E: generate data -> ingest -> run GX -> publish data docs as artifact
- [ ] Pre-commit hooks (ruff/black, yaml formatting)

## Docs
- [ ] Root README: add quickstart (one copy-paste block) and architecture diagram
- [ ] Add folder READMEs cross-linking commands and outputs
- [ ] Troubleshooting section (common errors: missing env, dependency install)

## Nice to have
- [ ] OpenLineage or dlt lineage export for end-to-end runs
- [ ] Data catalog registration step (Glue/BigQuery Data Catalog/OpenMetadata) using generated DDL/metadata
- [ ] Sample dashboard or notebook showcasing curated metrics

## Data Catalog (8.Data_catalog)
- [ ] Add example OpenMetadata ingestion recipe(s) to register warehouse/tables
- [ ] Provide scripts to run ingestion workflows (CLI) once OpenMetadata is up
- [ ] Optionally expose OM configs via env templates for local demo

## Databricks Lakehouse target (new)
- [ ] Ingestion: add Databricks destination option
  - Support writing via Databricks SQL Warehouse (JDBC/ODBC) or Delta Lake files (S3/ADLS) with auto-create tables
  - Env config: DATABRICKS_HOST, DATABRICKS_HTTP_PATH, DATABRICKS_TOKEN, and/or cloud storage creds
  - Update generator to emit destination-specific pipeline settings
- [ ] DDL: emit Databricks/Spark SQL dialect
  - Map types to STRING, BIGINT, DOUBLE, DECIMAL(p,s), DATE, TIMESTAMP
  - Note: PK/FK constraints are informational; enforce via expectations
  - Generate CREATE SCHEMA/USE statements and optionally Unity Catalog three-level names
- [ ] Great Expectations on Spark
  - Generate Spark-based GX config and checkpoints targeting Databricks (either cluster or SQL Warehouse)
  - Add QueryExpectation examples for cross-table checks
- [ ] Orchestrator
  - Add Dagster ops to run Databricks Jobs (REST API) or notebooks with parameters
  - Secrets via environment/credentials: DATABRICKS_* and cloud storage
- [ ] Catalog integration
  - Add OpenMetadata connector configs for Databricks/Unity Catalog (ingest schemas, lineage, queries)
  - Optional: Schedules for metadata sync
- [ ] Docs & CI
  - Document required secrets and minimal IAM for cloud storage access
  - GitHub Actions job (matrix) to lint/generate DDL for Databricks dialect and dry-run GX Spark locally
