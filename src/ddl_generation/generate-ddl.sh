#!/bin/bash

# Generate DDL for a specific platform using Data Contract CLI
# Usage: ./generate-ddl.sh <platform> <contract_path> <output_dir>
#
# Supported platforms: bigquery, databricks, snowflake, postgres
#
# Examples:
#   ./generate-ddl.sh bigquery ../demo/contracts/contract.yaml ./bigquery-output
#   ./generate-ddl.sh databricks ../demo/contracts/contract.yaml ./databricks-output

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 <platform> <contract_path> <output_dir>"
    echo ""
    echo "Supported platforms:"
    echo "  bigquery    - Google BigQuery"
    echo "  databricks  - Databricks Unity Catalog"
    echo "  snowflake   - Snowflake Data Cloud"
    echo "  postgres    - PostgreSQL and compatible databases"
    echo "  duckdb      - DuckDB local analytics database"
    echo ""
    echo "Examples:"
    echo "  $0 bigquery ../demo/contracts/contract.yaml ./bigquery-output"
    echo "  $0 databricks ../demo/contracts/contract.yaml ./databricks-output"
    echo "  $0 snowflake ../demo/contracts/contract.yaml ./snowflake-output"
    echo "  $0 postgres ../demo/contracts/contract.yaml ./postgres-output"
    echo "  $0 duckdb ../demo/contracts/contract.yaml ./duckdb-output"
}

# Check arguments
if [ $# -ne 3 ]; then
    print_error "Invalid number of arguments"
    show_usage
    exit 1
fi

PLATFORM="$1"
CONTRACT_PATH="$2"
OUTPUT_DIR="$3"

# Validate platform
case "$PLATFORM" in
    bigquery|databricks|snowflake|postgres|duckdb)
        print_status "Generating DDL for platform: $PLATFORM"
        ;;
    *)
        print_error "Unsupported platform: $PLATFORM"
        show_usage
        exit 1
        ;;
esac

# Check if contract file exists
if [ ! -f "$CONTRACT_PATH" ]; then
    print_error "Contract file not found: $CONTRACT_PATH"
    exit 1
fi

# Check if datacontract CLI is installed
if ! command -v datacontract &> /dev/null; then
    print_error "datacontract CLI is not installed"
    echo "Install with: pip install datacontract-cli"
    exit 1
fi

# Create output directory
print_status "Creating output directory: $OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Generate DDL
print_status "Generating $PLATFORM DDL from contract: $CONTRACT_PATH"
print_status "Output directory: $OUTPUT_DIR"

# Run datacontract CLI
if datacontract ddl --dialect "$PLATFORM" --contract "$CONTRACT_PATH" --out "$OUTPUT_DIR"; then
    print_success "DDL generation completed successfully"
    print_status "Generated files:"
    find "$OUTPUT_DIR" -type f -name "*.sql" | while read -r file; do
        echo "  📄 $file"
    done
else
    print_error "DDL generation failed"
    exit 1
fi

# Platform-specific post-processing messages
case "$PLATFORM" in
    bigquery)
        print_status "BigQuery DDL generated with:"
        echo "  • Dataset and table creation statements"
        echo "  • BigQuery-specific data types"
        echo "  • Partitioning and clustering hints (if defined in contract)"
        ;;
    databricks)
        print_status "Databricks Unity Catalog DDL generated with:"
        echo "  • Schema and table creation statements"
        echo "  • Delta Lake table properties"
        echo "  • Unity Catalog-specific features"
        ;;
    snowflake)
        print_status "Snowflake DDL generated with:"
        echo "  • Database, schema, and table creation statements"
        echo "  • Snowflake-specific data types"
        echo "  • Clustering keys and constraints"
        ;;
    postgres)
        print_status "PostgreSQL DDL generated with:"
        echo "  • Schema and table creation statements"
        echo "  • PostgreSQL data types and constraints"
        echo "  • Primary and foreign key relationships"
        ;;
    duckdb)
        print_status "DuckDB DDL generated with:"
        echo "  • Schema and table creation statements"
        echo "  • DuckDB data types and constraints"
        echo "  • Optimized for local analytics and development"
        echo "  • Compatible with DuckDB CLI and Python client"
        ;;
esac

print_success "DDL generation complete! Files available in: $OUTPUT_DIR"
