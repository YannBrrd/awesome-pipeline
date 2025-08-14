DLT ingestion generator

This folder contains generators that read a data contract and emit dlt pipelines with expectations (not_null, unique, min/enum/pattern).

Quickstart (PowerShell)

1) Install deps
   py -m pip install -r requirements.txt

2) Validate contract
   py .\2.Validation\contract_validator.py .\1.Data_contract\olist_mini\contract.yaml

3) Generate pipeline code
   - Generic (destination via env):
     py .\3.Ingestion\generate_dlt_pipeline.py .\1.Data_contract\olist_mini\contract.yaml
   - Databricks-targeted (defaults to Databricks destination):
     py .\3.Ingestion\generate_dlt_pipeline_databricks.py .\1.Data_contract\olist_mini\contract.yaml

4) Run pipeline
   - DuckDB:
     $env:OLIST_DATA_DIR = "data/olist_mini"
     $env:DLT_DESTINATION = "duckdb"
     $env:DLT_DATASET = "raw_olist"
     py .\3.Ingestion\pipelines\contract_pipeline.py
   - Databricks (SQL Warehouse):
     $env:OLIST_DATA_DIR = "data/olist_mini"
     $env:DLT_DATASET = "raw_olist"
     # Databricks SQL connector envs (preferred)
     $env:DATABRICKS_SERVER_HOSTNAME = "<workspace-host>"
     $env:DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/<id>"
     $env:DATABRICKS_ACCESS_TOKEN = "<token>"
     # Back-compat: DATABRICKS_HOST/TOKEN also supported by the generated Databricks pipeline
     py .\3.Ingestion\pipelines\contract_databricks_pipeline.py

Notes
- The generated scripts read CSVs from data/olist_mini/<table>.csv. Use scripts/generate_olist_mini.py to create them.
- Rejected rows are appended to data/olist_mini/rejects/<table>_rejects.csv for inspection.
- For richer checks and data docs, pair this with Great Expectations in 5.GX_code.
