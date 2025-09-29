# DDL generation (via Data Contracts CLI)

Purpose
- Generate DDL for multiple data platforms from data contracts using Data Contracts CLI
- Support major cloud platforms: BigQuery, Databricks, Snowflake, PostgreSQL
- Enable cross-platform data catalog integration with platform-specific schemas

## Installation

### Quick Setup
```bash
# Install dependencies and make scripts executable
./install.sh
```

### Manual Setup
```bash
# Install datacontract CLI
pip install datacontract-cli

# Make scripts executable
chmod +x generate-ddl.sh generate-all-ddl.sh
```

## Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `install.sh` | Install dependencies and setup | `./install.sh` |
| `generate-ddl.sh` | Generate DDL for single platform | `./generate-ddl.sh <platform> <contract> <output>` |
| `generate-all-ddl.sh` | Generate DDL for all platforms | `./generate-all-ddl.sh <contract> <base_output>` |
| `Makefile` | Automation with make targets | `make help` |

## Supported Platforms

| Platform | Dialect | Use Case |
|----------|---------|----------|
| **BigQuery** | `bigquery` | Google Cloud data warehouse |
| **Databricks** | `databricks` | Unity Catalog and Databricks SQL |
| **Snowflake** | `snowflake` | Snowflake data cloud |
| **PostgreSQL** | `postgres` | PostgreSQL and compatible databases |
| **DuckDB** | `duckdb` | Local analytics and development |

## Quick Usage

### Using Shell Scripts
```bash
# Install and setup (run once)
./install.sh

# Generate DDL for all platforms
./generate-all-ddl.sh ../../demo/contracts/contract.yaml ./output

# Generate DDL for specific platform
./generate-ddl.sh bigquery ../../demo/contracts/contract.yaml ./bigquery-output
./generate-ddl.sh databricks ../../demo/contracts/contract.yaml ./databricks-output
./generate-ddl.sh snowflake ../../demo/contracts/contract.yaml ./snowflake-output
./generate-ddl.sh postgres ../../demo/contracts/contract.yaml ./postgres-output
./generate-ddl.sh duckdb ../../demo/contracts/contract.yaml ./duckdb-output
```

### Using Makefile
```bash
# Show available targets
make help

# Generate DDL for all platforms
make all

# Generate DDL for specific platforms
make bigquery
make databricks
make snowflake
make postgres
make duckdb

# Use custom contract or output directory
make all CONTRACT=../../demo/contracts/my-contract.yaml OUTPUT_DIR=./my-output

# Run demo with example
make demo
```

## Integration with Framework

This step generates platform-specific DDL as **Step 4** in the awesome-pipeline workflow:

1. Provide your data contract
2. Validate using Data Contract CLI  
3. Generate DLT script using Pydantic
4. **← YOU ARE HERE** - Generate DDL for data catalogs using Data Contract CLI
5. Generate GX code to integrate data quality checks
6. Execute the pipeline

## Output Structure

```
src/ddl_generation/
├── install.sh                # Dependency installation and setup
├── generate-ddl.sh           # Single platform DDL generation
├── generate-all-ddl.sh       # Multi-platform DDL generation
├── Makefile                  # Make automation targets
├── output/                   # Generated DDL files
│   ├── bigquery/            # BigQuery-specific DDL
│   ├── databricks/          # Databricks Unity Catalog DDL
│   ├── snowflake/           # Snowflake DDL
│   ├── postgres/            # PostgreSQL DDL
│   └── duckdb/              # DuckDB DDL
└── README.md               # This file
```

Each platform output contains:
- **CREATE TABLE** statements with appropriate data types
- **Primary key** and **foreign key** constraints (where supported)
- **Column comments** and **table descriptions**
- **Platform-specific optimizations** (partitioning, clustering, etc.)

## Generated DDL Features

### Cross-Platform Compatibility
- **Data Type Mapping**: Automatic conversion of contract types to platform-specific types
- **Constraint Translation**: Primary keys, foreign keys, and check constraints where supported
- **Naming Conventions**: Platform-appropriate naming and escaping
- **Schema Organization**: Proper database/schema/table hierarchy for each platform

## Platform-Specific Features

### BigQuery
- Dataset and table creation
- Partitioning and clustering hints
- BigQuery-specific data types (TIMESTAMP, GEOGRAPHY, etc.)

### Databricks
- Unity Catalog schema creation
- Delta Lake table properties
- Databricks-specific data types and constraints

### Snowflake
- Database, schema, and table creation
- Snowflake data types and features
- Clustering keys and constraints

### PostgreSQL
- Schema and table creation
- PostgreSQL data types and constraints
- Indexes and foreign key relationships

### DuckDB
- Schema and table creation optimized for analytics
- DuckDB-specific data types and features
- Columnar storage optimizations
- Perfect for local development and testing
- Compatible with DuckDB CLI and Python/R clients
