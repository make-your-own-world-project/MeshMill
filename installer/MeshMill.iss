#ifndef MyAppVersion
  #error MyAppVersion must be supplied by the release build
#endif

#ifndef MyAppName
  #define MyAppName "MeshMill"
#endif
#ifndef MyAppId
  #define MyAppId "{{C8E36B57-B05D-47EE-95B2-45B96E01F7D5}"
#endif
#ifndef MySettingsKey
  #define MySettingsKey "Software\MeshMill"
#endif
#ifndef MyOutputBaseFilename
  #define MyOutputBaseFilename "MeshMill-" + MyAppVersion + "-windows-x64-setup"
#endif
#define MyAppPublisher "MeshMill contributors"
#define MyAppExeName "MeshMill.exe"

[Setup]
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL=https://github.com/make-your-own-world/MeshMill
AppSupportURL=https://github.com/make-your-own-world/MeshMill/issues
AppUpdatesURL=https://github.com/make-your-own-world/MeshMill/releases/latest
DefaultDirName={localappdata}\Programs\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=..\LICENSE
OutputDir=..\release
OutputBaseFilename={#MyOutputBaseFilename}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
SetupIconFile=..\assets\meshmill.ico
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=force
RestartApplications=no
SetupLogging=yes
UsePreviousAppDir=yes
UsePreviousGroup=yes
UsePreviousTasks=yes
UninstallDisplayName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=MeshMill installer
VersionInfoProductName={#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

; Remove the previous PyInstaller payload before copying an upgrade. The Inno
; Setup uninstaller and its data remain intact, while obsolete bundled modules,
; documentation, and locale files cannot survive from an older release.
[InstallDelete]
Type: filesandordirs; Name: "{app}\_internal"
Type: filesandordirs; Name: "{app}\assets"
Type: filesandordirs; Name: "{app}\docs"
Type: filesandordirs; Name: "{app}\locales"
Type: files; Name: "{app}\MeshMill.exe"
Type: files; Name: "{app}\MeshMillCLI.exe"
Type: files; Name: "{app}\LICENSE"
Type: files; Name: "{app}\README.md"
Type: files; Name: "{app}\ROADMAP.md"
Type: files; Name: "{app}\THIRD_PARTY_NOTICES.md"
Type: files; Name: "{app}\CUDA_EXCEPTION.md"

[Files]
Source: "..\dist\MeshMill\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autoprograms}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

; QSettings stores MeshMill preferences under this per-user key. An in-place
; upgrade keeps it. A real uninstall removes it with the rest of the app.
[Registry]
Root: HKCU; Subkey: "{#MySettingsKey}"; Flags: uninsdeletekey

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
Filename: "{app}\{#MyAppExeName}"; Parameters: "{code:GetReopenParameters}"; Flags: nowait; Check: ShouldReopen

[UninstallDelete]
Type: filesandordirs; Name: "{localappdata}\MeshMill"

[Code]
function GetReopenParameters(Param: String): String;
var
  ReopenFile: String;
begin
  ReopenFile := ExpandConstant('{param:REOPENFILE|}');
  if ReopenFile <> '' then
    Result := '"' + ReopenFile + '"'
  else
    Result := '';
end;

function ShouldReopen(): Boolean;
begin
  Result := ExpandConstant('{param:REOPEN|0}') = '1';
end;
