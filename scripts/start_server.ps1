param(
    [string]$Server,
    [string]$Database,
    [string]$Driver,
    [string]$Address = "127.0.0.1:8000",
    [switch]$NoReload,
    [switch]$InstallDependencies
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$originalEnvironment = @{}
Push-Location $projectRoot
try {
    $pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path -LiteralPath $pythonExe)) {
        & py -3.13 -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw "Cannot create Python 3.13 environment." }
        $InstallDependencies = $true
    }

    if (-not $InstallDependencies) {
        & $pythonExe -c "import importlib.util, sys; sys.exit(0 if all(importlib.util.find_spec(name) is not None for name in ('django', 'pyodbc', 'dotenv', 'mssql')) else 1)"
        if ($LASTEXITCODE -ne 0) { $InstallDependencies = $true }
    }
    if ($InstallDependencies) {
        & $pythonExe -m pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) { throw "Cannot install project dependencies." }
    }

    $overrides = @{}
    if ($Server) { $overrides["DT05_SQL_HOST"] = $Server }
    if ($Database) { $overrides["DT05_SQL_DATABASE"] = $Database }
    if ($Driver) { $overrides["DT05_SQL_DRIVER"] = $Driver }
    foreach ($key in $overrides.Keys) {
        $originalEnvironment[$key] = [Environment]::GetEnvironmentVariable($key, "Process")
        [Environment]::SetEnvironmentVariable($key, $overrides[$key], "Process")
    }

    $serverArgs = @("manage.py", "runserver", $Address)
    if ($NoReload) { $serverArgs += "--noreload" }
    & $pythonExe -u @serverArgs
    if ($LASTEXITCODE -ne 0) { throw "Server stopped with an error. See the details above." }
}
finally {
    foreach ($key in $originalEnvironment.Keys) {
        [Environment]::SetEnvironmentVariable($key, $originalEnvironment[$key], "Process")
    }
    Pop-Location
}
