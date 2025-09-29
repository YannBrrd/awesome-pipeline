# awesome-pipeline
Data Pipeline Framework & Toolchain Generator
> ⚠️ 🚧 **Warning — Work In Progress (Untested)**
> 
> **This repository is experimental and not ready for production.** Expect breaking changes, incomplete tests, and unstable tooling.
> 
> - **Testing status:** **incomplete / manual**
> - **Stability:** APIs, config, and generated artifacts may change without notice
> - **Recommended use:** evaluation, prototyping, or contributing — **not for critical workloads**
> 
> Quick actions:
> - Install validation tooling: `cd src/validation && ./install.sh`
> - Run the demo workflow: `cd demo && ./test-integration.sh`
> - Report problems: open an issue and submit a PR with fixes
> 
> Tips:
> - Review examples in `demo/contracts/` before generating artifacts
> - Always run Step 2 (validation) after editing contracts
- **Tool Generator**: Creates tools to generate pipelines, not the pipelines themselves

### Supported Integrations
- **Major Cloud Platforms**: BigQuery, Databricks, Snowflake, MS Fabric
- **Data Sources**: HTTP APIs, databases, file systems (via DLTHub)
- **Data Quality**: Great Expectations (GX) for comprehensive data validation
- **Validation**: Data Contract CLI for contract compliance
- **Orchestration**: Dagster for workflow management
- **Catalog**: OpenMetadata for data discovery and lineage

## Framework Workflow

The awesome-pipeline framework follows a **7-step workflow** to transform data contracts into fully executable pipelines with comprehensive data quality and lineage:

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

### 6. Execute data transformations with enforced DQ checks
Transform raw ingested data using the DQ Transformation Framework with automatic quality validation.

### 7. Execute the ingestion pipeline
Run the complete data ingestion pipeline with built-in quality checks, expectations, and lineage tracking.

## Project Structure

| Directory | Purpose | Key Components |
|-----------|---------|----------------|
| `src/validation/` | Contract validation tooling | Data Contract CLI integration, shell scripts |
| `src/ingestion/` | Pipeline generation tools | DLT generator, Pydantic models, Jinja2 templates |
| `src/ddl_generation/` | Schema generation | DDL scripts for warehouse catalogs |
| `src/gx_generation/` | Data quality automation | Great Expectations suite generation |
| `src/data_processing/` | DQ Transformation Framework | dbt/SQL/Spark/Python transformations with enforced DQ checks |
| `src/orchestrator/` | Workflow automation | Dagster orchestration patterns |
| `demo/contracts/` | Contract definitions & examples | YAML contracts, templates, samples |
| `demo/data_catalog/` | Metadata management | OpenMetadata local deployment |
| `demo/scripts/` | Demo utilities | Data generators, helpers |
| `demo/test-integration.sh` | End-to-end smoke test | Validates the full toolchain |

## Quick Start: End-to-End Workflow

Follow the complete 7-step workflow to transform a data contract into an executable pipeline:

### Step 1: Provide your data contract
```bash
# Use existing example or create your own
cp demo/contracts/contract.yaml demo/contracts/my-pipeline.yaml
# Edit the contract with your specifications
```

### Step 2: Validate using Data Contract CLI
```bash
cd src/validation
./validate.sh ../../demo/contracts/my-pipeline.yaml
```

### Step 3: Generate DLT script using Pydantic
```bash
cd ../ingestion/dlt-generator
python generate.py --contract ../../../demo/contracts/my-pipeline.yaml --out my-pipeline
```

### Step 4: Generate DDL for data catalogs using Data Contract CLI
```bash
cd ../../ddl_generation
./generate-ddl.sh --contract ../../demo/contracts/my-pipeline.yaml --platform duckdb
```

### Step 5: Generate GX code to integrate data quality checks
```bash
cd ../gx_generation
./generate-gx-suites.sh --contract ../../demo/contracts/my-pipeline.yaml
```

### Step 6: Execute data transformations with enforced DQ checks
```bash
cd ../data_processing/framework
# Install the DQ transformation framework
./scripts/install.sh

# Configure your transformation
cp templates/config.yaml config/my-transformation.yaml
# Edit config/my-transformation.yaml with your transformation logic
# Update `data_quality.gx_config.contract_path` to point to your contract (e.g. ../../../../demo/contracts/my-pipeline.yaml)

# Execute transformation with automatic DQ enforcement
python examples/dbt_example.py  # or sql_example.py, python_example.py
```

### Step 7: Execute the ingestion pipeline
```bash
cd ../../ingestion/dlt-generator/my-pipeline
# Configure environment variables
cp .env.example .env
# Edit .env with your credentials and settings
# Run the ingestion pipeline
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

### DQ Transformation Framework (Step 6)
- **Enforced Data Quality**: Every transformation must pass pre/post DQ validation
- **Multi-Engine Support**: dbt, SQL, Spark, Python transformations with unified DQ wrapper
- **Contract Integration**: Uses Step 5 GX suites for automated quality validation
- **Lineage Tracking**: Complete transformation lineage with quality check history
- **Flexible Configuration**: YAML-based transformation configuration with environment support

### Cross-Platform Tooling
- **Shell Scripts**: Bash-based automation for Linux/macOS/Windows
- **No PowerShell Dependencies**: Pure shell for maximum compatibility
- **Makefile Support**: Consistent build targets across environments

## Example Workflow

```bash
# Complete 7-step workflow example
# Prerequisites: pip install -r requirements.txt

# Step 1: Provide your data contract (using existing example)
cp demo/contracts/contract.yaml demo/contracts/my-pipeline.yaml
ls demo/contracts  # See available contract examples

# Step 2: Validate using Data Contract CLI
cd src/validation
./install.sh
./validate.sh ../../demo/contracts/contract.yaml

# Step 3: Generate DLT script using Pydantic
cd ../ingestion/dlt-generator
python generate.py --contract ../../../demo/contracts/contract.yaml --out my-pipeline

# Step 4: Generate DDL for data catalogs using Data Contract CLI
cd ../../ddl_generation
./generate-ddl.sh --contract ../../demo/contracts/contract.yaml --platform duckdb

# Step 5: Generate GX code to integrate data quality checks
cd ../gx_generation
./generate-gx-suites.sh --contract ../../demo/contracts/contract.yaml

# Step 6: Execute data transformations with enforced DQ checks
cd ../data_processing/framework
./scripts/install.sh
cp templates/config.yaml config/my-transformation.yaml
# Edit config/my-transformation.yaml with your transformation specifications
python examples/sql_example.py  # Execute transformation with DQ enforcement

# Step 7: Execute the ingestion pipeline
cd ../../ingestion/dlt-generator/my-pipeline
cp .env.example .env
# Edit .env with your credentials and configuration
python ingest.py

# Return to repository root
cd ../../../..
```

## Data Processing Phase (Step 6) - Detailed Setup

### Overview
The Data Processing phase transforms raw ingested data into modeled, curated layers using the **DQ Transformation Framework**. This framework enforces data quality checks while providing flexibility in transformation engines.

### Prerequisites
Before starting Step 6, ensure you have completed:
- ✅ **Step 1**: Data contract defined and ready
- ✅ **Step 2**: Contract validated successfully  
- ✅ **Step 3**: DLT ingestion scripts generated (for raw data)
- ✅ **Step 4**: DDL schemas generated for target tables
- ✅ **Step 5**: GX expectation suites generated

### Setup Process

#### 1. Install the DQ Transformation Framework
```bash
cd src/data_processing/framework

# For Linux/macOS/WSL
chmod +x scripts/install.sh
./scripts/install.sh

# For Windows PowerShell  
# For Windows PowerShell  
Set-Location src\data_processing\framework
.\scripts\install.ps1
```

#### 2. Configure Your Transformation
```bash
# Copy the configuration template
cp templates/config.yaml config/my-transformation.yaml

# Edit the configuration file
nano config/my-transformation.yaml  # or your preferred editor
```

#### 3. Example Configuration
```yaml
transformation:
  id: "customer_metrics"
  description: "Transform raw customer data to analytics-ready metrics"
  engine_type: "sql"  # or "dbt", "spark", "python"
  source_tables:
    - "raw_data.customers"
    - "raw_data.orders"
  target_tables:
    - "processed_data.customer_metrics"
  config_path: "./sql"

data_quality:
  pre_checks:
    enabled: true
    check_names: ["completeness_check", "schema_validation"]
    fail_on_error: true
  post_checks:
    enabled: true
    check_names: ["accuracy_check", "consistency_check"]
    fail_on_error: true
  gx_config:
    # Uses GX suites from Step 5
    suites_path: "../../gx_generation/suites_cli"
    contract_path: "../../../demo/contracts/contract.yaml"

engines:
  sql:
    connection_string: "duckdb:///data/warehouse.db"
    scripts_dir: "./sql"
    execution_order: "./sql/execution_order.txt"
```

#### 4. Create Your Transformation Logic

**For SQL transformations:**
```bash
mkdir sql
echo "01_customer_aggregations.sql" > sql/execution_order.txt
echo "02_customer_metrics.sql" >> sql/execution_order.txt

# Create your SQL transformation files
cat > sql/01_customer_aggregations.sql << EOF
-- Aggregate customer data
CREATE OR REPLACE TABLE temp.customer_aggregations AS
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(order_value) as total_spent,
    AVG(order_value) as avg_order_value
FROM raw_data.orders
GROUP BY customer_id;
EOF
```

**For dbt transformations:**
```bash
# Initialize dbt project
cp -r templates/dbt_project ./my_dbt_project
cd my_dbt_project
# Add your dbt models, tests, and configurations
```

#### 5. Execute Transformation with DQ Enforcement
```bash
# Execute using the appropriate example
python examples/sql_example.py      # For SQL transformations
python examples/dbt_example.py      # For dbt transformations  
python examples/python_example.py   # For Python transformations
```

### What Happens During Execution

1. **Pre-transformation DQ Checks**: Validates input data quality using GX suites from Step 5
2. **Transformation Execution**: Runs your transformation logic (SQL/dbt/Spark/Python)
3. **Post-transformation DQ Checks**: Validates output data quality
4. **Lineage Tracking**: Records transformation lineage and quality check results
5. **Reporting**: Generates comprehensive reports on transformation success/failure

### Output Structure
```
output/
├── lineage/
│   ├── lineage.yaml           # Complete transformation lineage
│   └── lineage_graph.json     # Graph format for visualization
├── reports/
│   ├── pre_dq_report.yaml     # Pre-transformation DQ results
│   ├── post_dq_report.yaml    # Post-transformation DQ results
│   └── transformation_report.yaml # Execution summary
├── gx/
│   └── expectations/          # Working GX suites (copied from Step 5)
└── logs/
    └── transformation.log     # Detailed execution logs
```

### Integration with Other Steps

- **Input**: Uses raw data from Step 3 (Ingestion)
- **Quality Checks**: Uses GX suites from Step 5
- **Schema Validation**: References DDL from Step 4
- **Contract Compliance**: Validates against contracts from Step 1
- **Output**: Produces analytics-ready data for BI tools or Step 7 (Orchestration)

### Troubleshooting

**DQ Checks Failed**: Check `output/reports/` for detailed failure information
**Transformation Failed**: Review `output/logs/transformation.log` for error details
**Configuration Issues**: Validate your YAML configuration against templates
**Missing Dependencies**: Re-run the installation script or check requirements

## Demo Example: CSV + DuckDB

The framework includes a **complete working example** demonstrating the full 6-step workflow:

### Sample Dataset
- **Synthetic Data**: `demo/scripts/generate_olist_mini.py` creates realistic e-commerce CSV data
- **Multiple Tables**: Orders, customers, products with realistic relationships and constraints
- **Quality Issues**: Intentional data quality issues to demonstrate validation capabilities

### Complete Workflow Demo
1. **Contract**: `demo/contracts/contract.yaml` - Comprehensive contract with schema and quality rules
2. **Validation**: Data Contract CLI validation ensures contract compliance
3. **DLT Generation**: Creates executable Python script with Pydantic expectations
4. **DDL Generation**: Produces DuckDB-compatible schema definitions
5. **GX Generation**: Creates Great Expectations suites for data quality monitoring
6. **Data Processing**: Uses DQ Transformation Framework to transform raw data with enforced quality checks
7. **Pipeline Execution**: Loads CSV data into DuckDB with full validation and quality checks

### Data Catalog Integration
- **OpenMetadata**: Local deployment for data discovery and lineage visualization
- **Schema Registration**: Auto-generated DDL can be applied to catalog databases
- **Lineage Tracking**: Full data lineage from source CSV through transformation to final tables

## Framework Extensions

### Adding New Sources
- Extend `src/ingestion/dlt-generator/contract_model.py` with new source types
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
✅ **DQ Transformation Framework**: Enforced data quality for all transformations with multi-engine support  
✅ **Cross-Platform**: Shell-based automation works across operating systems  
✅ **Tool Generator**: Creates tools to generate pipelines, not pipelines directly  
✅ **Minimal Friction**: Seamless experience for data engineers  
✅ **Full Lineage**: Complete data lineage tracking from source to destination  
✅ **Quality First**: Built-in data quality rules and monitoring throughout the pipeline  

**Mission**: Provide a seamless experience for data engineers to define, validate, and execute their data pipelines with minimal friction, including DQ rules and full lineage.
