# Example runner for Databricks destination
# Fill in your workspace details and token before running.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$env:OLIST_DATA_DIR = "data/olist_mini"
$env:DLT_DESTINATION = "databricks"
$env:DLT_DATASET = "raw_olist"

# Required Databricks SQL Warehouse settings
# TODO: replace with your values or set them in your user env securely
if (-not $env:DATABRICKS_HOST) { $env:DATABRICKS_HOST = "<your-workspace-host>.azuredatabricks.net" }
if (-not $env:DATABRICKS_HTTP_PATH) { $env:DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/<warehouse-id>" }
if (-not $env:DATABRICKS_TOKEN) { Write-Warning "DATABRICKS_TOKEN is not set. Set it in your user env for security." }

python .\3.Ingestion\pipelines\contract_pipeline.py
