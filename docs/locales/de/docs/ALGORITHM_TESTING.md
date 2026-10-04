# Algorithmentests und Beitrag

MeshMill-Algorithmen sollen schwierige Geometrien beherrschbar machen und gleichzeitig ihre Auswirkungen sichtbar halten,
messbar und reversibel, bevor ein Ergebnis angewendet wird.

## Referenzvorrichtungen

Verwenden Sie beide gebündelten Versionen der zusammengesetzten Beispielgeometrie:

- `samples/sample-scan.stl` ist das kleinere Standard-Git-Gerät für die automatisierte Routineentwicklung
  Kontrollen und das Erlernen der Kontrollen.
- `samples/original-scan.stl` ist die vollständige Git LFS-Vorrichtung für das Verhalten großer Dateien, redundante Schichten,
  ungleichmäßige Dichte, Überlappung und Leistungsarbeit.

Die redundanten und dichten Bereiche sind beabsichtigte Testmerkmale. Ein Test könnte auf sie abzielen, aber
Man sollte nicht davon ausgehen, dass jede überlappende Oberfläche wegwerfbar ist. Fügen Sie kompakte synthetische Netze hinzu, wenn a
Für eine Änderung ist eine bekannte Grenze, Krümmung, Topologie, Dichte oder Überlappungsinvariante erforderlich.

## Vergleichs-Checkliste

Notieren Sie für eine Algorithmus- oder Parameteränderung Folgendes:

- MeshMill-Version oder Commit;
- Eingabegerät und Prüfsumme;
- Algorithmus, Qualitätsvoreinstellung, Ziel und erweiterte Einstellungen;
- ursprüngliche und resultierende Dreiecks- und Scheitelpunktzahlen;
- Reduktionsprozentsatz, Abmessungen und Dimensionsdrift;
- verstrichene Zeit und Spitzenspeicher, wenn die Leistung relevant ist;
- Screenshots aus denselben gespeicherten Ansichten und Anzeigemodi;
- sichtbare Grenz-, Loch-, Selbstüberschneidungs-, Überlappungs- oder Verzerrungsänderungen;
- ob das Ergebnis aus einem Gesamtnetz- oder einem Nur-Auswahl-Vorgang stammt.

Vergleichen Sie mit dem aktuellen Verhalten beim gleichen Ziel, nicht nur mit einer anderen Voreinstellung mit a
unterschiedliche Ausgangsanzahl. Überprüfen Sie ggf. die Darstellung von Schattierungen, Dichte, Drahtgitter und Scheitelpunkten.

## Akzeptanzberatung

Durch eine Optimierungsänderung sollten unerwartete Dimensionsänderungen, offensichtliche Oberflächeninversionen usw. vermieden werden.
Risse zwischen verarbeiteten Regionen, Verlust sinnvoller Grenzen und große Qualitätsregressionen bei a
ähnliche Ausgabeanzahl. Dichteorientierte Änderungen sollten zeigen, dass die entfernte Konzentration dies tat
keine nützliche Krümmung oder Topologie aufweisen.

Die Leistungsergebnisse sollten den Prozessor, die Speicherkapazität, die Grafikhardware und den Betrieb identifizieren
System, Eingabegröße und ob die Daten bereits zwischengespeichert wurden. Strukturvalidierung und Screenshots
unterstützen die Überprüfung, ersetzen jedoch nicht die Inspektion durch Mitwirkende, die mit der Quellgeometrie vertraut sind.

## Regressionstests

Bevorzugen Sie deterministische Tests mit expliziten Toleranzen. Halten Sie neue Geräte klein genug für normales Git.
Dokumentieren Sie ihre Herkunft und Lizenz und verwenden Sie synthetische Geometrie, wenn echte Quelldaten nicht erforderlich sind.
Die Tests sollten den Abbruch und die Zustandswiederherstellung abdecken, wenn durch einen Vorgang die Geometrie geändert werden kann.
