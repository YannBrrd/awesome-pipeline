# DLT script generator from data contracts

This module automatically generates [DLT (Data Load Tool)](https://dlthub.com/) ingestion scripts from YAML data contracts.

## Features

- **Simple CLI**: `python generate.py --contract contract.yaml --out ./build`
- **Pydantic validation**: Automatic contract validation with interactive questions for missing fields
- **Supported sources**: HTTP API (GET) with Bearer Token or Basic authentication
- **Supported destinations**: DuckDB, PostgreSQL, BigQuery, Snowflake, Databricks
- **Expectations**: Data validation (nullable, in_set, min/max) before loading
- **Pagination**: Support for page-based pagination
- **Jinja2 templates**: Custom script generation

## Installation

```bash
cd 2.Validation/dlt-generator
pip install -r requirements.txt
```

## Quick usage

1. **Prepare a contract** (use examples in `../../1.Data_contract/`)
2. **Generate the pipeline**:
   ```bash
   python generate.py --contract ../../1.Data_contract/contract.yaml --out build
   # or
   make demo
   # or
   ./start.sh demo
   ```
3. **Configure environment** (see `build/.env.example`)
4. **Run ingestion**:
   ```bash
   python build/ingest.py
   ```

## Contract structure

```yaml
version: "1.0"
pipeline:
  name: "my-pipeline"
source:
  type: api
  base_url: "https://api.example.com/data"
  auth:
    kind: bearer_token  # none | bearer_token | basic
    token_env: API_TOKEN
  items_path: "data.items"  # JSON path to items
  incremental:
    mode: none  # none | cursor | full_refresh
    pagination:
      type: page  # none | page
      page_param: page
      start: 1
      limit_param: per_page
      page_size: 100
destination:
  type: duckdb  # duckdb | postgres | bigquery | snowflake | databricks
  schema: main  # required except BigQuery (uses 'dataset')
  write_disposition: append  # append | replace | merge
schema:
  my_table:
    primary_key: [id]
    columns:
      id: {type: bigint, nullable: false}
      status: {type: text, in_set: ["active", "inactive"]}
      amount: {type: decimal, min: 0, max: 1000000}
```

## Interactive mode

If required fields are missing from the contract, the tool will ask you automatically:

```
? Pipeline name (pipeline.name): my-super-pipeline
? API base URL (source.base_url): https://api.example.com/orders
? Environment variable name for token (source.auth.token_env): API_TOKEN
```

## Generated files

- `build/ingest.py` - Executable DLT script
- `build/README.md` - Pipeline documentation
- `build/.env.example` - Environment variables to configure
- `build/contract.yaml` - Copy of completed contract

## Destination examples

### DuckDB (local)
```yaml
destination:
  type: duckdb
  schema: main
  write_disposition: append
```

### PostgreSQL
```yaml
destination:
  type: postgres
  schema: public
  write_disposition: append
```

### BigQuery
```yaml
destination:
  type: bigquery
  dataset: raw_data
  write_disposition: append
```

## API authentication

### Bearer Token
```yaml
source:
  auth:
    kind: bearer_token
    token_env: API_TOKEN
```
Then define `API_TOKEN=your_token` in `.env`

### Basic Auth
```yaml
source:
  auth:
    kind: basic
    username: api_user
    password_env: API_PASSWORD
```
Then define `API_PASSWORD=your_password` in `.env`

### No authentication
```yaml
source:
  auth:
    kind: none
```

## Supported expectations

The following expectations are applied before loading:

- `nullable: false` - Rejects NULL values
- `in_set: [val1, val2]` - Value must be in set
- `min: 0` - Minimum numeric value
- `max: 1000` - Maximum numeric value

## Integration in awesome-pipeline

This generator integrates into the awesome-pipeline workflow:

1. **Data Contract** (`../../1.Data_contract/`) - Schema definitions + examples
2. **Validation** (`../../2.Validation/`) - Validation with Data Contract CLI
3. **Ingestion** (`../`) - **⭐ You are here** - DLT generation
4. **Processing** (`../../6.Data_processing/`) - Transformations
5. **Orchestration** (`../../7.Orchestrator/`) - Dagster

## Current limitations

- Source: HTTP GET API only (no POST, PUT, etc.)
- Pagination: page number only (no cursor)
- Expectations: simple validation (no complex SQL)
- Authentication: Bearer Token and Basic only

## Future improvements

- File source support (CSV, Parquet, JSON)
- Cursor/offset pagination
- OAuth2 authentication
- Advanced expectations with Great Expectations
- Incremental mode with watermarks
