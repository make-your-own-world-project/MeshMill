# Application updates

MeshMill checks for updates only when the user clicks the version control or enables the optional check at application startup. It does not install a service, scheduled task, startup item, or background update process.

## Update contract

The in-app updater:

1. Reads the latest GitHub release through the GitHub Releases API.
2. Selects the installable asset for the running operating system and architecture. Portable archives are excluded.
3. Downloads the package from the MeshMill GitHub release over HTTPS.
4. Verifies the asset against the SHA-256 digest returned by GitHub before executing it.
5. Starts the platform installer, closes MeshMill, replaces the installed version, and reopens the STL that was open.

Mesh edits that have not been saved are not serialized into the update session. The confirmation dialog identifies this condition before MeshMill closes.

## Platform status

- **Windows:** Inno Setup provides the supported per-user installer and in-place upgrade path. The installer preserves MeshMill settings, removes obsolete application files, and can reopen MeshMill with the previous STL.
- **macOS:** Automatic replacement remains disabled until releases provide a Developer ID signed and notarized `.pkg`. Preview ZIP files are portable test builds, not installers.
- **Linux:** Automatic replacement remains disabled until releases provide a supported AppImage. Preview tarballs do not have a reliable, universal installation location to replace.

When a release lacks a supported installable asset, the version control opens that release's downloads page instead of modifying the installation.

## Release requirements

Release asset names are part of the updater interface:

- `MeshMill-<version>-windows-x64-setup.exe`
- `MeshMill-<version>-macos-<architecture>.pkg`
- `MeshMill-<version>-linux-x86_64.AppImage`

Every installable asset needs a GitHub `sha256:` digest. Platform signing and native installation tests remain required in the release workflow.
