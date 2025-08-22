# DQ Transformation Framework

A comprehensive framework for data transformations with enforced data quality checks using Great Expectations. This framework provides a standardized way to run any type of data transformation (dbt, SQL, Spark, Python) while ensuring data quality through automated pre and post-transformation checks.

## 🎯 Features

- **Multi-Engine Support**: dbt, SQL, Spark, Python transformations
- **Enforced Data Quality**: Mandatory pre/post transformation checks using Great Expectations
- **Data Contract Integration**: Uses Data Contract CLI for validation and GX suite generation
- **Lineage Tracking**: Automatic data lineage generation and tracking
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Flexible Configuration**: YAML-based configuration with environment support
- **Comprehensive Reporting**: Detailed reports for transformations and quality checks

## 🏗️ Architecture

```
DQ Transformation Framework
├── wrapper.py              # Main transformation wrapper
├── engines/                # Transformation engine adapters
│   ├── dbt_engine.py      # dbt transformations
│   ├── sql_engine.py      # SQL script transformations
│   ├── spark_engine.py    # Spark transformations
│   └── python_engine.py   # Python script transformations
├── dq/                    # Data quality components
│   └── gx_runner.py       # Great Expectations runner
├── utils/                 # Utilities
│   ├── config.py          # Configuration management
│   └── lineage.py         # Lineage tracking
├── templates/             # Configuration templates
├── examples/              # Example implementations
└── scripts/               # Installation and utility scripts
```

## 🚀 Quick Start

### Installation

**Option 1: Using bash (Linux/macOS/WSL)**
```bash
cd framework
chmod +x scripts/install.sh
./scripts/install.sh
```

**Option 2: Using PowerShell (Windows)**
```powershell
cd framework
.\scripts\install.ps1
```

**Option 3: Manual installation**
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pyyaml great-expectations datacontract-cli

# Optional: Install dbt for dbt transformations
pip install dbt-core dbt-duckdb

# Create directories
mkdir -p output logs config temp

# Copy example configuration
cp templates/config.yaml config/config.yaml
```

### Basic Usage

1. **Customize Configuration**
   ```bash
   # Copy and edit the configuration template
   cp templates/config.yaml config/my_config.yaml
   ```

2. **Set Up Data Contract**
   ```bash
   # Ensure your data contract is available
   # The framework will use it to generate GX suites
   ```

3. **Run a Transformation**
   ```python
   from wrapper import DQTransformationWrapper
   from utils.config import ConfigLoader
   
   # Load configuration
   config = ConfigLoader.load_config('config/my_config.yaml')
   
   # Initialize and execute
   wrapper = DQTransformationWrapper(config)
   success = wrapper.execute()
   ```

## 📋 Configuration

The framework uses YAML configuration files. Here's a basic example:

```yaml
transformation:
  id: "my_transformation"
  description: "Sample transformation with DQ checks"
  engine_type: "dbt"  # dbt, sql, spark, python
  source_tables:
    - "raw_data.customers"
  target_tables:
    - "processed_data.customer_metrics"
  config_path: "./dbt_project"

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
    contract_path: "../../1.Data_contract/contract.yaml"

engines:
  dbt:
    project_dir: "./dbt_project"
    target: "dev"
  
  sql:
    connection_string: "duckdb:///data/warehouse.db"
    scripts_dir: "./sql"
  
  spark:
    app_name: "dq_transformation"
    script_path: "./spark/transform.py"
  
  python:
    script_path: "./python/transform.py"
    requirements_file: "./python/requirements.txt"
```

## 🔧 Transformation Engines

### dbt Engine
- Executes dbt projects with full model, test, and documentation support
- Validates dbt project structure before execution
- Supports custom dbt profiles and variables

### SQL Engine
- Executes SQL scripts in specified order
- Supports multiple database backends via connection strings
- Can use execution order file for script sequencing

### Spark Engine
- Runs Spark applications (Python or Scala)
- Configurable Spark settings and cluster connection
- Supports both local and cluster execution

### Python Engine
- Executes arbitrary Python scripts
- Manages Python dependencies automatically
- Supports virtual environment isolation

## 📊 Data Quality Checks

The framework enforces data quality through Great Expectations:

1. **Pre-transformation Checks**: Validate input data quality
2. **Post-transformation Checks**: Validate output data quality
3. **Automatic Suite Generation**: Uses Data Contract CLI to generate GX suites
4. **Comprehensive Reporting**: Detailed quality check reports

### Supported Check Types
- **Completeness**: Missing values, null checks
- **Schema Validation**: Data types, column presence
- **Data Freshness**: Recency checks
- **Accuracy**: Value range and format validation
- **Consistency**: Cross-table relationship checks

## 📈 Lineage Tracking

The framework automatically tracks:
- **Transformation History**: What transformations ran when
- **Data Dependencies**: Source and target table relationships
- **Quality Check Results**: DQ check outcomes linked to datasets
- **Execution Metadata**: Runtime information and configurations

Lineage output formats:
- YAML (human-readable)
- JSON (machine-readable)
- Graph structure (for visualization tools)

## 💼 Examples

### dbt Transformation
```python
# examples/dbt_example.py
from wrapper import DQTransformationWrapper
from utils.config import ConfigLoader

config = ConfigLoader.load_config('config/dbt_config.yaml')
wrapper = DQTransformationWrapper(config)
success = wrapper.execute()
```

### SQL Transformation
```python
# examples/sql_example.py
config = {
    'transformation': {
        'engine_type': 'sql',
        'source_tables': ['raw.customers'],
        'target_tables': ['marts.customer_summary']
    },
    'engines': {
        'sql': {
            'connection_string': 'duckdb:///warehouse.db',
            'scripts_dir': './sql'
        }
    }
}

wrapper = DQTransformationWrapper(config)
success = wrapper.execute()
```

### Python Transformation
```python
# examples/python_example.py
config = {
    'transformation': {
        'engine_type': 'python',
        'source_tables': ['raw.orders'],
        'target_tables': ['processed.order_metrics']
    },
    'engines': {
        'python': {
            'script_path': './transform.py',
            'requirements_file': './requirements.txt'
        }
    }
}

wrapper = DQTransformationWrapper(config)
success = wrapper.execute()
```

## 🔍 Output Structure

After execution, the framework generates:

```
output/
├── lineage/
│   ├── lineage.yaml           # Lineage information
│   └── lineage_graph.json     # Graph structure
├── reports/
│   ├── pre_dq_report.yaml     # Pre-check results
│   ├── post_dq_report.yaml    # Post-check results
│   └── transformation_report.yaml # Execution summary
├── gx/
│   └── expectations/          # Generated GX suites
└── logs/
    └── transformation.log     # Detailed execution logs
```

## 🛠️ Integration with Pipeline Steps

This framework integrates with the broader data pipeline:

1. **Data Contracts** (Step 1): Source of truth for data structure
2. **Validation** (Step 2): Contract validation before processing
3. **Ingestion** (Step 3): DLT scripts generate source data
4. **DDL Generation** (Step 4): Schema definitions for target tables
5. **GX Code** (Step 5): Quality check definitions
6. **Data Processing** (Step 6): **This framework** - transformations with DQ
7. **Orchestration** (Step 7): Workflow management

## 🔧 Development

### Adding New Engines

To add a new transformation engine:

1. Create a new engine class in `engines/`
2. Inherit from `TransformationEngine`
3. Implement required methods: `validate_config()` and `execute()`
4. Add engine configuration to templates

### Extending DQ Checks

To add new data quality check types:

1. Extend `GXRunner` class in `dq/gx_runner.py`
2. Add check definitions to data contracts
3. Update configuration templates

## 📚 Dependencies

Core dependencies:
- `pyyaml`: Configuration management
- `great-expectations`: Data quality framework
- `datacontract-cli`: Data contract validation and GX generation

Optional dependencies (based on engines used):
- `dbt-core`: For dbt transformations
- `pyspark`: For Spark transformations
- Database-specific drivers (e.g., `duckdb`, `psycopg2`, `sqlalchemy`)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
1. Check the examples in the `examples/` directory
2. Review configuration templates in `templates/`
3. Examine the logs in `output/logs/`
4. Consult the main project README for pipeline context
