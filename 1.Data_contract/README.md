# 1. Data contract

Purpose
- Define producer-owned, versioned data contracts that drive the rest of the pipeline.
- Store contract examples and templates for different use cases.

## What goes here
- **Contract definitions** (YAML/JSON), one per dataset/domain
- **Example contracts** for different destinations and patterns
- **Sample payloads** for producers/consumers
- **Templates** and documentation

## Current structure
```
1.Data_contract/
├── olist_mini/
│   └── contract.yaml         # Existing comprehensive contract
├── contract.yaml             # DuckDB pipeline example  
├── contract-bigquery.yaml    # BigQuery pipeline example
└── README.md                 # This file
```

## Example contracts

### contract.yaml
**Basic DuckDB pipeline** - Quick start template
- Source: HTTP API with Bearer Token authentication
- Destination: Local DuckDB (ideal for development)
- Schema: Simple `orders` table with validations

### contract-bigquery.yaml  
**Advanced BigQuery pipeline** - Complete e-commerce example
- Source: Paginated REST API 
- Destination: BigQuery dataset
- Schema: `orders` and `order_items` tables with relationships
- Validations: Business constraints (amounts, currencies, etc.)

### olist_mini/contract.yaml
**Comprehensive existing contract** - Reference format
- Schema: 7 linked tables (customers, orders, products, etc.)
- Constraints: Foreign keys, complex expectations
- Metadata: Lifecycle, ownership, privacy

## Recommended layout
- `contracts/<domain>/<dataset>/contract.yaml`
- `contracts/<domain>/<dataset>/README.md`  
- `contracts/<domain>/<dataset>/samples/*.json`

## Minimum contract sections
- **metadata**: name, owner, domain, description, contacts
- **lifecycle**: version, release date, change log
- **distribution**: refresh cadence, channel, SLAs
- **schema**: fields, types, nullability, keys, constraints
- **quality**: rules/tolerances (nulls, uniqueness, ranges)
- **privacy/security**: PII flags, classification, retention

## Integration with awesome-pipeline

```
1.Data_contract/      ← YOU ARE HERE - Contracts + examples
    ↓
2.Validation/         ← Validation with Data Contract CLI
    ↓  
3.Ingestion/          ← DLT pipeline generation
    ↓
4.DDL_for_catalogs/   ← Schemas for catalogs
    ↓
5.GX_code/            ← Data quality  
    ↓
6.Data_processing/    ← Transformations
    ↓
7.Orchestrator/       ← Dagster workflows
```

## Usage

### Create a new contract
1. Copy `contract.yaml` or `contract-bigquery.yaml` as template
2. Adapt according to your source and destination
3. Validate with: `cd ../2.Validation && ./validate.sh path/to/contract.yaml`
4. Generate pipeline: `cd ../3.Ingestion/dlt-generator && python generate.py --contract ../../1.Data_contract/your-contract.yaml --out build`

### Validate examples
```bash
cd ../2.Validation
./validate.sh all  # Validates all contracts in directory
```

### Use as template
Example contracts are designed to be copied and adapted:
- `contract.yaml` → Simple DuckDB pipeline
- `contract-bigquery.yaml` → Cloud BigQuery pipeline  
- `olist_mini/contract.yaml` → Complete format reference
