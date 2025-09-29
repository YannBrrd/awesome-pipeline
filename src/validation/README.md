# Validation

Purpose
- Validate data contracts using Data Contract CLI and custom validators.
- Ensure contract compliance before pipeline generation.

## Components

### Data Contract CLI Validation
**Standardized validation with datacontract-cli**

Uses the official [Data Contract CLI](https://cli.datacontract.com/) tool to validate contracts according to industry standards.

#### Installation
```bash
./install.sh
# or
make install
```

#### Quick usage
```bash
# Validate all contracts
./validate.sh all
# or
make validate-all

# Validate a specific contract
# Validate a specific contract
./validate.sh ../../demo/contracts/olist_mini/contract.yaml
# or  
make validate CONTRACT=../../demo/contracts/olist_mini/contract.yaml

# Lint only
datacontract lint ../../demo/contracts/contract.yaml
# or
make lint CONTRACT=../../demo/contracts/contract.yaml
```

#### Features
- **Automatic lint** with `datacontract lint`
- **YAML validation** structure and syntax
- **Schema export** (JSON Schema, etc.) if supported
- **Batch validation** of all contracts
- **Shell scripts** for CI/CD

## Inputs
- Contracts from `../../demo/contracts/` (examples moved here)

## Outputs
- **Schema exports** (JSON Schema, etc.)
- Compiled contract JSON/YAML
- Derived schemas (Avro/Parquet/DDL-ready)
- Quality rule templates for GX
- Human-readable docs

## Flow
1) Read contracts from `../../demo/contracts/`. 2) **Validate with Data Contract CLI.** 3) Export artifacts for ingestion and processing.
