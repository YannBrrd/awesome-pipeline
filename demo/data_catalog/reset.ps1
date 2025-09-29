# Stops the stack and removes volumes (data reset)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$composeDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $composeDir
try {
  docker compose down -v
}
finally { Pop-Location }
