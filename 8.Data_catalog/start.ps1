# Starts the OpenMetadata stack (creates .env from example if missing)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$composeDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $composeDir
try {
  if (-not (Test-Path .env)) {
    if (Test-Path .env.example) {
      Copy-Item .env.example .env
      Write-Host "Created .env from .env.example"
    }
  }
  Write-Host "Starting OpenMetadata stack via docker compose..."
  docker compose up -d

  # Read SERVER_PORT from .env (default 8585)
  $port = 8585
  if (Test-Path .env) {
    $line = Get-Content .env | Where-Object { $_ -match '^\s*SERVER_PORT\s*=' } | Select-Object -First 1
    if ($line) {
      $val = ($line -split '=',2)[1].Trim().Trim('"').Trim("'")
      if ($val -match '^[0-9]+$') { $port = [int]$val }
    }
  }

  # Wait for port to respond (up to ~90s)
  $deadline = (Get-Date).AddSeconds(90)
  $ready = $false
  while((Get-Date) -lt $deadline) {
    try {
      $client = New-Object System.Net.Sockets.TcpClient
      $iar = $client.BeginConnect('127.0.0.1', $port, $null, $null)
      if ($iar.AsyncWaitHandle.WaitOne(1000) -and $client.Connected) { $ready = $true; $client.Close(); break }
      $client.Close()
    } catch { }
  }
  if ($ready) {
    Write-Host "OpenMetadata is up at http://localhost:$port"
  } else {
    Write-Warning "Service not reachable on http://localhost:$port yet; use .\\logs.ps1 to inspect logs"
  }
}
finally { Pop-Location }
