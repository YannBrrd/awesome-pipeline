# 5. Great Expectations (GX) code (via Data Contracts CLI)

Purpose
- Generate GX expectation suites from the data contract using Data Contracts CLI and store them here.

Prerequisites
- data-contract-cli installed (e.g., pipx install data-contract-cli)

Usage (Bash/Shell)
- Generate suites from contract using the shell script:

  
  ```bash
  data-contract-cli gx --contract ./1.Data_contract/olist_mini/contract.yaml --out ./5.GX_code/suites_cli
  ```

Outputs
- GX suites under `5.GX_code/suites_cli/` ready to be wired into a GX project (checkpoints, data docs).

Notes
- This replaces the previous custom suite generator. You can still run GX pre/post-ingestion to enforce quality.