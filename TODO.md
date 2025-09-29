# TODO

A concise backlog to take this pipeline from demo to robust.

## Priority P0 (next)
- [ ] Run synthetic data generation and a full end-to-end ingest once
  - cd demo && python scripts/generate_olist_mini.py
  - cd ../src/validation && ./validate.sh ../../demo/contracts/olist_mini/contract.yaml
  - cd ../ddl_generation && ./generate-ddl.sh duckdb ../../demo/contracts/olist_mini/contract.yaml ./ddl-output
  - cd ../ingestion/dlt-generator && python generate.py --contract ../../../demo/contracts/olist_mini/contract.yaml --out olist-pipeline
  - $env:OLIST_DATA_DIR = "demo/data/olist_mini"; python olist-pipeline/ingest.py
- [ ] Commit generated DDL (src\\ddl_generation\\ddl\\create_all.sql) and GX suites (src\\gx_generation\\expectations)
- [ ] Orchestrator: launch Dagster and run job `build_and_ingest` once
  - dagster dev -m src.orchestrator.orchestrator

## Contracts (demo/contracts)
- [ ] Add/confirm regex patterns and enums where applicable (ids, states, categories)
- [ ] Add cross-table checks to `contract.yaml` (payments vs items, timestamps order) as documented checks
- [ ] Versioning policy: bump versions and add changelog on contract changes

## Validation (src/validation)
- [ ] Emit per-table JSON Schema files (one file per table) in `_artifacts/`
- [ ] Optional: JSON Schema validate a small sample of each CSV (fast feedback)
- [ ] Unit tests for model validation (keys exist, FK refs valid)

## Ingestion (src/ingestion)
- [ ] Extend generator to include: max constraints, basic FK existence checks (warn/reject)
- [ ] Partition rejects by reason (not_null/unique/enum/pattern/min) and by date
- [ ] Add typed casting map from contract types (decimal/date/timestamp) instead of best-effort casts
- [ ] Support additional destinations via env (bigquery, snowflake) and doc required creds
- [ ] Lightweight logging/metrics (row counts, rejects) per table

## DDL (src/ddl_generation)
- [ ] Add platform flavors: Postgres, BigQuery, Snowflake type mapping and DDL emitters
- [ ] Emit indexes for PKs and common FKs; optional unique constraints for natural keys
- [ ] Emit comments from field descriptions (if present)
- [ ] Generate DROP/CREATE and ALTER migration stubs

## Great Expectations (src/gx_generation)
// [ ] Scaffold a GX project (datasource, checkpoint, data docs) targeting Databricks tables
- [ ] Generate and run checkpoints per table pre/post load
- [ ] Parameterize tolerance (mostly) via env and persist in checkpoint configs
- [ ] Translate cross-table SQL check into a GX validation (custom expectation or QueryExpectation)

## Data processing (src/data_processing)
- [ ] Add a couple of example transformations (order totals, delivery SLAs, review aggregates)
- [ ] Add tests for transformations (row-count and value spot checks)

## Orchestrator (src/orchestrator)
- [ ] Add a daily schedule and a file sensor for new CSV drops
- [ ] Split into two jobs: build (validate+DDL+GX+codegen) and ingest (per dataset)
- [ ] Add run config schema (data_dir, destination, dataset) and defaults via resources
// [ ] Persist Dagster run storage and event logs (e.g., sqlite)

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

## Data Catalog (demo/data_catalog)
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
