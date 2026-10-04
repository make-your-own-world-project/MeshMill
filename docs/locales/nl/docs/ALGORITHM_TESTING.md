# Algoritmetesten en bijdrage

MeshMill-algoritmen moeten moeilijke geometrie beheersbaar maken en hun effecten zichtbaar houden,
meetbaar en omkeerbaar voordat een resultaat wordt toegepast.

## Referentie armaturen

Gebruik beide gebundelde versies van de samengestelde monstergeometrie:

- `samples/sample-scan.stl` is de kleinere normale Git-fixture voor routinematige ontwikkeling, geautomatiseerd
  controles en het leren van de controles.
- `samples/original-scan.stl` is de volledige Git LFS-fixture voor gedrag bij grote bestanden, redundante lagen,
  ongelijkmatige dichtheid, overlap en prestatiewerk.

De redundante en dichte gebieden zijn opzettelijke testkenmerken. Een test kan zich op hen richten, maar
mag er niet van uitgaan dat elk overlappend oppervlak wegwerpbaar is. Voeg compacte synthetische meshes toe wanneer a
verandering heeft een bekende grens, kromming, topologie, dichtheid of overlap-invariant nodig.

## Vergelijkingscontrolelijst

Voor een algoritme- of parameterwijziging registreert u:

- MeshMill-versie of commit;
- invoer armatuur en controlesom;
- algoritme, kwaliteitsvoorinstelling, doel en geavanceerde instellingen;
- oorspronkelijke en resulterende driehoek- en hoekpunttellingen;
- reductiepercentage, afmetingen en dimensieafwijking;
- verstreken tijd en piekgeheugen wanneer prestaties relevant zijn;
- screenshots van dezelfde opgeslagen weergaven en weergavemodi;
- zichtbare grens-, gat-, zelfdoorsnede-, overlap- of vervormingsveranderingen;
- of het resultaat afkomstig was van een hele mesh- of alleen-selectiebewerking.

Vergelijk het met het huidige gedrag op hetzelfde doel, niet alleen met een andere preset met a
verschillende outputtellingen. Inspecteer de weergaven met schaduw, dichtheid, draadframe en hoekpunten waar van toepassing.

## Acceptatie begeleiding

Een optimalisatiewijziging moet onverwachte dimensieveranderingen, duidelijke oppervlakte-inversie,
scheuren tussen verwerkte regio's, verlies van betekenisvolle grenzen en grote kwaliteitsregressies bij a
vergelijkbaar aantal outputs. Op dichtheid gerichte veranderingen zouden moeten aantonen dat de verwijderde concentratie dat wel deed
geen bruikbare kromming of topologie dragen.

Prestatieresultaten moeten de processor, geheugencapaciteit, grafische hardware en besturing identificeren
systeem, invoergrootte en of de gegevens al in de cache stonden. Structurele validatie en screenshots
ondersteunen de beoordeling, maar vervangen de inspectie niet door bijdragers die bekend zijn met de brongeometrie.

## Regressietesten

Geef de voorkeur aan deterministische tests met expliciete toleranties. Houd nieuwe armaturen klein genoeg voor normale Git,
documenteer hun oorsprong en licentie, en gebruik synthetische geometrie wanneer echte brongegevens niet nodig zijn.
Tests moeten betrekking hebben op het annuleren en herstellen van de toestand wanneer een operatie de geometrie kan wijzigen.
