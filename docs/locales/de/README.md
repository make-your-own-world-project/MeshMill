# MeshMill

![MeshMill schattierte Ansicht](../../images/meshmill-shaded.png)

MeshMill ist eine spezialisierte Desktop-Anwendung, um sehr große, hochdichte oder komplexe Mesh-Geometrien
handhabbar zu machen. Sie bietet Funktionen zur schnellen Überprüfung, Dichteanalyse, bereichsweisen Auswahl, zum Zuschneiden, Löschen
und zur kontrollierten Mesh-Reduzierung – ganz ohne Benutzerkonto oder das Hochladen von Geometriedaten.

MeshMill verarbeitet Meshes aus 3D-Scannern, CAD- und Modellierungsexporten, Rekonstruktions-Pipelines,
generierter Geometrie und anderen STL-Quellen. Es bereitet Geometrien für nachgelagerte Editoren,
Fertigungswerkzeuge und weitere Mesh-Workflows vor. Allgemeine Modellierung, Sculpting, Animation,
Materialien und Szenenerstellung gehören nicht zum Funktionsumfang.

## Download

Laden Sie eine dieser Dateien von [GitHub Releases](../../releases) herunter:

- `MeshMill-<version>-windows-x64-setup.exe`: Installer für den aktuellen Benutzer mit Startmenü-Eintrag und optionalen
  Desktop-Verknüpfungen.
- `MeshMill-<version>-windows-x64-portable.zip`: Portable Anwendung. Entpacken Sie das gesamte Archiv,
  und starten Sie anschließend `MeshMill.exe`.

Beide Pakete enthalten die Laufzeitumgebung für die Anwendung. Endbenutzer installieren keine Python-, Node.js- oder
Abhängigkeiten. Die erste Version unterstützt Windows 10 und Windows 11 auf x64-Hardware. Linux- und
macOS-Pakete sind geplant; die Produkt- und Dateiformate sind nicht spezifisch für Windows.

Nicht signierte Community-Builds lösen möglicherweise eine Windows-SmartScreen-Warnung aus. Prüfsummen der Versionen sind
in `SHA256SUMS.txt` neben der jeweiligen Version aufgeführt.

## Schnellstart

1. Öffnen Sie eine STL.
2. Überprüfen Sie sie im Anzeigemodus „Schattiert“, „Dichte“, „Drahtgitter“ oder „Scheitelpunkte“.
3. Wählen Sie eine Qualitätsstufe, einen Algorithmus und eine Ziel-Dreiecksanzahl.
4. Wählen Sie **Optimieren**, um ein Ergebnis zu berechnen.
5. Vergleichen Sie das ursprüngliche und das optimierte Mesh und wählen Sie dann **Anwenden**, um den Vorgang zu übernehmen.
6. Wählen Sie **Aktuellen Zustand speichern** oder drücken Sie `Ctrl+S`.

MeshMill startet die Optimierung niemals allein aufgrund einer Änderung an einer Datei oder Einstellung.

## Funktionen

- Eingabe im Binär- und ASCII-Format, Ausgabe im Binärformat (STL) (STL)
- Dichteausgeglichene, form- und topologieerhaltende Reduzierung (Fast QEM)
- Anzeigemodi: Schattiert, Dichte, Drahtgitter und Eckpunkte
- Automatische Zielvorgaben basierend auf der Geometrie statt auf einer festen Obergrenze für die Anzahl der Dreiecke
- Polygon-Auswahl mit additiver Auswahl mehrerer Bereiche
- Zuschneiden, Löschen oder Optimieren nur des ausgewählten Bereichs
- Vergleich zwischen zwischengespeichertem Original-, vorherigem und aktuellem Mesh
- Rückgängigmachen und Wiederherstellen von bestätigten Geometrieänderungen
- Abweichung der Abmessungen, Reduzierungsprozentsatz und geschätzte Ausgabegröße
- Anzeigeeinheiten: Millimeter, Zentimeter, Meter, Zoll und Fuß
- Metriken zu Modell, Speicher, Ausgabe und Geometrieaktivität (CPU) (GPU)
- Begrenztes Laden einer Übersicht, wenn das Eingabemodell das konfigurierte Speicherbudget überschreitet (STL)
- Anwendungen mit grafischer Benutzeroberfläche (GUI) und Befehlszeilenschnittstelle
- Lokale Verarbeitung ohne Abhängigkeit von Benutzerkonten, Telemetrie, Uploads oder Cloud-Diensten

![Anzeige der Dichte](../../images/meshmill-density.png) (MeshMill)

## Ansichtssteuerung

| Eingabe | Aktion |
| --- | --- |
| Mittlere Maustaste (ziehen) | Orbit (um die Ansicht drehen) |
| Umschalt + mittlere Maustaste (ziehen) | Verschieben (Pan) |
| Mausrad | Auf den Mauszeiger zu zoomen |
| Strg + Mausrad | Im oder gegen den Uhrzeigersinn drehen |
| Pfeiltasten | Orbit um den Ansichtsmittelpunkt |
| Strg + Pfeiltasten | Verschieben (Pan) |
| Strg + Umschalt + Oben/Unten | Zoomen |
| Strg + Umschalt + Links/Rechts | Rolle |
| `F1` / `F2` / `F3` / `F4` | Schattiert / Dichte / Drahtmodell / Eckpunkte |
| Rechte Maustaste gedrückt halten | Lupe |
| Umschalt + Linksklick | Linealpunkte hinzufügen oder entfernen |
| Strg + linke Maustaste | ziehen Zeichnen Sie ein Auswahlpolygon |
| `Ctrl+C` | Fügen Sie das Polygon zur gespeicherten Auswahl hinzu |
| `Ctrl+X` | Auf die Auswahl zuschneiden |
| `Ctrl+Space` | Optimieren Sie die Auswahl |
| `Delete` | Auswahl löschen |
| `Escape` | Löschen Sie die aktive Auswahl oder das aktive Lineal |
| `Ctrl+Z` / `Ctrl+Y` | Rückgängig machen/Wiederholen |
| `Ctrl+S` | Speichern Sie den aktuellen Mesh-Status |

Die Standardansichtstasten folgen dem Navigationsblock mit sechs Tasten:

| Schlüssel | Anzeigen | Strg + Taste |
| --- | --- | --- |
| `Insert` | Links | Stellen Sie die aktuelle Ausrichtung auf Links | ein
| `Home` | Vorne | Legen Sie die aktuelle Ausrichtung auf „Vorne |“ fest
| `Page Up` | Richtig | Legen Sie die aktuelle Ausrichtung auf „Rechts |“ fest
| `Delete` | Oben, wenn keine Auswahl vorhanden ist | Stellen Sie die aktuelle Ausrichtung auf Oben | ein
| `End` | Zurück | Legen Sie die aktuelle Ausrichtung auf „Zurück |“ fest
| `Page Down` | Unten | Legen Sie die aktuelle Ausrichtung auf „Unten |“ fest

Durch das Speichern einer Ansicht wird auch die Gegenansicht aktualisiert. Links und rechts, vorne und hinten und oben und unten
bleiben gepaart. Im Bestätigungsdialog ist **Speichern** die Standardaktion, daher speichert Enter die Aktion
Orientierung. Die Vorderseite wird sowohl in der Ansicht von oben als auch von unten oben angezeigt.

Verknüpfungen können in den Einstellungen geändert oder zurückgesetzt werden.

## Auswahlworkflow

Halten Sie die Strg-Taste gedrückt und ziehen Sie mit der linken Maustaste, um ein Polygon zu zeichnen. Ziehen Sie an den Ecken, um die Form zu ändern, und klicken Sie mit der linken Maustaste auf eine Kante, um eine hinzuzufügen
Punkt, oder klicken Sie mit der rechten Maustaste auf eine Kante, um eine zu entfernen. Fügen Sie weitere Regionen mit `Ctrl+C` hinzu. Das Bewegen der Kamera wird ausgeblendet
das Bildschirmraum-Polygon unter Beibehaltung der ausgewählten Geometrie.

Die Optimierung mit einer aktiven Auswahl wirkt sich nur auf diese Auswahl aus. Das Ergebnis bleibt vorläufig
bis **Anwenden** ausgewählt ist. **Abbrechen** verwirft das vorläufige Ergebnis und behält die Auswahl bei
Es kann eine andere Konfiguration ausprobiert werden. Zuschneide- und Löschvorgänge werden zu normalen, rückgängig zu machenden Netzbearbeitungen.

## Große Maschen

Vor der Zuweisung eines binären STL vergleicht MeshMill seinen geschätzten Arbeitsspeicher mit dem konfigurierten
Speicherbudget. Eine Datei oberhalb des Budgets wird als begrenzte, schreibgeschützte Übersicht geöffnet. Die Übersichtsberichte
die vollständige Anzahl der Quelldreiecke, deaktiviert jedoch die Bearbeitung und den Export, da es sich um ein Beispiel und nicht um die vollständige handelt
Objekt. Geplant ist eine indizierte, zoomabhängige Out-of-Core-Verarbeitung
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md).

## Befehlszeile

`MeshMillCLI.exe` ist in beiden Release-Paketen enthalten:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

Führen Sie `.\MeshMillCLI.exe --help` für alle Optionen aus. MeshMill weigert sich, seine Eingabedatei zu überschreiben.

## Beispielgeometrie

Es stehen zwei Versionen des Entwicklungsbeispiels zur Verfügung. Die Probe ist ein Verbundnetz mit
absichtliche Schichten redundanter Geometrie und unterschiedlicher Dichte. Es gibt Menschen ohne Scanner eine
realistische Vorrichtung zum Vergleichen von Algorithmen, Überprüfen der Dichte, Ausführen regionaler Operationen,
und Entwicklung von Roadmap-Funktionen. MeshMill erfordert keine gescannte Eingabe.

| Datei | Dreiecke | Größe | Lieferung | Am besten für |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249.999 | 11,9 MiB | Normales Git | Schnelle Auswertung, CI und Erlernen der Steuerung |
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4.126.315 | 196,8 MiB | Git LFS | Testen der dichten Quellgeometrie und der Leistung großer Netze |

Das kleinere Beispiel wird mit jedem normalen Klon heruntergeladen. Das unberührte Original ist optional und
wird über Git LFS verwaltet, sodass der normale Repository-Verlauf nicht vergrößert wird. GitHub Desktop beinhaltet
Git LFS. Befehlszeilenbenutzer können Git LFS installieren und Folgendes ausführen:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

Mit Tags versehene Veröffentlichungen veröffentlichen auch das Original STL als direkten Download für Leute, die Git nicht verwenden.
Siehe [`samples/README.md`](../../../samples/README.md) für Herkunft, Abmessungen und Prüfsummen.

Algorithmus-Mitwirkende sollten auch die lesen
[Anleitung zum Testen von Algorithmen](docs/ALGORITHM_TESTING.md), bevor Sie die Reduzierung vergleichen oder ändern
Verhalten.

## STL-Einheiten

STL kodiert keine Einheit. Durch Ändern der Modelleinheiten werden Beschriftungen und Maße ohne Skalierung geändert
die gespeicherten Koordinaten. Wählen Sie die Einheit aus, die die Quellgeometrie beschreibt.

## Privatsphäre

MeshMill liest und schreibt lokale Dateien. Es enthält kein Konto, Telemetrie, Upload, Werbung oder
Cloud-Verarbeitungsfunktion. Die aktuelle Implementierung der GPU-Metriken nutzt die lokale Windows-Leistung
Zähler. Für Linux und macOS sind gleichwertige native Metrikanbieter geplant.

Zur diagnostischen Fehlerbehebung können Entwickler die GUI mit starten
`--diagnostic-log <local-file.jsonl>`. Das Protokoll zeichnet die Eingabeweiterleitung und den Kamerastatus lokal auf und ist
bei normalem Gebrauch deaktiviert.

## Entwicklung und Veröffentlichung

- [Beitrag](CONTRIBUTING.md)
- [Freigabeprozess](RELEASING.md)
- [Roadmap](ROADMAP.md)
- [Fehlerbehebung](docs/TROUBLESHOOTING.md)
- [Hinweise Dritter](THIRD_PARTY_NOTICES.md)

## Unterstützt MeshMill

MeshMill wird unabhängig entwickelt und gepflegt. Lesen
[warum die Unterstützung dieser Arbeit wichtig ist](SUPPORT.md), oder unterstützen Sie die weitere Entwicklung durch
[Kauf mir einen Kaffee](https://buymeacoffee.com/tednv).

MeshMill ist unter der GNU General Public License, Version 3 oder höher, lizenziert. Siehe
[`LICENSE`](../../../LICENSE).
