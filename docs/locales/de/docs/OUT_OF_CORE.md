# Out-of-Core-Mesh-Architektur

Der aktuelle Schutz für große Dateien von MeshMill schätzt den Arbeitsspeicher, bevor ein vollständiger Speicherplatz zugewiesen wird
Netz. Dateien, die das konfigurierte Budget überschreiten, können als begrenzte Navigationsübersichten geöffnet werden. Ein
Bei der Übersicht handelt es sich um abgetastete Geometrie, die sichtbar als solche gekennzeichnet ist und nicht als solche bearbeitet oder exportiert werden kann
obwohl es die vollständige Quelle wäre.

Echte zoomabhängige Details erfordern einen dauerhaften räumlichen Index. Das Design unten definiert dies
nächste Umsetzungsphase.

## Indexformat

Jedes Quellnetz erhält ein versioniertes `.meshmill-index`-Verzeichnis mit:

- `manifest.json`, mit Quellgröße, Änderungszeit, abgetasteten Inhalts-Hashes, Grenzen,
  Dreiecksanzahl, Indexversion, Koordinatengenauigkeit und Ebenenbeschreibungen;
- räumliche Kacheln, die durch Octree-Ebene und Morton-Code adressiert werden;
- ein grobes Anzeigenetz für jede besetzte übergeordnete Kachel;
- Dreiecksaufzeichnungen in voller Auflösung in Blattkacheln; Und
- Grenzbesitz und Überlappungsmetadaten, die während regionaler Operationen und Montage verwendet werden.

Bei der Indexerstellung wird die Quelle nacheinander in begrenzten Blöcken gelesen. Es schreibt temporäre Kachelläufe und
Veröffentlicht das Manifest atomar, nachdem jede erforderliche Datei die Validierung bestanden hat. Eine unterbrochene bzw
Veralteter Index wird anhand seines Manifests erkannt und kann fortgesetzt oder neu erstellt werden, ohne den vollständigen Index zu öffnen
Mesh im Speicher.

## Viewport-Streaming

Das Ansichtsfenster wählt Kacheln mithilfe des Kamerakegelstumpfs und des Bildschirmbereichsfehlers aus. Grobe übergeordnete Kacheln sind
zuerst angezeigt. Sichtbare untergeordnete Kacheln ersetzen sie, wenn sich die Kamera nähert, außerhalb des Bildschirms und
Schonende Fliesen bleiben grob. RAM und VRAM verfügen über unabhängige Budgets und werden am längsten nicht verwendet
Caches. Durch die Freigabe von Details wird niemals die grobe Gesamtobjektdarstellung freigegeben.

Der Scheduler zeichnet die folgenden Kachelzustände auf: Warteschlange, Lesen, Verarbeiten, Hochladen, Resident, Fehlgeschlagen,
und abgesagt. Das Ansichtsfenster kann Würfel nach Zustand einfärben und jeden Würfel proportional zu seinem Zustand füllen
Fortschritt. Beim Abbruch werden Teilergebnisse entfernt und die letzte vollständige Darstellung bleibt aktiv.

## Verarbeitung und Kapazität

Eine lokale Arbeitseinheit ist eine Kachel plus die für ihren Betrieb erforderliche deterministische Überlappung. Parallelität
wird durch den aktuell verfügbaren RAM, den konfigurierten Speicherprozentsatz, die Anzahl der logischen Prozessoren usw. begrenzt
gemessene Arbeitseinheitsgröße. GPU-Upload und -Anzeige haben ein separates VRAM-Budget. Parallel gemeldet
Die Kapazität ist eine Schätzung, bis repräsentative Kacheln gemessen wurden.

Für jedes Grenzelement behält der Betrieb einen Eigentümer. Die Versammlung bestätigt gemeinsame Grenzen,
Entfernt Duplikate, überprüft Zählungen und Grenzen und zeichnet die genauen verwendeten Parameter auf. Die gleiche Arbeit
Einheit und Ergebnisformat können später über verteilte Syntheseknoten hinweg geplant werden.

## Sicherheitsregeln

- Ein globales Beispiel wird als Übersicht und nicht als Detailansicht des Ansichtsfensters in voller Auflösung bezeichnet.
- Eine Übersicht kann das vollständige Quellnetz nicht überschreiben oder exportieren.
- Vollauslastungsanfragen, die das aktuelle Budget überschreiten, erfordern eine explizite Auswahl.
- Indexgenerierung, Kachelbearbeitung und Montage bleiben abbrechbar und bewahren das bisherige
  vollständiger Zustand.
- Kapazitätswerte sind Schätzungen und geben an, ob sie den aktuellen Motor beschreiben oder geplant sind
  parallele Fliesenausführung.
