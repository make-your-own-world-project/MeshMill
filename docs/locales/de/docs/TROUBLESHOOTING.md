# Fehlerbehebung

## Windows blockiert den Download

Nicht signierte Community-Builds können Microsoft Defender SmartScreen auslösen. Vergleichen Sie die heruntergeladenen
SHA-256-Hash der Datei mit `SHA256SUMS.txt` aus derselben GitHub-Version. Signierte Veröffentlichungen identifizieren
ihren Herausgeber in den Dateieigenschaften Windows.

## Der tragbare Build startet nicht

Extrahieren Sie die vollständige ZIP-Datei, bevor Sie `MeshMill.exe` ausführen. Als nächstes muss das Verzeichnis `_internal` verbleiben
auf beide ausführbaren Dateien. Führen Sie die ausführbare Datei nicht im ZIP-Viewer aus.

## Als Übersicht öffnet sich ein großes STL

Der geschätzte Arbeitssatz überschreitet das Speicherbudget in den Einstellungen. Der Übersichtsmodus ist absichtlich
schreibgeschützt. Erhöhen Sie das Budget nur, wenn die Maschine über genügend verfügbaren Speicher verfügt, oder reduzieren Sie das Budget
Netz, bevor Sie es zur Bearbeitung öffnen.

## Eine Standardansicht wurde nicht gespeichert

Drücken Sie die Tastenkombination „Strg-geänderte Ansicht“ und wählen Sie dann **Speichern** oder drücken Sie zur Bestätigung die Eingabetaste
Dialog. Durch das Speichern einer Ansicht wird auch das Gegenteil aktualisiert. Die Statuszeile meldet die gespeicherte Ansicht.

## Navigationsverknüpfungen reagieren nicht

Schließen Sie zunächst alle modalen Dialoge. Überprüfen Sie die Verknüpfungen in den Einstellungen oder setzen Sie sie zurück, wenn sie angepasst wurden. Die
Die Standardverknüpfungen für die Ansicht verwenden „Einfügen“, „Startseite“, „Bild nach oben“, „Löschen“, „Ende“ und „Bild nach unten“.

## Erstellen Sie ein Diagnoseprotokoll für die lokale Ausrichtung

Die Diagnoseprotokollierung ist standardmäßig deaktiviert. So zeichnen Sie Tastaturrouting und Kamerastatus lokal auf:

```powershell
.\MeshMill.exe --diagnostic-log ".\orientation-session.jsonl" "C:\path\mesh.stl"
```

Das Protokoll enthält möglicherweise den Pfad der geöffneten Datei. Überprüfen und redigieren Sie es, bevor Sie es teilen. Die Netzgeometrie ist nicht vorhanden
ins Protokoll geschrieben.

## Melden Sie ein Problem

Beziehen Sie die MeshMill-Version, die Windows-Version, das GPU-Modell, die Anzahl der Netzdreiecke und die genaue Aktion ein
Reihenfolge und ob das Installationsprogramm oder das tragbare Paket verwendet wurde. Verwenden Sie das weiterverteilbare Muster
Mesh, wenn möglich. Hängen Sie keine privaten Scans oder Diagnoseprotokolle an, ohne sie vorher überprüft zu haben.
