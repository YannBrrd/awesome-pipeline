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

## Framework Workflow

The awesome-pipeline framework follows a **6-step workflow** to transform data contracts into fully executable pipelines with comprehensive data quality and lineage:

### 1. Provide your data contract
Define your data schema, quality rules, and pipeline configuration in a standardized YAML contract format.

### 2. Validate using Data Contract CLI
Ensure contract compliance and correctness using industry-standard Data Contract CLI validation.

### 3. Generate DLT script using Pydantic
Create executable DLT ingestion scripts with Pydantic expectation injection for runtime data validation.

### 4. Generate DDL for data catalogs using Data Contract CLI
Produce database schemas and catalog definitions compatible with major cloud platforms.

### 5. Generate GX code to integrate data quality checks into the pipeline
Create comprehensive Great Expectations suites for automated data quality monitoring.

### 6. Execute the pipeline
Run the complete data pipeline with built-in quality checks, expectations, and lineage tracking.

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

## Quick Start: End-to-End Workflow

Follow the complete 6-step workflow to transform a data contract into an executable pipeline:

### Step 1: Provide your data contract
```bash
# Use existing example or create your own
cp 1.Data_contract/contract.yaml 1.Data_contract/my-pipeline.yaml
# Edit the contract with your specifications
```

### Step 2: Validate using Data Contract CLI
```bash
cd 2.Validation
./validate.sh ../1.Data_contract/my-pipeline.yaml
```

### Step 3: Generate DLT script using Pydantic
```bash
cd ../3.Ingestion/dlt-generator
python generate.py --contract ../../1.Data_contract/my-pipeline.yaml --out my-pipeline
```

### Step 4: Generate DDL for data catalogs using Data Contract CLI
```bash
cd ../../4.DDL_for_catalogs
datacontract ddl --contract ../1.Data_contract/my-pipeline.yaml --out ./generated-ddl
```

### Step 5: Generate GX code to integrate data quality checks
```bash
cd ../5.GX_code
datacontract gx --contract ../1.Data_contract/my-pipeline.yaml --out ./generated-gx
```

### Step 6: Execute the pipeline
```bash
cd ../3.Ingestion/dlt-generator/my-pipeline
# Configure environment variables
cp .env.example .env
# Edit .env with your credentials and settings
# Run the complete pipeline
python ingest.py
```

## Framework Capabilities

### Data Contract-Driven Architecture
- **Standardized Contracts**: YAML-based data contracts define the entire pipeline specification
- **Contract Validation**: Industry-standard Data Contract CLI ensures compliance and consistency
- **Single Source of Truth**: All pipeline artifacts generated from the same contract definition

### DLTHub Integration with Pydantic Expectations
- **Multiple Sources**: HTTP APIs, databases, file systems via DLTHub's extensive connector library
- **Expectation Injection**: Pydantic validations automatically embedded in generated DLT scripts
- **Runtime Validation**: Data quality checks executed during ingestion for immediate feedback

### Multi-Platform DDL Generation
- **Cloud-Native**: Support for BigQuery, Databricks, Snowflake, MS Fabric
- **Catalog Integration**: Auto-generated schemas compatible with major data catalogs
- **Data Contract CLI**: Leverages official tooling for consistent DDL generation

### Comprehensive Data Quality
- **Great Expectations**: Automated GX suite generation from contract specifications
- **Quality Gates**: Built-in data quality checks integrated into pipeline execution
- **Data Contract CLI GX**: Official tool integration for standard quality patterns

### Cross-Platform Tooling
- **Shell Scripts**: Bash-based automation for Linux/macOS/Windows
- **No PowerShell Dependencies**: Pure shell for maximum compatibility
- **Makefile Support**: Consistent build targets across environments

## Example Workflow

```bash
# Complete 6-step workflow example
# Prerequisites: pip install -r requirements.txt

# Step 1: Provide your data contract (using existing example)
cd 1.Data_contract
ls -la  # See available contract examples

# Step 2: Validate using Data Contract CLI
cd ../2.Validation
./validate.sh ../1.Data_contract/contract.yaml

# Step 3: Generate DLT script using Pydantic
cd ../3.Ingestion/dlt-generator
python generate.py --contract ../../1.Data_contract/contract.yaml --out my-pipeline

# Step 4: Generate DDL for data catalogs using Data Contract CLI
cd ../../4.DDL_for_catalogs
datacontract ddl --contract ../1.Data_contract/contract.yaml --out ./ddl-output

# Step 5: Generate GX code to integrate data quality checks
cd ../5.GX_code
datacontract gx --contract ../1.Data_contract/contract.yaml --out ./gx-output

# Step 6: Execute the pipeline
cd ../3.Ingestion/dlt-generator/my-pipeline
cp .env.example .env
# Edit .env with your credentials and configuration
python ingest.py
```

## Demo Example: CSV + DuckDB

The framework includes a **complete working example** demonstrating the full 6-step workflow:

### Sample Dataset
- **Synthetic Data**: `scripts/generate_olist_mini.py` creates realistic e-commerce CSV data
- **Multiple Tables**: Orders, customers, products with realistic relationships and constraints
- **Quality Issues**: Intentional data quality issues to demonstrate validation capabilities

### Complete Workflow Demo
1. **Contract**: `1.Data_contract/olist_mini/contract.yaml` - Comprehensive contract with schema and quality rules
2. **Validation**: Data Contract CLI validation ensures contract compliance
3. **DLT Generation**: Creates executable Python script with Pydantic expectations
4. **DDL Generation**: Produces DuckDB-compatible schema definitions
5. **GX Generation**: Creates Great Expectations suites for data quality monitoring
6. **Pipeline Execution**: Loads CSV data into DuckDB with full validation and quality checks

### Data Catalog Integration
- **OpenMetadata**: Local deployment for data discovery and lineage visualization
- **Schema Registration**: Auto-generated DDL can be applied to catalog databases
- **Lineage Tracking**: Full data lineage from source CSV through transformation to final tables

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

## Framework Goals & Achievements

✅ **Generic Framework**: Support for BigQuery, Databricks, Snowflake, MS Fabric  
✅ **Contract-Driven**: All artifacts generated from standardized data contracts  
✅ **DLTHub Integration**: Sourcing through DLT with Pydantic expectation injection  
✅ **Data Contract CLI**: Industry-standard validation and artifact generation  
✅ **Great Expectations**: Automated GX code generation for data quality  
✅ **Cross-Platform**: Shell-based automation works across operating systems  
✅ **Tool Generator**: Creates tools to generate pipelines, not pipelines directly  
✅ **Minimal Friction**: Seamless experience for data engineers  
✅ **Full Lineage**: Complete data lineage tracking from source to destination  
✅ **Quality First**: Built-in data quality rules and monitoring  

**Mission**: Provide a seamless experience for data engineers to define, validate, and execute their data pipelines with minimal friction, including DQ rules and full lineage.
