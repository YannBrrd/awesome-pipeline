#!/bin/bash

# Generate DDL for all supported platforms using Data Contract CLI
# Usage: ./generate-all-ddl.sh <contract_path> <base_output_dir>
#
# This script generates DDL for all supported platforms:
# - BigQuery
# - Databricks Unity Catalog  
# - Snowflake
# - PostgreSQL
#
# Example:
#   ./generate-all-ddl.sh ../1.Data_contract/contract.yaml ./output

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
    echo "Usage: $0 <contract_path> <base_output_dir>"
    echo ""
    echo "This script generates DDL for all supported platforms:"
    echo "  • BigQuery"
    echo "  • Databricks Unity Catalog"
    echo "  • Snowflake"  
    echo "  • PostgreSQL"
    echo "  • DuckDB"
    echo ""
    echo "Example:"
    echo "  $0 ../1.Data_contract/contract.yaml ./output"
    echo ""
    echo "Output structure:"
    echo "  <base_output_dir>/"
    echo "  ├── bigquery/"
    echo "  ├── databricks/"
    echo "  ├── snowflake/"
    echo "  ├── postgres/"
    echo "  └── duckdb/"
}

# Check arguments
if [ $# -ne 2 ]; then
    print_error "Invalid number of arguments"
    show_usage
    exit 1
fi

CONTRACT_PATH="$1"
BASE_OUTPUT_DIR="$2"

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

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if generate-ddl.sh exists
if [ ! -f "$SCRIPT_DIR/generate-ddl.sh" ]; then
    print_error "generate-ddl.sh not found in script directory: $SCRIPT_DIR"
    exit 1
fi

# Make generate-ddl.sh executable
chmod +x "$SCRIPT_DIR/generate-ddl.sh"

# Supported platforms
PLATFORMS=("bigquery" "databricks" "snowflake" "postgres" "duckdb")

print_status "Starting DDL generation for all platforms"
print_status "Contract: $CONTRACT_PATH"
print_status "Base output directory: $BASE_OUTPUT_DIR"
echo ""

# Create base output directory
mkdir -p "$BASE_OUTPUT_DIR"

# Track success/failure
SUCCESSFUL_PLATFORMS=()
FAILED_PLATFORMS=()

# Generate DDL for each platform
for PLATFORM in "${PLATFORMS[@]}"; do
    PLATFORM_OUTPUT_DIR="$BASE_OUTPUT_DIR/$PLATFORM"
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_status "Generating DDL for: $PLATFORM"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if "$SCRIPT_DIR/generate-ddl.sh" "$PLATFORM" "$CONTRACT_PATH" "$PLATFORM_OUTPUT_DIR"; then
        SUCCESSFUL_PLATFORMS+=("$PLATFORM")
        print_success "✅ $PLATFORM DDL generation completed"
    else
        FAILED_PLATFORMS+=("$PLATFORM")
        print_error "❌ $PLATFORM DDL generation failed"
    fi
    echo ""
done

# Summary report
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
print_status "GENERATION SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ${#SUCCESSFUL_PLATFORMS[@]} -gt 0 ]; then
    print_success "Successful platforms (${#SUCCESSFUL_PLATFORMS[@]}):"
    for platform in "${SUCCESSFUL_PLATFORMS[@]}"; do
        echo "  ✅ $platform"
    done
fi

if [ ${#FAILED_PLATFORMS[@]} -gt 0 ]; then
    print_error "Failed platforms (${#FAILED_PLATFORMS[@]}):"
    for platform in "${FAILED_PLATFORMS[@]}"; do
        echo "  ❌ $platform"
    done
fi

echo ""
print_status "Output structure:"
echo "  $BASE_OUTPUT_DIR/"
for PLATFORM in "${PLATFORMS[@]}"; do
    if [[ " ${SUCCESSFUL_PLATFORMS[*]} " =~ " ${PLATFORM} " ]]; then
        echo "  ├── $PLATFORM/ ✅"
    else
        echo "  ├── $PLATFORM/ ❌"
    fi
done

echo ""
if [ ${#FAILED_PLATFORMS[@]} -eq 0 ]; then
    print_success "🎉 All platforms generated successfully!"
    print_status "You can now apply these DDL scripts to your respective data platforms"
else
    print_warning "⚠️  Some platforms failed. Check the error messages above."
    exit 1
fi
