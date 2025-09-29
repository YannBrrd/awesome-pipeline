#!/bin/bash

# Installation script for DDL generation tools
# This script ensures all dependencies are installed and scripts are executable

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

print_status "Installing DDL generation tools..."

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    print_error "Python is not installed or not in PATH"
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
fi

print_status "Using Python: $PYTHON_CMD"

# Install datacontract CLI
print_status "Installing datacontract CLI..."
if $PIP_CMD install datacontract-cli; then
    print_success "datacontract CLI installed successfully"
else
    print_error "Failed to install datacontract CLI"
    exit 1
fi

# Make scripts executable
print_status "Making scripts executable..."
chmod +x generate-ddl.sh
chmod +x generate-all-ddl.sh

print_success "Scripts are now executable"

# Verify installation
print_status "Verifying installation..."
if command -v datacontract &> /dev/null; then
    DATACONTRACT_VERSION=$(datacontract --version 2>/dev/null || echo "unknown")
    print_success "datacontract CLI is available (version: $DATACONTRACT_VERSION)"
else
    print_error "datacontract CLI verification failed"
    exit 1
fi

# Create output directory
mkdir -p output

print_success "Installation complete!"
echo ""
print_status "Available commands:"
echo "  ./generate-ddl.sh <platform> <contract> <output_dir>"
echo "  ./generate-all-ddl.sh <contract> <output_dir>"
echo "  make help    # Show Makefile targets"
echo ""
print_status "Example usage:"
echo "  ./generate-all-ddl.sh ../demo/contracts/contract.yaml ./output"
echo "  make all CONTRACT=../demo/contracts/contract.yaml"
