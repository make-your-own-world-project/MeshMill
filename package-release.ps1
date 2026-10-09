[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^\d+\.\d+\.\d+(?:\.\d+)?$')]
    [string]$Version,
    [switch]$Clean,
    [switch]$Repackage
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw "Build Python was not found at $Python."
}

$BundledRuntime = Join-Path $ProjectRoot "dist\MeshMill\_internal\cuda_runtime"
if (-not $Repackage) {
    & (Join-Path $ProjectRoot "build.ps1") -Version $Version -Clean:$Clean

    # Stage the minimal CUDA libraries used by Depth Adaptive QEM inside the app.
    $RuntimeVersion = "1.0.0"
    $RuntimeDirectory = Join-Path $ProjectRoot "build\cuda-runtime"
    if (-not ([IO.Path]::GetFullPath($RuntimeDirectory) + '\').StartsWith(
        [IO.Path]::GetFullPath($ProjectRoot) + '\', [StringComparison]::OrdinalIgnoreCase
    )) {
        throw "CUDA runtime staging directory is outside the project."
    }
    if (Test-Path -LiteralPath $RuntimeDirectory) {
        Remove-Item -LiteralPath $RuntimeDirectory -Recurse -Force
    }
    New-Item -ItemType Directory -Path $RuntimeDirectory | Out-Null
    & $Python -m pip install --only-binary=:all: --target $RuntimeDirectory -r (Join-Path $ProjectRoot "requirements-cuda-runtime.txt")
    if ($LASTEXITCODE -ne 0) { throw "CUDA runtime dependency staging failed." }
    Get-ChildItem -LiteralPath $RuntimeDirectory -Force |
        Where-Object { $_.Name -match '^numpy(?:[.-]|$)' -or $_.Name -eq 'bin' } |
        Remove-Item -Recurse -Force
    Get-ChildItem -LiteralPath $RuntimeDirectory -Recurse -Directory -Filter '__pycache__' |
        Remove-Item -Recurse -Force
    @{
        schema = 1
        runtimeVersion = $RuntimeVersion
        application = "MeshMill"
    } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $RuntimeDirectory "meshmill-cuda-runtime.json") -Encoding utf8
    if (Test-Path -LiteralPath $BundledRuntime) {
        Remove-Item -LiteralPath $BundledRuntime -Recurse -Force
    }
    Copy-Item -LiteralPath $RuntimeDirectory -Destination $BundledRuntime -Recurse
} elseif (-not (Test-Path -LiteralPath (Join-Path $ProjectRoot "dist\MeshMill\MeshMill.exe")) -or
          -not (Test-Path -LiteralPath $BundledRuntime)) {
    throw "Repackage requires an existing verified application build and bundled CUDA runtime."
}

# Refresh legal and release documentation without requiring an application rebuild.
$BundledDataRoot = Join-Path $ProjectRoot "dist\MeshMill\_internal"
@("LICENSE", "README.md", "ROADMAP.md", "THIRD_PARTY_NOTICES.md", "CUDA_EXCEPTION.md") |
    ForEach-Object {
        Copy-Item -LiteralPath (Join-Path $ProjectRoot $_) -Destination (Join-Path $BundledDataRoot $_) -Force
    }

$CompilerCandidates = @(
    (Join-Path $env:LOCALAPPDATA "Programs\Inno Setup 6\ISCC.exe"),
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe"
)
$Compiler = $CompilerCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $Compiler) {
    throw "Inno Setup 6 was not found. Install it on the build computer or use the GitHub Release workflow."
}

$ReleaseDirectory = Join-Path $ProjectRoot "release"
New-Item -ItemType Directory -Path $ReleaseDirectory -Force | Out-Null
Get-ChildItem -LiteralPath $ReleaseDirectory -File |
    Where-Object {
        $_.Name -match '^MeshMill-.+-windows-x64-(?:setup|portable|cuda-component)\.(?:exe|zip)$' -or
        $_.Name -match '^MeshMill-CUDA-runtime-.+-windows-x64\.zip$' -or
        $_.Name -eq 'SHA256SUMS.txt'
    } |
    Remove-Item -Force
& $Compiler "/DMyAppVersion=$Version" (Join-Path $ProjectRoot "installer\MeshMill.iss")
if ($LASTEXITCODE -ne 0) {
    throw "Installer build failed."
}
$PortableArchive = Join-Path $ReleaseDirectory "MeshMill-$Version-windows-x64-portable.zip"
$ArchiveBuilder = Join-Path $ProjectRoot "tools\create_reproducible_zip.py"
& $Python $ArchiveBuilder (Join-Path $ProjectRoot "dist\MeshMill") $PortableArchive
if ($LASTEXITCODE -ne 0) {
    throw "Portable archive creation failed."
}

$ReleaseArtifacts = @(
    (Join-Path $ReleaseDirectory "MeshMill-$Version-windows-x64-portable.zip"),
    (Join-Path $ReleaseDirectory "MeshMill-$Version-windows-x64-setup.exe"),
    (Join-Path $ReleaseDirectory "MeshMill-sample-scan-original.stl")
) | Where-Object { Test-Path -LiteralPath $_ }

$ReleaseArtifacts |
    Sort-Object |
    ForEach-Object {
        $Hash = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant()
        "$Hash  $(Split-Path -Leaf $_)"
    } |
    Set-Content -LiteralPath (Join-Path $ReleaseDirectory "SHA256SUMS.txt") -Encoding ascii

Write-Host "Release artifacts are ready in $ReleaseDirectory"
