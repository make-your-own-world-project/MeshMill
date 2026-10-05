[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$InstallerPath
)

$ErrorActionPreference = "Stop"
$Installer = (Resolve-Path -LiteralPath $InstallerPath).Path
$TempRoot = [IO.Path]::GetFullPath($env:TEMP).TrimEnd('\') + '\'
$TestRoot = [IO.Path]::GetFullPath((Join-Path $env:TEMP ("MeshMill-installer-test-" + [guid]::NewGuid())))
$InstallDirectory = Join-Path $TestRoot "app"
$InstallLog = Join-Path $TestRoot "install.log"
$UpgradeLog = Join-Path $TestRoot "upgrade.log"
$SettingsKey = "HKCU:\Software\MeshMill"
$StartMenuShortcut = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\MeshMill.lnk"
$DesktopShortcut = Join-Path ([Environment]::GetFolderPath("Desktop")) "MeshMill.lnk"

if (-not ($TestRoot + '\').StartsWith($TempRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Installer test directory is outside the temporary directory: $TestRoot"
}
if (Test-Path -LiteralPath $SettingsKey) {
    throw "Refusing to run because MeshMill user settings already exist for this account."
}

function Invoke-CheckedProcess {
    param([string]$FilePath, [string[]]$ArgumentList)
    $Process = Start-Process -FilePath $FilePath -ArgumentList $ArgumentList -Wait -PassThru -WindowStyle Hidden
    if ($Process.ExitCode -ne 0) {
        throw "$FilePath exited with code $($Process.ExitCode)."
    }
}

New-Item -ItemType Directory -Path $TestRoot | Out-Null
try {
    $InstallArguments = @(
        "/VERYSILENT",
        "/SUPPRESSMSGBOXES",
        "/NORESTART",
        "/CURRENTUSER",
        "/DIR=$InstallDirectory",
        "/TASKS=desktopicon",
        "/LOG=$InstallLog"
    )
    Invoke-CheckedProcess -FilePath $Installer -ArgumentList $InstallArguments

    foreach ($Required in @("MeshMill.exe", "MeshMillCLI.exe", "unins000.exe")) {
        if (-not (Test-Path -LiteralPath (Join-Path $InstallDirectory $Required))) {
            throw "Installed file is missing: $Required"
        }
    }
    if (-not (Test-Path -LiteralPath $StartMenuShortcut)) {
        throw "The Start menu shortcut was not created."
    }
    if (-not (Test-Path -LiteralPath $DesktopShortcut)) {
        throw "The requested desktop shortcut was not created."
    }
    Invoke-CheckedProcess -FilePath (Join-Path $InstallDirectory "MeshMillCLI.exe") -ArgumentList @("--help")

    New-Item -ItemType Directory -Path $SettingsKey -Force | Out-Null
    New-ItemProperty -Path $SettingsKey -Name "InstallerUpgradeTest" -Value "preserve" -Force | Out-Null
    $ObsoleteFile = Join-Path $InstallDirectory "_internal\obsolete-meshmill-upgrade-test.txt"
    Set-Content -LiteralPath $ObsoleteFile -Value "obsolete" -Encoding ascii

    $UpgradeArguments = @(
        "/VERYSILENT",
        "/SUPPRESSMSGBOXES",
        "/NORESTART",
        "/CURRENTUSER",
        "/DIR=$InstallDirectory",
        "/LOG=$UpgradeLog"
    )
    Invoke-CheckedProcess -FilePath $Installer -ArgumentList $UpgradeArguments
    if (Test-Path -LiteralPath $ObsoleteFile) {
        throw "The upgrade left an obsolete PyInstaller payload file behind."
    }
    if ((Get-ItemPropertyValue -LiteralPath $SettingsKey -Name "InstallerUpgradeTest") -ne "preserve") {
        throw "The upgrade did not preserve user settings."
    }
    if (-not (Test-Path -LiteralPath $DesktopShortcut)) {
        throw "The upgrade did not preserve the selected desktop shortcut task."
    }
    Invoke-CheckedProcess -FilePath (Join-Path $InstallDirectory "MeshMillCLI.exe") -ArgumentList @("--help")

    Invoke-CheckedProcess -FilePath (Join-Path $InstallDirectory "unins000.exe") -ArgumentList @(
        "/VERYSILENT",
        "/SUPPRESSMSGBOXES",
        "/NORESTART"
    )
    if (Test-Path -LiteralPath (Join-Path $InstallDirectory "MeshMill.exe")) {
        throw "The uninstaller left the application executable behind."
    }
    if (Test-Path -LiteralPath $StartMenuShortcut) {
        throw "The uninstaller left the Start menu shortcut behind."
    }
    if (Test-Path -LiteralPath $DesktopShortcut) {
        throw "The uninstaller left the desktop shortcut behind."
    }
    if (Test-Path -LiteralPath $SettingsKey) {
        throw "The uninstaller left MeshMill user settings behind."
    }
    Write-Host "Installer install, upgrade, launch, and uninstall checks passed."
}
finally {
    $Uninstaller = Join-Path $InstallDirectory "unins000.exe"
    if (Test-Path -LiteralPath $Uninstaller) {
        $Cleanup = Start-Process -FilePath $Uninstaller -ArgumentList @(
            "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART"
        ) -Wait -PassThru -WindowStyle Hidden
    }
    foreach ($OwnedPath in @($StartMenuShortcut, $DesktopShortcut, $SettingsKey)) {
        if (Test-Path -LiteralPath $OwnedPath) {
            Remove-Item -LiteralPath $OwnedPath -Recurse -Force
        }
    }
    if (Test-Path -LiteralPath $TestRoot) {
        Remove-Item -LiteralPath $TestRoot -Recurse -Force
    }
}
