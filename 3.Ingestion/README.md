DLT ingestion generator (Databricks)

This folder contains a generator that reads a data contract and emits a dlt pipeline with expectations (not_null, unique, min/enum/pattern) targeting Databricks SQL Warehouse.

Quickstart (PowerShell)

1) Install deps
   
  ```powershell
  py -m pip install -r requirements.txt
  ```

2) Validate contract
   
  ```powershell
  py .\2.Validation\contract_validator.py .\1.Data_contract\olist_mini\contract.yaml
  ```

3) Generate Databricks pipeline code
   
  ```powershell
  py .\3.Ingestion\generate_dlt_pipeline_databricks.py .\1.Data_contract\olist_mini\contract.yaml
  ```

4) Run pipeline (Databricks SQL Warehouse)
   
  ```powershell
  $env:OLIST_DATA_DIR = "data/olist_mini"
  $env:DLT_DATASET = "raw_olist"
  $env:DATABRICKS_SERVER_HOSTNAME = "<workspace-host>"
  $env:DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/<id>"
  $env:DATABRICKS_ACCESS_TOKEN = "<token>"
  py .\3.Ingestion\pipelines\contract_databricks_pipeline.py
  ```

Notes
- The generated scripts read CSVs from data/olist_mini/<table>.csv. Use scripts/generate_olist_mini.py to create them.
- Rejected rows are appended to data/olist_mini/rejects/<table>_rejects.csv for inspection.
- For richer checks and data docs, pair this with Great Expectations in 5.GX_code.
