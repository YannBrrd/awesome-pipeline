# PowerShell installation script for DQ Transformation Framework
# For native Windows environments

# Colors for output
$Red = "`e[0;31m"
$Green = "`e[0;32m"
$Yellow = "`e[1;33m"
$NC = "`e[0m"

# Helper functions
function Write-Info {
    param($Message)
    Write-Host "${Green}[INFO]${NC} $Message"
}

function Write-Warn {
    param($Message)
    Write-Host "${Yellow}[WARN]${NC} $Message"
}

function Write-Error {
    param($Message)
    Write-Host "${Red}[ERROR]${NC} $Message"
}

# Check if command exists
function Test-Command {
    param($Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# Install Python dependencies
function Install-PythonDeps {
    Write-Info "Installing Python dependencies..."
    
    if (Test-Path "requirements.txt") {
        pip install -r requirements.txt
    } else {
        Write-Warn "requirements.txt not found, installing core dependencies"
        pip install pyyaml great-expectations datacontract-cli
    }
}

# Install Data Contract CLI
function Install-DataContractCLI {
    Write-Info "Checking Data Contract CLI installation..."
    
    if (Test-Command "datacontract") {
        Write-Info "Data Contract CLI already installed"
        datacontract --version
    } else {
        Write-Info "Installing Data Contract CLI..."
        pip install datacontract-cli
    }
}

# Install dbt (optional)
function Install-Dbt {
    Write-Info "Checking dbt installation..."
    
    if (Test-Command "dbt") {
        Write-Info "dbt already installed"
        dbt --version
    } else {
        Write-Warn "dbt not found. Install with: pip install dbt-core dbt-duckdb"
    }
}

# Create necessary directories
function New-Directories {
    Write-Info "Creating necessary directories..."
    
    $dirs = @("output", "logs", "config", "temp")
    foreach ($dir in $dirs) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
    }
    
    Write-Info "Directories created successfully"
}

# Setup example configuration
function Set-Config {
    Write-Info "Setting up example configuration..."
    
    if (-not (Test-Path "config\config.yaml")) {
        Copy-Item "templates\config.yaml" "config\config.yaml"
        Write-Info "Example configuration copied to config\config.yaml"
        Write-Warn "Please customize config\config.yaml for your environment"
    } else {
        Write-Info "Configuration already exists at config\config.yaml"
    }
}

# Main installation
function Main {
    Write-Info "Starting DQ Transformation Framework installation..."
    
    # Check Python
    if (-not (Test-Command "python") -and -not (Test-Command "python3")) {
        Write-Error "Python is not installed. Please install Python 3.8+ first."
        exit 1
    }
    
    # Check pip
    if (-not (Test-Command "pip") -and -not (Test-Command "pip3")) {
        Write-Error "pip is not installed. Please install pip first."
        exit 1
    }
    
    # Create virtual environment (recommended)
    $createVenv = Read-Host "Create virtual environment? [y/N]"
    if ($createVenv -match "^[Yy]$") {
        Write-Info "Creating virtual environment..."
        python -m venv venv
        
        & "venv\Scripts\Activate.ps1"
        Write-Info "Virtual environment activated"
    }
    
    # Install dependencies
    Install-PythonDeps
    Install-DataContractCLI
    Install-Dbt
    
    # Setup directories and config
    New-Directories
    Set-Config
    
    Write-Info "✅ Installation completed successfully!"
    Write-Info ""
    Write-Info "Next steps:"
    Write-Info "1. Customize config\config.yaml for your environment"
    Write-Info "2. Set up your data contract in the demo\contracts\ directory"
    Write-Info "3. Run an example: python examples\python_example.py"
    Write-Info ""
    Write-Info "For help, see the README.md file"
}

# Run main function
Main
