[CmdletBinding()]
param(
    [switch]$Clean,
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^\d+\.\d+\.\d+(?:\.\d+)?$')]
    [string]$Version
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
