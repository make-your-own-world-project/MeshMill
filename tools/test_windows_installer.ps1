[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$InstallerPath,
    [string]$ProductName = "MeshMill",
    [string]$SettingsSubkey = "Software\MeshMill",
    [string]$ReopenFile = ""
)

$ErrorActionPreference = "Stop"
$Installer = (Resolve-Path -LiteralPath $InstallerPath).Path
$TempRoot = [IO.Path]::GetFullPath($env:TEMP).TrimEnd('\') + '\'
$TestRoot = [IO.Path]::GetFullPath((Join-Path $env:TEMP ("MeshMill-installer-test-" + [guid]::NewGuid())))
$InstallDirectory = Join-Path $TestRoot "app"
$InstallLog = Join-Path $TestRoot "install.log"
$UpgradeLog = Join-Path $TestRoot "upgrade.log"
$SettingsKey = "HKCU:\$SettingsSubkey"
$SettingsRegistryPath = "HKCU\$SettingsSubkey"
$SettingsBackup = Join-Path $TestRoot "existing-settings.reg"
$HadExistingSettings = $false
$StartMenuShortcut = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\$ProductName.lnk"
$DesktopShortcut = Join-Path ([Environment]::GetFolderPath("Desktop")) "$ProductName.lnk"
$StartMenuShortcutBackup = Join-Path $TestRoot "existing-start-menu-shortcut.lnk"
$DesktopShortcutBackup = Join-Path $TestRoot "existing-desktop-shortcut.lnk"
if ($ReopenFile) {
    $ReopenFile = (Resolve-Path -LiteralPath $ReopenFile).Path
}

if (-not ($TestRoot + '\').StartsWith($TempRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Installer test directory is outside the temporary directory: $TestRoot"
}
function Invoke-CheckedProcess {
    param([string]$FilePath, [string[]]$ArgumentList)
    $Process = Start-Process -FilePath $FilePath -ArgumentList $ArgumentList -PassThru -WindowStyle Hidden
    $Process.WaitForExit()
    if ($Process.ExitCode -ne 0) {
        throw "$FilePath exited with code $($Process.ExitCode)."
    }
}

function Test-GuiLaunch {
    param([string]$FilePath)
    $Process = Start-Process -FilePath $FilePath -PassThru -WindowStyle Hidden
    try {
        Start-Sleep -Seconds 5
        if ($Process.HasExited) {
            throw "$FilePath exited during GUI startup with code $($Process.ExitCode)."
        }
    }
    finally {
        if (-not $Process.HasExited) {
            Stop-Process -Id $Process.Id -Force
            $Process.WaitForExit()
        }
    }
}

function Test-ReopenedFile {
    param([string]$Executable, [string]$ExpectedFile)
    $Deadline = [DateTime]::UtcNow.AddSeconds(15)
    $Match = $null
    while ([DateTime]::UtcNow -lt $Deadline -and -not $Match) {
        $Match = Get-CimInstance Win32_Process -Filter "Name = 'MeshMill.exe'" |
            Where-Object {
                $_.ExecutablePath -eq $Executable -and
                $_.CommandLine -like "*$ExpectedFile*"
            } |
            Select-Object -First 1
        if (-not $Match) {
            Start-Sleep -Milliseconds 250
        }
    }
    if (-not $Match) {
        throw "The upgraded application did not reopen the requested STL."
    }
    $Process = Get-Process -Id $Match.ProcessId
    Start-Sleep -Seconds 5
    if ($Process.HasExited) {
        throw "The upgraded application exited after reopening the STL."
    }
    if (-not $Process.HasExited) {
        Stop-Process -Id $Process.Id -Force
        $Process.WaitForExit()
    }
}

function Wait-ForRemoval {
    param([string]$Path, [int]$Seconds = 20)
    $Deadline = [DateTime]::UtcNow.AddSeconds($Seconds)
    $AbsentChecks = 0
    while ([DateTime]::UtcNow -lt $Deadline -and $AbsentChecks -lt 8) {
        if (Test-Path -LiteralPath $Path) {
            $AbsentChecks = 0
        }
        else {
            $AbsentChecks++
        }
        Start-Sleep -Milliseconds 250
    }
    if ($AbsentChecks -lt 8) {
        throw "Timed out waiting for removal: $Path"
    }
}

New-Item -ItemType Directory -Path $TestRoot | Out-Null
try {
    if (Test-Path -LiteralPath $StartMenuShortcut) {
        Copy-Item -LiteralPath $StartMenuShortcut -Destination $StartMenuShortcutBackup
    }
    if (Test-Path -LiteralPath $DesktopShortcut) {
        Copy-Item -LiteralPath $DesktopShortcut -Destination $DesktopShortcutBackup
    }
    if (Test-Path -LiteralPath $SettingsKey) {
        Invoke-CheckedProcess -FilePath "reg.exe" -ArgumentList @(
            "export", $SettingsRegistryPath, $SettingsBackup, "/y"
        )
        $HadExistingSettings = $true
        Remove-Item -LiteralPath $SettingsKey -Recurse -Force
    }
    $InstallArguments = @(
        "/VERYSILENT",
        "/SUPPRESSMSGBOXES",
        "/NORESTART",
        "/CURRENTUSER",
        "/DIR=$InstallDirectory",
        "/TASKS=desktopicon",
        "/LOG=$InstallLog"
    )
    Write-Host "Installing release candidate..."
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
    Write-Host "Checking installed CLI and GUI..."
    Invoke-CheckedProcess -FilePath (Join-Path $InstallDirectory "MeshMillCLI.exe") -ArgumentList @("--help")
    Test-GuiLaunch -FilePath (Join-Path $InstallDirectory "MeshMill.exe")

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
    if ($ReopenFile) {
        $UpgradeArguments += "/REOPEN=1"
        # Start-Process joins ArgumentList into one Windows command line. Preserve a path with
        # spaces as the value of this single Inno Setup parameter.
        $UpgradeArguments += "/REOPENFILE=`"$ReopenFile`""
    }
    Write-Host "Upgrading in place..."
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
    if ($ReopenFile) {
        Write-Host "Checking reopened STL..."
        Test-ReopenedFile -Executable (Join-Path $InstallDirectory "MeshMill.exe") -ExpectedFile $ReopenFile
    }
    else {
        Test-GuiLaunch -FilePath (Join-Path $InstallDirectory "MeshMill.exe")
    }

    Write-Host "Uninstalling release candidate..."
    Invoke-CheckedProcess -FilePath (Join-Path $InstallDirectory "unins000.exe") -ArgumentList @(
        "/VERYSILENT",
        "/SUPPRESSMSGBOXES",
        "/NORESTART"
    )
    Wait-ForRemoval -Path (Join-Path $InstallDirectory "MeshMill.exe")
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
    if (Test-Path -LiteralPath (Join-Path $InstallDirectory "MeshMill.exe")) {
        $Cleanup = Start-Process -FilePath $Uninstaller -ArgumentList @(
            "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART"
        ) -Wait -PassThru -WindowStyle Hidden
        Wait-ForRemoval -Path (Join-Path $InstallDirectory "MeshMill.exe")
    }
    foreach ($OwnedPath in @($StartMenuShortcut, $DesktopShortcut, $SettingsKey)) {
        if (Test-Path -LiteralPath $OwnedPath) {
            Remove-Item -LiteralPath $OwnedPath -Recurse -Force
        }
    }
    if (Test-Path -LiteralPath $StartMenuShortcutBackup) {
        Copy-Item -LiteralPath $StartMenuShortcutBackup -Destination $StartMenuShortcut -Force
    }
    if (Test-Path -LiteralPath $DesktopShortcutBackup) {
        Copy-Item -LiteralPath $DesktopShortcutBackup -Destination $DesktopShortcut -Force
    }
    if (Test-Path -LiteralPath $TestRoot) {
        if ($HadExistingSettings -and (Test-Path -LiteralPath $SettingsBackup)) {
            Invoke-CheckedProcess -FilePath "reg.exe" -ArgumentList @("import", $SettingsBackup)
        }
        Remove-Item -LiteralPath $TestRoot -Recurse -Force
    }
}
