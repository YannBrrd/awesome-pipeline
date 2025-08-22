# 6. Data processing

Purpose
- Transform raw data into modeled, curated layers with enforced data quality checks
- Provide a flexible wrapper framework that supports any transformation engine
- Ensure data quality through automated pre/post transformation validation

## Framework Overview

The Data Processing framework enforces **DQ-wrapped transformations** while giving users complete flexibility in their transformation logic:

- **Enforced DQ Checks**: Automatic pre/post transformation validation using Great Expectations
- **Multi-Engine Support**: dbt, SQL, Spark, Python - use whatever works best for your use case
- **Contract-Driven**: Leverages data contracts and GX suites from previous steps
- **Standardized Interface**: Consistent configuration and execution across all transformation types

## Supported Transformation Engines

| Engine | Use Case | Configuration |
|--------|----------|---------------|
| **dbt** | Analytical transformations, complex models | `dbt_project/`, model specifications |
| **SQL** | Simple transformations, direct database operations | SQL script files |
| **Spark** | Big data processing, complex ETL | PySpark scripts, cluster config |
| **Python** | Custom logic, ML preprocessing | Python scripts, dependencies |

## Framework Architecture

```
6.Data_processing/
├── framework/              # Core DQ wrapper framework
│   ├── wrapper.py         # Main transformation wrapper with DQ enforcement
│   ├── engines/           # Transformation engine adapters
│   ├── dq/               # Data quality check runners
│   └── utils/            # Lineage tracking and configuration
├── templates/             # Configuration and code templates
├── examples/              # Working examples for each engine
└── scripts/              # Shell scripts for easy execution
```

## Quick Start

### 1. Setup Framework
```bash
# Install dependencies and setup framework
./setup.sh
```

### 2. Generate Transformation Config
```bash
# Generate config template for your transformation type
./scripts/generate_transform.sh --type dbt --name customer_metrics --output ./my_transform
```

### 3. Configure Transformation
```yaml
# Edit generated transform_config.yaml
transformation:
  name: "customer_silver_layer"
  type: "dbt"
  
source:
  tables: ["raw.customers", "raw.orders"]
  contract: "../../1.Data_contract/customer_contract.yaml"
  
target:
  tables: ["silver.customer_metrics"]
  
data_quality:
  pre_checks: ["completeness", "validity"]
  post_checks: ["accuracy", "consistency"]
```

### 4. Execute with DQ Enforcement
```bash
# Run transformation with automatic DQ checks
./scripts/run_transform.sh \
    --contract ../../1.Data_contract/customer_contract.yaml \
    --config ./my_transform/transform_config.yaml
```

## Integration with awesome-pipeline

This framework integrates as **Step 6** in the awesome-pipeline workflow:

1. Provide your data contract
2. Validate using Data Contract CLI
3. Generate DLT script using Pydantic
4. Generate DDL for data catalogs using Data Contract CLI
5. Generate GX code to integrate data quality checks
6. **← YOU ARE HERE** - Execute transformations with enforced DQ checks

## Inputs
- **Raw/landing data** from `../3.Ingestion/` 
- **Data contracts** from `../1.Data_contract/`
- **GX suites** from `../5.GX_code/`
- **Schema definitions** from `../4.DDL_for_catalogs/`

## Outputs
- **Modeled tables/views** (silver/gold) ready for discovery and BI
- **DQ validation reports** with pre/post transformation results
- **Data lineage information** tracking transformations
- **Audit logs** for compliance and debugging

## Framework Features

### Automatic DQ Enforcement
- **Pre-transformation checks**: Validate input data quality before processing
- **Post-transformation checks**: Ensure output data meets quality standards
- **Fail-fast approach**: Stop pipeline if DQ checks fail
- **Detailed reporting**: Comprehensive DQ results and recommendations

### Transformation Flexibility
- **Any engine**: Use dbt, SQL, Spark, Python, or custom tools
- **Pluggable architecture**: Easy to add new transformation engines
- **User-defined logic**: Full control over transformation implementation
- **Configuration-driven**: Consistent setup across different engines

### Production Ready
- **Lineage tracking**: Automatic data lineage generation
- **Error handling**: Robust error management and recovery
- **Monitoring**: Integration with observability tools
- **Scalability**: Support for large-scale data processing
