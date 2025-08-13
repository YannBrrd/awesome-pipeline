DLT ingestion generator

This folder contains a generator that reads a data contract and emits a dlt pipeline with simple expectations (not_null, unique, min constraints) executed pre-load.

Quickstart (PowerShell)

1) Install deps
   py -m pip install -r requirements.txt

2) Validate contract
   py .\2.Validation\contract_validator.py .\1.Data_contract\olist_mini\contract.yaml

3) Generate pipeline code
   py .\3.Ingestion\generate_dlt_pipeline.py .\1.Data_contract\olist_mini\contract.yaml

4) Run pipeline to DuckDB (writes to .dlt/ and raw_olist dataset)
   $env:OLIST_DATA_DIR = "data/olist_mini"
   $env:DLT_DESTINATION = "duckdb"
   $env:DLT_DATASET = "raw_olist"
   py .\3.Ingestion\pipelines\contract_pipeline.py

Notes
- The generated script reads CSVs from data/olist_mini/<table>.csv. Use scripts/generate_olist_mini.py to create them.
- Rejected rows are appended to data/olist_mini/rejects/<table>_rejects.csv for inspection.
- For richer checks and data docs, pair this with Great Expectations in 5.GX_code.
