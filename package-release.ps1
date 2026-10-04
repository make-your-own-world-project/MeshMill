[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^\d+\.\d+\.\d+(?:\.\d+)?$')]
    [string]$Version,
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

& (Join-Path $ProjectRoot "build.ps1") -Version $Version -Clean:$Clean

$CompilerCandidates = @(
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe"
)
$Compiler = $CompilerCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $Compiler) {
    throw "Inno Setup 6 was not found. Install it on the build computer or use the GitHub Release workflow."
}

$ReleaseDirectory = Join-Path $ProjectRoot "release"
New-Item -ItemType Directory -Path $ReleaseDirectory -Force | Out-Null
& $Compiler "/DMyAppVersion=$Version" (Join-Path $ProjectRoot "installer\MeshMill.iss")
if ($LASTEXITCODE -ne 0) {
    throw "Installer build failed."
}

$PortableArchive = Join-Path $ReleaseDirectory "MeshMill-$Version-windows-x64-portable.zip"
Compress-Archive -LiteralPath (Join-Path $ProjectRoot "dist\MeshMill") -DestinationPath $PortableArchive -CompressionLevel Optimal -Force

Get-ChildItem -LiteralPath $ReleaseDirectory -File |
    Where-Object { $_.Name -ne "SHA256SUMS.txt" } |
    Sort-Object Name |
    ForEach-Object {
        $Hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        "$Hash  $($_.Name)"
    } |
    Set-Content -LiteralPath (Join-Path $ReleaseDirectory "SHA256SUMS.txt") -Encoding ascii

Write-Host "Release artifacts are ready in $ReleaseDirectory"
