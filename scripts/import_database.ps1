param(
    [string]$Server,
    [string]$Database,
    [string]$Driver,
    [switch]$SeedDemo,
    [switch]$SkipSeed,
    [switch]$BasicDemo,
    [string]$Manager
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $projectRoot
try {
    if ($SeedDemo -and $SkipSeed) { throw "Use either -SeedDemo or -SkipSeed, not both." }
    if ($SkipSeed -and $Manager) { throw "-Manager cannot be used with -SkipSeed." }
    if ($SkipSeed -and $BasicDemo) { throw "-BasicDemo cannot be used with -SkipSeed." }
    $pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path -LiteralPath $pythonExe)) {
        & py -3.13 -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw "Cannot create Python 3.13 environment." }
    }

    & $pythonExe -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw "Cannot install project dependencies." }

    $setupArgs = @("scripts/setup_database.py")
    if ($Server) { $setupArgs += @("--server", $Server) }
    if ($Database) { $setupArgs += @("--database", $Database) }
    if ($Driver) { $setupArgs += @("--driver", $Driver) }
    if ($SkipSeed) { $setupArgs += "--no-seed-demo" }
    if ($BasicDemo) { $setupArgs += "--basic-demo" }
    if ($Manager) { $setupArgs += @("--manager", $Manager) }
    & $pythonExe @setupArgs
    if ($LASTEXITCODE -ne 0) { throw "Database import failed. See the error above." }
}
finally {
    Pop-Location
}
