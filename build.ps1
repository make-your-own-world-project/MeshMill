[CmdletBinding()]
param(
    [switch]$Clean,
    [string]$Version = "0.1.0"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VirtualEnvironment = Join-Path $ProjectRoot ".venv"
$Python = Join-Path $VirtualEnvironment "Scripts\python.exe"

if ($Clean) {
    foreach ($Path in @((Join-Path $ProjectRoot "build"), (Join-Path $ProjectRoot "dist"))) {
        if (Test-Path -LiteralPath $Path) {
            Remove-Item -LiteralPath $Path -Recurse -Force
        }
    }
}

if (-not (Test-Path -LiteralPath $Python)) {
    py -3.12 -m venv $VirtualEnvironment
}

& $Python -m pip install --upgrade pip
& $Python -m pip install -r (Join-Path $ProjectRoot "requirements-dev.txt")
& $Python (Join-Path $ProjectRoot "tools\write_version_info.py") --version $Version
& $Python -m PyInstaller --noconfirm (Join-Path $ProjectRoot "MeshMill.spec")

Write-Host "Build complete: $ProjectRoot\dist\MeshMill"
