#!/bin/bash
# Cross-platform installation script for DQ Transformation Framework
# Supports Windows (WSL/Git Bash), Linux, and macOS

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

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Linux*)     OS=Linux;;
        Darwin*)    OS=Mac;;
        CYGWIN*)    OS=Cygwin;;
        MINGW*)     OS=MinGw;;
        MSYS*)      OS=MSys;;
        *)          OS="UNKNOWN:$(uname -s)"
    esac
    log_info "Detected OS: $OS"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Python dependencies
install_python_deps() {
    log_info "Installing Python dependencies..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        log_warn "requirements.txt not found, installing core dependencies"
        pip install pyyaml great-expectations datacontract-cli
    fi
}

# Install Data Contract CLI
install_datacontract_cli() {
    log_info "Checking Data Contract CLI installation..."
    
    if command_exists datacontract; then
        log_info "Data Contract CLI already installed"
        datacontract --version
    else
        log_info "Installing Data Contract CLI..."
        pip install datacontract-cli
    fi
}

# Install dbt (optional)
install_dbt() {
    log_info "Checking dbt installation..."
    
    if command_exists dbt; then
        log_info "dbt already installed"
        dbt --version
    else
        log_warn "dbt not found. Install with: pip install dbt-core dbt-duckdb"
    fi
}

# Create necessary directories
create_directories() {
    log_info "Creating necessary directories..."
    
    mkdir -p output
    mkdir -p logs
    mkdir -p config
    mkdir -p temp
    
    log_info "Directories created successfully"
}

# Setup example configuration
setup_config() {
    log_info "Setting up example configuration..."
    
    if [ ! -f "config/config.yaml" ]; then
        cp templates/config.yaml config/config.yaml
        log_info "Example configuration copied to config/config.yaml"
        log_warn "Please customize config/config.yaml for your environment"
    else
        log_info "Configuration already exists at config/config.yaml"
    fi
}

# Main installation
main() {
    log_info "Starting DQ Transformation Framework installation..."
    
    detect_os
    
    # Check Python
    if ! command_exists python && ! command_exists python3; then
        log_error "Python is not installed. Please install Python 3.8+ first."
        exit 1
    fi
    
    # Check pip
    if ! command_exists pip && ! command_exists pip3; then
        log_error "pip is not installed. Please install pip first."
        exit 1
    fi
    
    # Create virtual environment (recommended)
    read -p "Create virtual environment? [y/N]: " create_venv
    if [[ $create_venv =~ ^[Yy]$ ]]; then
        log_info "Creating virtual environment..."
        python -m venv venv
        
        case $OS in
            MinGw|MSys|Cygwin)
                source venv/Scripts/activate
                ;;
            *)
                source venv/bin/activate
                ;;
        esac
        
        log_info "Virtual environment activated"
    fi
    
    # Install dependencies
    install_python_deps
    install_datacontract_cli
    install_dbt
    
    # Setup directories and config
    create_directories
    setup_config
    
    log_info "✅ Installation completed successfully!"
    log_info ""
    log_info "Next steps:"
    log_info "1. Customize config/config.yaml for your environment"
    log_info "2. Set up your data contract in the 1.Data_contract/ directory"
    log_info "3. Run an example: python examples/python_example.py"
    log_info ""
    log_info "For help, see the README.md file"
}

# Run main function
main "$@"
