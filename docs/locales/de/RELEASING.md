# Veröffentlichung von MeshMill

Die stabile Release-Pipeline erstellt Windows-Artefakte auf von GitHub gehosteten Windows-Runnern. Ein separates
Der manuelle Workflow erstellt unsignierte Linux x86-64- und macOS Intel/Apple-Siliziumvorschauen auf nativer Basis
Von GitHub gehostete Läufer. Endbenutzer installieren weder Python, Node.js noch Abhängigkeiten.

Aktualisieren und validieren Sie vor dem Erstellen die Lokalisierungsquellenkataloge:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## Vor der ersten öffentlichen Veröffentlichung

1. Fertigstellen und Validieren der geplanten Anwendungs- und Dokumentationsübersetzungen.
2. Lesen Sie die GPL- und Drittanbieter-Hinweise.
3. Testen Sie die Installation, den Start, das Laden von STL, die Optimierung, den Export und die Deinstallation in einem sauberen Zustand
   Windows-Konto oder virtuelle Maschine.
4. Führen Sie CI gegen `samples/sample-scan.stl` aus. Überprüfen Sie jeden Dokumentations-Screenshot und schneiden Sie ihn aus
   die Taskleiste, Fensterrahmen, die nicht Teil von MeshMill sind, Benachrichtigungen, private Pfade, Konto
   Details und nicht dazugehörige Desktop-Inhalte vor der Veröffentlichung.
5. Konfigurieren Sie den Repository-lokalen Git-Autor mit der „No-Reply“-Adresse des GitHub-Kontos vor dem
   ersten Commit. Bestätigen Sie dies mit `git config --local --get user.email`.
6. Konfigurieren Sie optionale Authenticode-Signierungsgeheimnisse:
   - `WINDOWS_CERTIFICATE_BASE64`: Base64-codiertes PFX-Zertifikat.
   - `WINDOWS_CERTIFICATE_PASSWORD`: PFX-Passwort.

Ohne Signierungszertifikat funktionieren die generierten Dateien zwar weiterhin, aber Windows SmartScreen zeigt möglicherweise
eine Warnung vor einem unbekannten Herausgeber an. Bezeichnen Sie unsignierte Builds nicht als signiert oder vertrauenswürdig.

## Ursprünglicher Scan und Git LFS

`samples/original-scan.stl` wird über Git LFS nachverfolgt, da es das normale Limit von 100 MiB von GitHub
für Dateigrößen überschreitet. Überprüfen Sie vor dem ersten Commit Folgendes:

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

Der Filter muss `lfs` lauten und die Zeiger-Objekt-ID muss mit `samples/SHA256SUMS.txt` übereinstimmen. Der Release-
Workflow ruft LFS-Inhalte ab und veröffentlicht das ursprüngliche STL als separates Release-Asset. Die CI verwendet
das kleinere Standard-Git-Beispiel und lädt das LFS-Objekt nicht herunter.

## Testen eines Release-Builds ohne Veröffentlichung

Öffnen Sie **Actions**, wählen Sie **Release**, dann **Run workflow** und geben Sie eine numerische Version ein, wie z. B.
`0.1.0`. Ein manueller Durchlauf lädt Workflow-Artefakte zu Testzwecken hoch, erstellt jedoch kein öffentliches GitHub-
Release.

## Veröffentlichen eines Releases

Ausgehend von einem sauberen, geprüften `main`-Branch:

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

Das Tag startet den Release-Workflow. Dieser:

1. installiert die festgelegten Build-Abhängigkeiten;
2. generiert passende Windows-Versionsmetadaten;
3. erstellt die eigenständigen GUI- und CLI-Executables;
4. signiert die Executables, sofern Signier-Secrets konfiguriert sind;
5. erstellt den benutzerbezogenen Inno-Setup-Installer;
6. signiert den Installer, sofern konfiguriert;
7. erstellt das portable ZIP-Archiv sowie die SHA-256-Prüfsummendatei;
8. lädt Workflow-Artefakte hoch;
9. erstellt das GitHub-Release für das gepushte Tag.

Überprüfen Sie den Installer und das portable Archiv auf einem sauberen Windows-System, bevor Sie das Release ankündigen.
Halten Sie den Quellcode für jede verteilte Binärdatei unter demselben Release-Tag bereit.
Stellen Sie sicher, dass die Schaltfläche GitHub auf die endgültige URL des öffentlichen Repositorys verweist, bevor Sie das erste
Release mit einem Tag versehen.

## Erstellen Sie Linux- und macOS-Vorschauen

Öffnen Sie **Aktionen**, wählen Sie **Plattform-Vorschau-Builds** und wählen Sie **Workflow ausführen**. Geben Sie eine Vorschau ein
Version wie „0.2.0-preview.1“.

Lassen Sie **Eine öffentliche GitHub-Vorabversion veröffentlichen** für die erste Ausführung deaktiviert. Der Workflow erstellt und testet:

- Linux x86-64 auf Ubuntu 22.04;
- macOS x86-64 auf einem Intel-Läufer;
- macOS arm64 auf einem Apple Silicon Runner.

Laden Sie die Workflow-Artefakte herunter und überprüfen Sie deren Prüfsummen und Protokolle. Führen Sie den Workflow erneut mit aus
Die Veröffentlichung wird erst aktiviert, nachdem jeder Build-Job erfolgreich abgeschlossen wurde. Veröffentlichte macOS-Vorschauen sind Ad-hoc-signiert,
nicht von Apple notariell beglaubigt. Beschreiben Sie sie als Vorschau-Builds und verlinken Sie Tester darauf
`docs/PLATFORM_TESTING.md` und das Problemformular **Plattform-Vorschautest**.
