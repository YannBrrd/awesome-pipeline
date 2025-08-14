# 4. DDL for catalogs (via Data Contracts CLI)

Purpose
- Generate Unity Catalog DDL from the data contract using Data Contracts CLI.

Prerequisites
- data-contract-cli installed (e.g., pipx install data-contract-cli)
- Contract at `1.Data_contract/olist_mini/contract.yaml`

Usage (PowerShell)
- Databricks Unity Catalog DDL:
  
  ```powershell
  data-contract-cli ddl --dialect databricks --contract .\1.Data_contract\olist_mini\contract.yaml --out .\4.DDL_for_catalogs\ddl_cli
  ```

Outputs
- SQL files under `4.DDL_for_catalogs/ddl_cli/` (ordered for FK dependencies where supported).

Notes
- This repository now targets Databricks only for DDL. Previous Python generators are deprecated.
