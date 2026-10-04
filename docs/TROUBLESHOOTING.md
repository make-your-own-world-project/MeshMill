# Troubleshooting

## Windows blocks the download

Unsigned community builds can trigger Microsoft Defender SmartScreen. Compare the downloaded
file's SHA-256 hash with `SHA256SUMS.txt` from the same GitHub Release. Signed releases identify
their publisher in Windows file properties.

## The portable build does not start

Extract the complete ZIP before running `MeshMill.exe`. The `_internal` directory must remain next
to both executables. Do not run the executable from inside the ZIP viewer.

## A large STL opens as an overview

The estimated working set exceeds the memory budget in Settings. Overview mode is intentionally
read-only. Increase the budget only when the machine has enough available memory, or reduce the
mesh before opening it for editing.

## A standard view was not saved

Press the Ctrl-modified view shortcut, then choose **Save** or press Enter in the confirmation
dialog. Saving one view also updates its opposite. The status line reports the saved view.

## Navigation shortcuts do not respond

Close any modal dialog first. Review or reset shortcuts in Settings if they were customized. The
default view shortcuts use Insert, Home, Page Up, Delete, End, and Page Down.

## Create a local orientation diagnostic log

Diagnostic logging is disabled by default. To record keyboard routing and camera state locally:

```powershell
.\MeshMill.exe --diagnostic-log ".\orientation-session.jsonl" "C:\path\mesh.stl"
```

The log may contain the opened file path. Review and redact it before sharing. Mesh geometry is not
written to the log.

## Report a problem

Include the MeshMill version, Windows version, GPU model, mesh triangle count, exact action
sequence, and whether the installer or portable package was used. Use the redistributable sample
mesh when possible. Do not attach private scans or diagnostic logs without reviewing them first.
