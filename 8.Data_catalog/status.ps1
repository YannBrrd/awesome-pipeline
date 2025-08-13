# Shows compose services status
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$composeDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $composeDir
try {
  docker compose ps
}
finally { Pop-Location }
