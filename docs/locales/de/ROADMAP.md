# MeshMill-Roadmap

## Plattformunterstützung

Windows ist die erste paketierte Plattform. Die Anwendungsarchitektur und die Mesh-Formate sind
plattformübergreifend; zukünftige Releases sollen native Linux- und macOS-Pakete hinzufügen. Die Arbeiten an der Plattform
umfassen Paketierung, Anwendungsintegration, Hardware-Metriken, Dateisystemverhalten sowie automatisierte
Release-Tests, wobei die Projekt- und STL-Workflows auf allen unterstützten Systemen beibehalten werden.

- Validieren Sie das Linux x86-64-Vorschaupaket für alle Distributionen, Desktop-Umgebungen und Displays
  Server und GPU-Treiber, bevor Sie es auf stabil hochstufen.
- Validieren Sie die macOS Apple Silicon- und x86-64-Vorschaupakete auf echter Hardware und fügen Sie dann Developer hinzu
  Unterzeichnung und notarielle Beglaubigung des Personalausweises vor der Beförderung zum Stall.
- Hinzufügen plattformnativer Anbieter für CPU-, Speicher- und GPU-Metriken hinter einer gemeinsamen Schnittstelle.
- Gewährleistung der Portabilität von gespeicherten Einstellungen, Tastaturbelegungen, Befehlszeilenverhalten und Projektdaten.

Diese Roadmap dokumentiert geplante Arbeiten. Sie beschreibt keine Funktionen des aktuellen Releases.

## Umfang

MeshMill verwaltet Geometrie, Netzdichte, Punktdichte, Optimierung, Bereinigung, Validierung und STL.
Austauschen, sodass große oder umfangreiche Mesh-Dateien in nachgelagerten Bearbeitungsworkflows nützlich bleiben.

Universelle Modellierung, Bildhauerei, Malerei, Animation, Rendering, Szenenkomposition, Materialien,
Rigging und andere Content-Erstellungssysteme fallen nicht in diese Roadmap. Es gilt die verteilte Synthese
zu den Mesh-Management-Operationen von MeshMill und erweitert das Produkt nicht zu einem allgemeinen Editor.

## Referenzgeometrie

Das gebündelte Verbundnetz ist die gemeinsame Entwicklungseinrichtung für aktuelle Algorithmen und Roadmaps
Arbeit. Seine absichtlich redundanten Schichten und die ungleichmäßige Dichte ermöglichen wiederholbare Vergleiche
Reduktionsqualität, Dichteanalyse, Überlappungsbehandlung, regionale Operationen, Out-of-Core-Verarbeitung,
und zukünftige Synthese. Roadmap-Implementierungen sollten Ergebnisse für diese Vorrichtung und klein melden
speziell entwickelte Regressionsnetze, anstatt das Verhalten nur für ein Modell zu optimieren.

## Multi-STL-Arbeitsbereiche und statistische Synthese

Ein Arbeitsbereich sollte mehrere STL-Eingaben als separate, unabhängig sichtbare Quellobjekte akzeptieren.
MeshMill sollte diese Quellen ausrichten, ihre geometrische Übereinstimmung messen und eine verwendbare synthetisieren
Netz ohne Beibehaltung doppelter Innenflächen oder wiederholter Überlappungsgeometrie.

Geplantes Verhalten:

- mehrere STL-Quellen in einem Arbeitsbereich hinzufügen, entfernen, ausblenden, isolieren, neu anordnen und prüfen;
- Behalten Sie die Identität der Quelle, Einheiten, Transformationen, Grenzen, Auflösung und Operationsverlauf bei;
- Bereitstellung einer automatischen Registrierung mit manuellen Ausrichtungskontrollen und messbarer Passqualität;
- Partitionieren Sie Quellen vor dem Vergleich in räumliche Regionen, sodass große Eingaben begrenzt bleiben.
- Analysieren Sie die Belegung, den Abstand zur nächsten Oberfläche, die normale Übereinstimmung, die lokale Dichte, die Varianz usw
  Beobachtungsanzahl über überlappende Regionen hinweg;
- klassifizieren Sie passende Oberflächen, widersprüchliche Oberflächen, Scan-Rauschen, Lücken und einzigartige Geometrie;
- Konsolidieren Sie statistisch übereinstimmende Oberflächen zu einer repräsentativen Oberfläche mit aufgezeichneten Daten
  Vertrauen, anstatt doppelte Dreiecke zu stapeln;
- Entfernen Sie eingeschlossene, zusammenfallende und gemeinsam genutzte Geometrie, die keine äußeren Formdetails beisteuert.
- Behalten Sie nicht überlappende Quellgeometrie bei und legen Sie mehrdeutige Bereiche zur visuellen Überprüfung offen.
- Erlauben Sie eine Gewichtung pro Quelle und pro Region, wenn ein Scan sauberer oder detaillierter ist.
- Validierung von Wasserdichtigkeit, Grenzen, Normalen, Abmessungen und Topologie nach der Synthese;
- Zeichnen Sie die Herkunft der Quelle und die Syntheseparameter auf, damit das kombinierte Netz reproduzierbar ist.
- Vorschau der erwarteten Dreiecksanzahl, der Grenzen, der entfernten Überlappung und der Konfidenzverteilung
  Festschreiben des synthetisierten Ergebnisses.

Dieser Workflow sollte denselben räumlichen Out-of-Core-Index und dasselbe Arbeitseinheitsmodell verwenden, das für große Unternehmen geplant ist
Maschen. Statistischer Vergleich und Überlappungskonsolidierung sollten auch lokal verteilbar sein
oder entfernte MeshMill-Knoten.

## Verteilte Synthese

Ein MeshMill-Cluster sollte mehrere Knoten koordinieren, die parallel über mehrere Knoten hinweg arbeiten
Arbeitsplätze. Ein Knoten kann eine zugewiesene Region prüfen, auswählen, reduzieren, validieren, reparieren oder kombinieren
Arbeitseinheit. Beiträge bleiben unabhängig versioniert, bis sie überprüft und eingearbeitet werden
in eine Shared-Object-Version umwandeln.

Das System sollte Folgendes unterstützen:

- gleichzeitige Beiträge von mehreren Betreibern und automatisierten Knoten;
- deterministische Eingaben, Parameter, Abhängigkeiten und Ausgaben für Arbeitseinheiten;
- fähigkeitsbewusste Planung basierend auf CPU, GPU, Speicher, Algorithmen und aktueller Auslastung;
- Abhängigkeitsbewusste Partitionierung von Netzen, Regionen, Validierungsdurchgängen und Synthesestufen;
- dauerhafte Warteschlangen mit Pause, Wiederaufnahme, Abbruch, Wiederholung, Neuzuweisung und Fehlerbehebung;
- inhaltsadressierte Artefakte und Integritätsprüfungen zwischen Knoten;
- reproduzierbare Synthese aus einem aufgezeichneten Satz akzeptierter Beitragsversionen;
- Offline- oder zeitweise verbundene Workstations, die später synchronisiert werden können;
- Local-First-Betrieb mit expliziter Kontrolle über teilnehmende Knoten und gemeinsame Projektdaten.

## Versionierte Zusammenarbeit

Jeder Beitrag sollte die Version seines übergeordneten Objekts, die ausgewählte Region oder Arbeitseinheit, den Vorgang usw. aufzeichnen.
Parameter, Knotenidentität, Zeitstempel, Abhängigkeiten, Validierungsergebnisse und Ausgabeprüfsumme.

Geplantes Kollaborationsverhalten:

- Projekte enthalten Objekte, Zweige, Prüfpunkte, Beiträge und synthetisierte Versionen;
- Mitwirkende können mit derselben übergeordneten Version arbeiten, ohne sich gegenseitig zu überschreiben.
- sich nicht überschneidende Beiträge können nach der Validierung automatisch zusammengeführt werden;
- überlappende Geometrie oder inkompatible Abhängigkeiten erzeugen einen expliziten Konflikt;
- Konflikte bieten visuellen Vergleich, Auswahl auf Regionsebene, Rebase, Wiederholung und manuelle Lösung;
- Zu den Überprüfungsstatus gehören „Ausstehend“, „Angenommen“, „Abgelehnt“, „Ersetzt“, „Konflikt“ und „Inkorporiert“.
- Das endgültige Synthesemanifest identifiziert jeden integrierten Beitrag und jede Abhängigkeit.

## Koordinations-Benutzeroberfläche

Die Desktop-Anwendung sollte verteilte Arbeit verwalten, ohne dass eine separate Befehlszeile erforderlich ist
oder Serveradministrations-Workflow. Zu den geplanten Ansichten gehören:

- **Projekte:** Objekte, Zweige, Versionen, Mitwirkende und Synthesestatus.
- **Cluster:** verbundene Arbeitsstationen und Knoten, Funktionen, Zustand, Auslastung und aktuelle Zuweisung.
- **Warteschlange:** ausstehende, aktive, pausierte, blockierte, fehlgeschlagene und abgeschlossene Arbeitseinheiten.
- **Beiträge:** Autor, Knoten, übergeordnete Version, betroffene Region, Parameter, Prüfungen und Überprüfungsstatus.
- **Vergleichen:** synchronisierte 3D-Ansichten, Geometrieunterschiede, Metriken und Grenzprüfung.
- **Konflikte:** überlappende Regionen, Abhängigkeitskonflikte, Lösungsoptionen und Validierungsergebnisse.
- **Synthese:** Abhängigkeitsdiagramm, aggregierter Fortschritt, ausgewählte Beitragsversionen und endgültige Ausgabe.
- **Verlauf:** Verzweigungsdiagramm, Prüfpunkte, Zusammenführungen, synthetisierte Versionen und Reproduzierbarkeitsmanifeste.

Das Ansichtsfenster sollte Eigentümer, zugewiesene Regionen, abgeschlossene Arbeiten, ausstehende Änderungen, Konflikte usw. anzeigen.
und Versionsunterschiede, ohne das zugrunde liegende Netz zu verändern.

## Koordination und Transport

In der ersten Entwurfsphase sollten Protokollgrenzen definiert werden, bevor ein Transport ausgewählt wird. Das Protokoll
sollte Koordinationsmetadaten von großen Mesh-Artefakten trennen, eine wiederaufnehmbare Übertragung unterstützen und
bleiben in einem lokalen Netzwerk ohne externes Konto oder gehosteten Dienst nutzbar.

Erforderliche Koordinationskonzepte:

- Wahl des Koordinators oder eines explizit ausgewählten Koordinators;
- Knotenerkennung und manuelle Knotenregistrierung;
- authentifizierte Sitzungen und projektbezogene Autorisierung;
- Mietverträge und Heartbeats für Arbeitseigentum;
- idempotente Arbeitseinreichung und Ergebnisakzeptanz;
- Versionsaushandlung zwischen verschiedenen MeshMill-Releases;
- strukturierte Ereignisse für Fortschritt, Protokolle, Validierung, Fehler und Wiederholungsversuche;
- Wiederherstellung nach einer Koordinator-, Workstation-, Netzwerk- oder Knotenunterbrechung.

## Lieferphasen

### Phase 0: Verarbeitung großer Netze außerhalb des Kerns

Der Index, das Streaming, der Cache, die Arbeitseinheit und der Sicherheitsvertrag sind in dokumentiert
[`docs/OUT_OF_CORE.md`](docs/OUT_OF_CORE.md).

- Schätzen Sie die Anzahl der Dreiecke und den Arbeitsspeicher, bevor Sie das gesamte Netz zuweisen.
- Öffnen Sie übergroße binäre STL-Dateien als begrenzte, gleichmäßig abgetastete Navigationsübersichten.
- Partitionieren Sie vollständig aufgelöste Geometrie in räumliche Würfel mit deterministischen Überlappungsgrenzen.
- Lesen, analysieren und optimieren Sie gleichzeitig unabhängige Cubes innerhalb der CPU- und Speichergrenzen.
- Benchmarken Sie GPU-Computing-Implementierungen für Reduktionsstufen wie Fehlerbewertung und Kandidaten
  Scoring, räumliche Abfragen und unabhängige Arbeitseinheitenverarbeitung. Entladen Sie eine Stufe nur, wenn sie vorhanden ist
  Bietet einen messbaren End-to-End-Geschwindigkeits- oder Speichervorteil, ohne Determinismus und Mesh zu reduzieren
  Qualität, Topologiegarantien oder Kompatibilität mit Systemen, denen eine geeignete GPU fehlt.
- Streamen Sie Ansichtsfensterebenen von grob nach fein, anstatt das gesamte Netz im Speicher zu benötigen.
- Zeichnen Sie den Cube-Status direkt im Ansichtsfenster ein: in der Warteschlange, gelesen, verarbeitet, abgeschlossen und fehlgeschlagen.
- Zeigen Sie den Fortschritt pro Würfel an, indem Sie jeden Würfel füllen, und behalten Sie eine übergeordnete Gesamtansicht des Objekts bei.
- Stellen Sie verarbeitete Würfel mit Grenzvalidierung, Duplikatentfernung und reproduzierbaren Einstellungen zusammen.
- Erweitern Sie den lokalen Cube-Scheduler in späteren Phasen auf verteilte Synthesearbeitseinheiten.

### Phase 1: versioniertes lokales Fundament

- Definieren Sie Objekt-, Operations-, Beitrags-, Zweig- und Manifestformate.
- Fügen Sie Multi-STL-Arbeitsbereiche mit Sichtbarkeit, Transformationen, Metadaten und Herkunft pro Quelle hinzu.
- Fügen Sie Metriken für die Registrierungsqualität und die Klassifizierung räumlicher Überlappungen hinzu.
- Synthetisieren Sie statistisch übereinstimmende Flächen und entfernen Sie gleichzeitig doppelte und eingeschlossene Geometrie.
- Fügen Sie eine visuelle Überprüfung auf Konflikte, Lücken, Vertrauen und Geometrie hinzu, die nur für eine Quelle gelten.
- Behalten Sie den lokalen Verlauf über alle Anwendungssitzungen hinweg bei.
- Fügen Sie visuelle Netz- und Regionsvergleiche hinzu.
- Machen Sie Vorgänge deterministisch und unabhängig reproduzierbar.

### Phase 2: Koordinierte lokale Knoten

- Führen Sie Worker-Knoten auf einer Workstation aus.
- Fügen Sie Warteschlangen, Fähigkeitsberichte, Arbeitszuweisungen und Stornierungen hinzu.
- Knoten- und Arbeitseinheitsstatus in der MeshMill-Benutzeroberfläche anzeigen.
- Validieren Sie die Partitionierung und die Ergebnisassemblierung lokal.

### Phase 3: Multi-Workstation-Synthese

- Fügen Sie authentifizierte LAN-Erkennung und -Registrierung hinzu.
- Übertragen Sie inhaltsbezogene Arbeitseingaben und -ergebnisse mit Lebenslaufunterstützung.
- Koordinieren Sie die gleichzeitige Arbeit über mehrere Workstations hinweg.
- Stellen Sie Zuweisungen nach einem Knoten- oder Netzwerkausfall wieder her.

### Phase 4: kollaborative Versionierung

- Fügen Sie Mitwirkende, Zweige, Überprüfungsstatus und Berechtigungen hinzu.
- Nicht überlappende Beiträge zusammenführen.
- Erkennen und lösen Sie Überschneidungs- oder Abhängigkeitskonflikte.
- Synthetisieren Sie ausgewählte Beiträge zu einer reproduzierbaren Objektversion.

### Phase 5: Produktionshärtung

- Fügen Sie Protokollkompatibilitätstests und die Handhabung gemischter Versionen hinzu.
- Fügen Sie Audit-, Integritäts-, Korruptions-, Unterbrechungs- und Wiederherstellungstests hinzu.
- Benchmarking-, Partitionierungs-, Übertragungs-, Zusammenführungs- und Syntheseleistung.
- Bereitstellung, Sicherung, Migration und Wiederherstellung von Dokumenten.
