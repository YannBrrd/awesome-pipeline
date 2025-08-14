Dagster Orchestrator

This module orchestrates the pipeline: validate contract → generate DDL → generate GX suites → generate dlt pipeline → optional ingestion run.

Install
- ```powershell
  py -m pip install -r requirements.txt
  ```

Run the UI and job
- Start Dagster (will open localhost:3000):
  - ```powershell
    py -m pip install dagster-webserver  # if not already installed
    dagster dev -m 7.Orchestrator.orchestrator
    ```
- In the UI, launch the build_and_ingest job (optionally configure data_dir/destination/dataset).

Databricks as destination
- Set env before running the job:
  
  ```powershell
  $env:DLT_DESTINATION = "databricks"
  $env:DLT_DATASET = "raw_olist"
  $env:DATABRICKS_HOST = "xxxx.azuredatabricks.net"
  $env:DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/xxxxxxxx"
  $env:DATABRICKS_TOKEN = "<token>"
  ```

CLI run without UI
- ```powershell
  py -c "from 7.Orchestrator.orchestrator import build_and_ingest; build_and_ingest.execute_in_process()"
  ```

Notes
- The ingestion step reads CSVs from data/olist_mini and writes to Databricks (SQL Warehouse).
- DDL and GX suites are generated via Data Contracts CLI.
