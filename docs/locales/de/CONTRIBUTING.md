# Mitwirken

Beiträge über Issues und Pull Requests sind willkommen.

## Projektumfang

Mit MeshMill können übergroße, dichte oder schwierig zu vernetzende Dateien für die nachgelagerte Bearbeitung verwaltet werden
Produktionsabläufe. Beiträge sollen die Geometrieinspektion, Netz- und Punktdichte verbessern
Verwaltung, Optimierung, Auswahl, Zuschneiden, Bereinigung, Validierung, STL-Austausch, Leistung,
oder die Koordinierung dieser Operationen.

Das Projekt umfasst keine allgemeine Modellierung, Bildhauerei, Malerei, Animation, Rendering,
Szenenkomposition, Materialien, Rigging oder andere Systeme zur Inhaltserstellung. Vorschläge, die einführen
Diese Funktionen liegen außerhalb des Projektumfangs.

Neue Funktionen sollen dafür sorgen, dass die Anwendung konzentriert bleibt und direkte Arbeitsabläufe erhalten bleiben, die zur Quelle werden
Geometrie in überschaubare Netze umwandeln und vermeiden, unterstützende Steuerelemente in eine allgemeine Bearbeitung umzuwandeln
Umgebung.

## Lokalisierung

Englischer UI-Quelltext wird in `locales/en-US.json` gespeichert. Gebietsschema-Metadaten werden in gespeichert
`locales/manifest.json`. Übersetzte UI-Kataloge verwenden dieselben stabilen Schlüssel und den gleichen Dateinamen
`<locale>.json`. In der übersetzten Dokumentation wird der entsprechende Root-Dateiname verwendet
`docs/locales/<locale>/`.

Übersetzungen werden zunächst mit externen maschinellen Übersetzungsdiensten erstellt und erhalten
automatisierte Strukturvalidierung. Dieser Prozess kann keine natürliche, technisch präzise oder einwandfreie Qualität gewährleisten
kontextuell korrekte Sprache. Muttersprachler werden ermutigt, die übersetzte Benutzeroberfläche zu überprüfen und zu korrigieren
Text und Dokumentation. Bei Übersetzungskorrekturen sollten Katalogschlüssel, Platzhalter usw. erhalten bleiben.
Befehle, Links, Messungen, Produktnamen und Markdown-Struktur.

Führen Sie nach dem Ändern von Beschriftungen, QuickInfos, Dialogen oder anderem für den Benutzer sichtbaren Text Folgendes aus:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
```

Überprüfen Sie gemeinsam Quelländerungen und neu generierte Schlüssel.

## Geometrie- und Algorithmusänderungen

Nutzen Sie die gebündelte Probengeometrie beim Ändern von Optimierung, Dichteanalyse, Auswahl, Zuschneiden usw.
Handhabung großer Dateien oder Verhalten beim Ansichtsfenstervergleich. Es enthält absichtlich redundante Schichten
und ungleichmäßige Dichte, daher sollte ein brauchbares Ergebnis die Handhabbarkeit verbessern, ohne Verzerrungen zu verbergen.
Verwerfen sinnvoller Grenzen oder stillschweigendes Entfernen von Geometrie, die ein anderer Algorithmus beibehält.

Zeichnen Sie die Eingabe, den Algorithmus, die Einstellungen, die Dreiecksanzahl, die Abmessungen, die Dimensionsabweichung, die verstrichene Zeit usw. auf.
und relevante Screenshots zum Vergleich. Testen Sie sowohl das kleinere Normal-Git-Gerät als auch, wenn das
Die Änderung betrifft große oder geschichtete Geometrien, die ursprüngliche Git LFS-Vorrichtung. Optimieren Sie keinen Algorithmus
allein zu diesem Gerät. Fügen Sie kleine synthetische Fälle für die spezifische Invariante oder das Regressionswesen hinzu
getestet.

Die Vergleichscheckliste finden Sie unter [Algorithmentests und Beitrag](docs/ALGORITHM_TESTING.md).

## Entwicklungsaufbau

1. Installieren Sie 64-Bit Python 3.12 auf Windows.
2. Erstellen und aktivieren Sie eine virtuelle Umgebung.
3. Installieren Sie `requirements-dev.txt`.
4. Führen Sie `python meshmill.py` für die GUI oder `python meshmill.py --help` für die CLI-Nutzung aus.
5. Führen Sie `python -m py_compile meshmill.py` aus, bevor Sie eine Änderung übermitteln.

Behalten Sie private Netze, generierte ausführbare Dateien, Screenshots mit privaten Informationen und lokal bei
Erstellen Sie Verzeichnisse aus Commits. Weiterverteilbare Testgeometrie gehört unter `samples/` mit
Quelle, Lizenz, Abmessungen und Generierungsmethode dokumentiert. Neue Quelldateien sollten die verwenden
SPDX-Kennung `GPL-3.0-or-later`.

Schneiden Sie jeden Dokumentations-Screenshot auf den Anwendungsinhalt MeshMill zu. Schließen Sie das nicht ein
Taskleiste, unabhängiges Fensterchrom, Benachrichtigungen, Kontodetails, private Pfade oder Hintergrund
Desktop-Inhalte.
