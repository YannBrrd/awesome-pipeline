# Tails server logs (Ctrl+C to stop)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$composeDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $composeDir
try {
  docker compose logs -f openmetadata_server
}
finally { Pop-Location }
