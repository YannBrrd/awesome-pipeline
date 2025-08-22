# 2. Validation

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
./validate.sh ../1.Data_contract/olist_mini/contract.yaml
# or  
make validate CONTRACT=../1.Data_contract/olist_mini/contract.yaml

# Lint only
datacontract lint ../1.Data_contract/contract.yaml
# or
make lint CONTRACT=../1.Data_contract/contract.yaml
```

#### Features
- **Automatic lint** with `datacontract lint`
- **YAML validation** structure and syntax
- **Schema export** (JSON Schema, etc.) if supported
- **Batch validation** of all contracts
- **Shell scripts** for CI/CD

## Inputs
- Contracts from `../1.Data_contract/` (examples moved here)

## Outputs
- **Validation reports** via Data Contract CLI
- **Schema exports** (JSON Schema, etc.)
- Compiled contract JSON/YAML
- Derived schemas (Avro/Parquet/DDL-ready)
- Quality rule templates for GX
- Human-readable docs

## Flow
1) Read contracts from `1.Data_contract/`. 2) **Validate with Data Contract CLI.** 3) Export artifacts for ingestion and processing.
