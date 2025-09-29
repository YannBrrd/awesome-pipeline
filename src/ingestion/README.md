# Ingestion

Purpose
- Generate and execute data ingestion pipelines from validated contracts.
- Transform API sources into target destinations with DLT.

## Components

### dlt-generator/
**DLT script generator from data contracts**

CLI that takes a validated YAML data contract as input, asks for missing fields interactively, then generates a complete DLT ingestion script.

#### Installation and quick usage
```bash
cd dlt-generator
./install.sh
# or
make install

# Generate a pipeline  
python generate.py --contract ../../../demo/contracts/contract.yaml --out build
# or
./start.sh demo
# or  
make demo
```

#### Features
- **Sources**: HTTP API (GET) with Bearer Token/Basic auth
- **Destinations**: DuckDB, PostgreSQL, BigQuery, Snowflake, Databricks  
- **Expectations**: Nullable, in_set, min/max validation before load
- **Pagination**: Support for page-based pagination
- **Interactive CLI**: Asks questions for missing fields
- **Jinja2 Templates**: Generates ingest.py, README.md, .env.example

#### Generated file structure
```
build/
├── ingest.py          # Executable DLT script
├── README.md          # Pipeline documentation
├── .env.example       # Environment variables
└── contract.yaml      # Completed contract
```

See `dlt-generator/README.md` for complete documentation.

## Inputs
- Validated contracts from `../../demo/contracts/` (via `../validation/`)

## Outputs  
- **Executable DLT scripts** (via dlt-generator/)
- **Configured pipelines** for different destinations
- **Generated documentation** for each pipeline

## Flow
1) Contracts validated by `validation/`. 2) **DLT generation with dlt-generator/**. 3) Execute ingestion pipelines.

## Integration in awesome-pipeline

```
demo/contracts/      ← Source contracts + examples
src/validation/      ← Validation with Data Contract CLI  
src/ingestion/       ← YOU ARE HERE - DLT generation
    └── dlt-generator/
src/ddl_generation/  ← Destination schemas
src/gx_generation/   ← Data quality
src/data_processing/ ← Transformations
src/orchestrator/    ← Dagster workflows
```
