# Stops the OpenMetadata stack (keeps volumes)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$composeDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $composeDir
try {
  docker compose down
}
finally { Pop-Location }
