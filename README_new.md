# awesome-pipeline
Data Pipeline Framework & Toolchain Generator

## Description

This project provides a **framework and toolchain for generating data pipelines** based on data contracts. The goal is not to generate pipelines directly, but to **create the tools that generate pipelines**, ensuring data integrity and consistency throughout the data ecosystem.

### Key Principles
- **Data Contract-Driven**: All pipeline generation starts from standardized data contracts
- **Generic & Extensible**: Framework supports multiple data sources and sinks
- **Industry Standards**: Integrates with established tools (DLT, Great Expectations, Data Contract CLI)
- **Cross-Platform**: Shell scripts work across different operating systems
- **Tool Generator**: Creates tools to generate pipelines, not the pipelines themselves

### Supported Integrations
- **Major Cloud Platforms**: BigQuery, Databricks, Snowflake, MS Fabric
- **Data Sources**: HTTP APIs, databases, file systems (via DLTHub)
- **Data Quality**: Great Expectations (GX) for comprehensive data validation
- **Validation**: Data Contract CLI for contract compliance
- **Orchestration**: Dagster for workflow management
- **Catalog**: OpenMetadata for data discovery and lineage

## Framework Architecture

```
1. Data Contracts     ← Define schemas, quality rules, SLAs
2. Validation        ← Validate contracts with Data Contract CLI  
3. Pipeline Generation ← Generate DLT scripts with Pydantic expectations
4. DDL Generation    ← Create schemas for catalogs
5. Quality Rules     ← Generate Great Expectations suites
6. Processing        ← Transform and model data
7. Orchestration     ← Dagster workflow automation
8. Data Catalog      ← Metadata and lineage discovery
```

## Project Structure

| Directory | Purpose | Key Components |
|-----------|---------|----------------|
| `1.Data_contract/` | Contract definitions & examples | YAML contracts, templates, samples |
| `2.Validation/` | Contract validation tooling | Data Contract CLI integration, shell scripts |
| `3.Ingestion/` | Pipeline generation tools | DLT generator, Pydantic models, Jinja2 templates |
| `4.DDL_for_catalogs/` | Schema generation | DDL scripts for warehouse catalogs |
| `5.GX_code/` | Data quality automation | Great Expectations suite generation |
| `6.Data_processing/` | Transformation frameworks | dbt/Spark/SQL transformation tools |
| `7.Orchestrator/` | Workflow automation | Dagster orchestration patterns |
| `8.Data_catalog/` | Metadata management | OpenMetadata local deployment |

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Validate a Data Contract
```bash
cd 2.Validation
./validate.sh ../1.Data_contract/contract.yaml
```

### 3. Generate Pipeline from Contract
```bash
cd 3.Ingestion/dlt-generator
python generate.py --contract ../../1.Data_contract/contract.yaml --out build
```

### 4. Execute Generated Pipeline
```bash
cd build
python ingest.py
```

## Framework Capabilities

### Contract-to-Pipeline Generation
- **Input**: YAML data contract with schema, quality rules, source/destination
- **Output**: Executable DLT pipeline with built-in data validation
- **Features**: Interactive CLI, multiple destinations, expectation injection

### Multi-Destination Support
- **Local Development**: DuckDB for rapid prototyping
- **Cloud Warehouses**: BigQuery, Snowflake, Databricks, MS Fabric
- **Flexible Configuration**: Environment-based destination switching

### Quality-First Approach
- **Expectation Injection**: Pydantic validations embedded in DLT scripts
- **GX Integration**: Automated Great Expectations suite generation
- **Contract Validation**: Industry-standard Data Contract CLI compliance

### Cross-Platform Tooling
- **Shell Scripts**: Bash-based automation for Linux/macOS/Windows
- **No PowerShell Dependencies**: Pure shell for maximum compatibility
- **Makefile Support**: Consistent build targets across environments

## Example Workflow

```bash
# 1. Define contract (manual)
vim 1.Data_contract/my-api/contract.yaml

# 2. Validate contract
cd 2.Validation && ./validate.sh ../1.Data_contract/my-api/contract.yaml

# 3. Generate pipeline
cd ../3.Ingestion/dlt-generator
python generate.py --contract ../../1.Data_contract/my-api/contract.yaml --out my-pipeline

# 4. Configure and run
cd my-pipeline
cp .env.example .env
# Edit .env with your credentials
python ingest.py

# 5. Generate catalog schemas
cd ../../../4.DDL_for_catalogs
datacontract-cli ddl --contract ../1.Data_contract/my-api/contract.yaml

# 6. Create quality suites
cd ../5.GX_code
datacontract-cli gx --contract ../1.Data_contract/my-api/contract.yaml
```

## Integration Example: CSV + DuckDB

The framework includes a complete example demonstrating the end-to-end workflow:

- **Sample Data**: `scripts/generate_olist_mini.py` creates synthetic e-commerce data
- **Contract**: `1.Data_contract/olist_mini/contract.yaml` defines schema and quality rules
- **Pipeline**: Generated DLT script loads CSV data into DuckDB with validation
- **Quality**: Great Expectations suite validates data quality post-ingestion
- **Catalog**: OpenMetadata provides data discovery and lineage visualization

## Framework Extensions

### Adding New Sources
- Extend `3.Ingestion/dlt-generator/contract_model.py` with new source types
- Add Jinja2 templates for source-specific code generation
- Update validation schemas in Pydantic models

### Adding New Destinations
- Extend destination types in contract model
- Add destination-specific DLT configuration templates
- Update environment variable handling

### Custom Quality Rules
- Extend expectation types in contract schema
- Add custom validation logic in DLT templates
- Generate corresponding Great Expectations suites

## Related Projects

- **Data Contracts**: https://datacontract.com/
- **DLTHub**: https://dlthub.com/
- **Great Expectations**: https://greatexpectations.io/
- **Dagster**: https://dagster.io/
- **OpenMetadata**: https://open-metadata.org/

## Framework Goals

✅ **Generic Framework**: Support multiple sources/destinations  
✅ **Contract-Driven**: All artifacts generated from contracts  
✅ **Industry Standards**: Leverage existing tools and patterns  
✅ **Quality First**: Built-in data validation and expectations  
✅ **Cross-Platform**: Shell-based automation  
✅ **Extensible**: Easy to add new sources/destinations/rules  
✅ **Developer Experience**: Minimal friction, maximum automation

This framework empowers data engineers to define, validate, and execute data pipelines with minimal friction while maintaining full lineage and data quality throughout the process.
