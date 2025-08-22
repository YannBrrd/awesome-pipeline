#!/bin/bash
# Generate Great Expectations suites from data contracts
# This script should be run as part of Step 5 to generate GX code

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Default paths
CONTRACT_PATH="../1.Data_contract/contract.yaml"
OUTPUT_DIR="./suites_cli"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --contract)
            CONTRACT_PATH="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [--contract path/to/contract.yaml] [--output output/directory]"
            echo ""
            echo "Options:"
            echo "  --contract    Path to data contract YAML file (default: ../1.Data_contract/contract.yaml)"
            echo "  --output      Output directory for GX suites (default: ./suites_cli)"
            echo "  -h, --help    Show this help message"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Validate inputs
if [ ! -f "$CONTRACT_PATH" ]; then
    log_error "Data contract file not found: $CONTRACT_PATH"
    exit 1
fi

# Check if datacontract CLI is installed
if ! command -v datacontract &> /dev/null; then
    log_error "datacontract CLI not found. Please install it first:"
    echo "  pip install datacontract-cli"
    exit 1
fi

log_info "Generating Great Expectations suites from data contract..."
log_info "Contract: $CONTRACT_PATH"
log_info "Output: $OUTPUT_DIR"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Generate GX suites
log_info "Running datacontract export..."
datacontract export \
    --format great-expectations \
    --output "$OUTPUT_DIR" \
    "$CONTRACT_PATH"

if [ $? -eq 0 ]; then
    log_info "✅ Great Expectations suites generated successfully!"
    log_info "Generated files:"
    find "$OUTPUT_DIR" -type f -name "*.json" | head -10
    
    # Count generated files
    suite_count=$(find "$OUTPUT_DIR" -type f -name "*.json" | wc -l)
    log_info "Total expectation suites generated: $suite_count"
    
    log_info ""
    log_info "Next steps:"
    log_info "1. Review generated suites in: $OUTPUT_DIR"
    log_info "2. Customize expectations if needed"
    log_info "3. Use these suites in Step 6 data processing framework"
    log_info "4. Configure Step 6 to point to: $OUTPUT_DIR"
else
    log_error "❌ Failed to generate Great Expectations suites"
    exit 1
fi
