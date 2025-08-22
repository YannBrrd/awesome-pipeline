# Copilot System Prompt: Data Contract–Driven Pipeline Generator

You are generating a toolkit (not a specific pipeline) that scaffolds code, configs, and scripts to build data pipelines driven by Data Contracts. All prose, comments, and documentation must be in English.

## High-level objective
Create a generic, extensible code generator that:
- Ingests a Data Contract file as the single source of truth.
- Emits a ready-to-run pipeline scaffold supporting multiple sources and sinks.
- Injects data quality (DQ) rules and full lineage end-to-end.
- Validates and enforces the contract throughout the pipeline lifecycle.
- Produces only cross-platform shell automation (POSIX sh and PowerShell) for all CLI entry points.

Do not build a specific pipeline here; build the tools to generate pipelines.

## Supported platforms (first-class)
- Sources and sinks: BigQuery, Databricks (Spark), Snowflake, Microsoft Fabric.
- Example/reference implementation: CSV source → DuckDB sink + data catalog.

## Required technologies
- Data loading/orchestration: DLT (via DLTHub).
- Schema and expectations injection: Pydantic models → injected `expects` in DLT scripts.
- Data quality: Great Expectations (GX).
- Contract validation and GX code-gen: Data Contract CLI.
- Lineage: emit lineage metadata (e.g., OpenLineage-compatible JSON) from generated tasks.

## Architectural blueprint (what to generate)
Generate a CLI tool (Python package) named `dcgen` with subcommands:

- `dcgen init`
  - Create a minimal Data Contract template and project scaffold.
- `dcgen generate --contract path/to/contract.yaml --target <bigquery|databricks|snowflake|msfabric|duckdb> --source <csv|...>`
  - Render code, configs, and scripts from the contract into `./build/<project_name>/`.
  - Output includes:
    - DLT pipelines with Pydantic models and inline `expects` for field-level constraints.
    - GX suites and checkpoints auto-generated via Data Contract CLI.
    - Connection/config stubs for the chosen source and sink.
    - Cross-platform shell scripts: `run.sh` and `run.ps1` to validate contract, (re)generate GX, and run the pipeline.
    - Lineage emitters that publish run metadata.
- `dcgen validate --contract path/to/contract.yaml`
  - Run Data Contract CLI validation and report.
- `dcgen dq --build-dir ./build/<project_name>`
  - Execute GX checkpoints and fail fast on critical tests.
- `dcgen lineage --build-dir ./build/<project_name>`
  - Produce lineage artifacts and print their locations.

All generated code must be idempotent and re-runnable. Regeneration must never silently delete user edits—write to `./build/` only and gate overwrites with flags.

## Cross-platform scripting requirements
- Provide both `run.sh` (POSIX sh) and `run.ps1` (PowerShell 7+). Avoid Bash-isms; target `/bin/sh`.
- Scripts must:
  1) Validate the contract (Data Contract CLI)
  2) Generate/refresh GX (Data Contract CLI → GX suite/checkpoint files)
  3) Run DLT pipeline (DLTHub) with Pydantic `expects` injected
  4) Run GX checks and return non-zero on failure
  5) Emit lineage artifacts to `./lineage/`
- No platform-specific path assumptions; use relative paths only.

## Pydantic + DLT expectations (must-do)
- Derive Pydantic models directly from the contract schema.
- For each field constraint (type, nullable, ranges, regex, enums), inject DLT `expects` close to the extraction/transform step.
- Provide a single source of truth for constraints: parse once from the contract and reuse for Pydantic, DLT `expects`, and GX expectations to prevent drift.

## Great Expectations (GX) integration
- Use Data Contract CLI to generate GX suites from the contract.
- Create checkpoints per dataset with clear, stable names.
- Wire checkpoints into `run.sh`/`run.ps1`.
- On failure, exit non-zero and write human-readable reports to `./reports/gx/`.

## Data Contract CLI usage
- Validate the contract at generation time and at run time.
- Generate GX suites from the contract.
- Reject generation if the contract is invalid.

## Connectors (scaffold expectations)
- BigQuery: produce `profiles` or connection stubs; example DLT pipeline for loading to a table; partition/cluster hints if present in the contract.
- Databricks: Spark session bootstrap and table creation DDL stubs.
- Snowflake: stage + copy strategy stub and role/schema hints.
- MS Fabric: Lakehouse table writer stub and workspace placeholders.
- DuckDB (example path): local file path config and simple SQL DDL.

Keep platform-specific details behind a uniform interface: `dcgen/targets/<target>/renderer.py`.

## Example project (must generate with `dcgen init`)
- Contract-driven CSV → DuckDB sample:
  - `data/sample/customers.csv`
  - `contracts/customers.yaml`
  - Generated pipeline in `build/customers/`
  - Minimal data catalog (YAML or JSON) in `./catalog/` describing datasets and ownership.

## Deliverables the generator must emit
- Source:
  - `dcgen/` Python package with `__main__.py` CLI.
  - `dcgen/renderers/` for DLT, GX, configs, scripts.
  - `dcgen/targets/{bigquery,databricks,snowflake,msfabric,duckdb}/renderer.py`
- Templates:
  - Jinja2 or simple string templates for DLT scripts, Pydantic models, GX suite/checkpoint, connection stubs, shell scripts.
- Output tree (example):
  - `build/<project>/dlt/<pipeline>.py`
  - `build/<project>/models/<dataset>.py` (Pydantic)
  - `build/<project>/gx/` (suites, checkpoints)
  - `build/<project>/scripts/run.sh`
  - `build/<project>/scripts/run.ps1`
  - `build/<project>/configs/<target>.yaml`
  - `build/<project>/lineage/`
  - `build/<project>/catalog/`

## Acceptance criteria
- One-command bootstrap: `dcgen init` produces a runnable CSV→DuckDB example.
- `./scripts/run.sh` and `./scripts/run.ps1` succeed on valid data and fail on DQ violations.
- Regeneration is deterministic given the same contract.
- Supports at least the four main sinks plus the CSV→DuckDB example.
- All documentation and comments are in English.

## Style and constraints for generated code
- Python 3.12; standard library only for the generator except where specific libraries are required by the user (DLT/GX/Jinja2). Avoid numpy.
- Clear module docstrings explaining how files were generated and which parts are safe to edit.
- Provide typed function signatures and docstrings.
- No external network calls at generation time other than the documented CLIs.

## Prompts to guide code generation (what to implement now)
1) Implement `dcgen/__main__.py` with argparse subcommands: `init`, `generate`, `validate`, `dq`, `lineage`.
2) Implement a contract parser that normalizes field constraints into a single internal model reused by Pydantic, DLT `expects`, and GX.
3) Implement a renderer for DLT pipelines that injects `expects` based on the normalized model.
4) Implement GX suite/checkpoint rendering triggered via Data Contract CLI, and wire it to the scripts.
5) Implement cross-platform `run.sh` and `run.ps1` templates performing: validate → codegen GX → run DLT → run GX → emit lineage.
6) Implement the CSV→DuckDB example end-to-end under `dcgen init`.
7) Provide unit tests for the parser and renderers.

## Non-goals (explicitly exclude)
- Building or running cloud infrastructure.
- Rich orchestration beyond what is needed to run the example.
- Non-English documentation.

## Example commands (to document in README)
- `python -m dcgen init`
- `python -m dcgen generate --contract contracts/customers.yaml --target duckdb --source csv`
- `./build/customers/scripts/run.sh` (or `./build/customers/scripts/run.ps1`)

