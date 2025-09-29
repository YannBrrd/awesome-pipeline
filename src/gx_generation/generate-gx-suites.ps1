# PowerShell script to generate Great Expectations suites from data contracts
# This script should be run as part of Step 5 to generate GX code

param(
    [string]$Contract = "../../demo/contracts/contract.yaml",
    [string]$Output = "./suites_cli",
    [switch]$Help
)

# Colors for output
$Green = "`e[0;32m"
$Yellow = "`e[1;33m"
$Red = "`e[0;31m"
$NC = "`e[0m"

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

# Show help
if ($Help) {
    Write-Host "Usage: .\generate-gx-suites.ps1 [-Contract path\to\contract.yaml] [-Output output\directory]"
    Write-Host ""
    Write-Host "Parameters:"
    Write-Host "  -Contract    Path to data contract YAML file (default: ..\..\demo\contracts\contract.yaml)"
    Write-Host "  -Output      Output directory for GX suites (default: .\suites_cli)"
    Write-Host "  -Help        Show this help message"
    exit 0
}

# Validate inputs
if (-not (Test-Path $Contract)) {
    Write-Error "Data contract file not found: $Contract"
    exit 1
}

# Check if datacontract CLI is installed
try {
    $null = Get-Command datacontract -ErrorAction Stop
} catch {
    Write-Error "datacontract CLI not found. Please install it first:"
    Write-Host "  pip install datacontract-cli"
    exit 1
}

Write-Info "Generating Great Expectations suites from data contract..."
Write-Info "Contract: $Contract"
Write-Info "Output: $Output"

# Create output directory
if (-not (Test-Path $Output)) {
    New-Item -ItemType Directory -Path $Output -Force | Out-Null
}

# Generate GX suites
Write-Info "Running datacontract export..."
& datacontract export --format great-expectations --output $Output $Contract
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Info "✅ Great Expectations suites generated successfully!"
    Write-Info "Generated files:"
    Get-ChildItem -Path $Output -Filter "*.json" -Recurse | Select-Object -First 10 | ForEach-Object { Write-Host "  $($_.FullName)" }
    
    # Count generated files
    $suiteCount = (Get-ChildItem -Path $Output -Filter "*.json" -Recurse).Count
    Write-Info "Total expectation suites generated: $suiteCount"
    
    Write-Info ""
    Write-Info "Next steps:"
    Write-Info "1. Review generated suites in: $Output"
    Write-Info "2. Customize expectations if needed"
    Write-Info "3. Use these suites in Step 6 data processing framework"
    Write-Info "4. Configure Step 6 to point to: $Output"
} else {
    Write-Error "❌ Failed to generate Great Expectations suites"
    exit 1
}
