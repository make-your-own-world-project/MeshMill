# Out-of-core mesh-architectuur

De huidige beveiliging voor grote bestanden van MeshMill schat het werkgeheugen in voordat een volledig bestand wordt toegewezen
gaas. Bestanden die het geconfigureerde budget overschrijden, kunnen worden geopend als begrensde navigatieoverzichten. Een
Het overzicht is een bemonsterde geometrie, is zichtbaar als zodanig geïdentificeerd en kan niet worden bewerkt of geëxporteerd als
ook al was het de volledige bron.

Echte zoomafhankelijke details vereisen een persistente ruimtelijke index. Onderstaand ontwerp definieert dat
volgende implementatiefase.

## Indexformaat

Elke bronmesh ontvangt een `.meshmill-index`-map met versiebeheer met daarin:

- `manifest.json`, met de brongrootte, wijzigingstijd, hashes van bemonsterde inhoud, grenzen,
  driehoekentelling, indexversie, coördinaatprecisie en niveaubeschrijvingen;
- ruimtelijke tegels geadresseerd op octree-niveau en Morton-code;
- een grof weergavegaas voor elke bezette oudertegel;
- driehoekige records met volledige resolutie in bladtegels; En
- grenseigendom en overlappende metadata die worden gebruikt tijdens regionale operaties en assemblage.

Bij het maken van een index wordt de bron opeenvolgend gelezen in begrensde blokken. Het schrijft tijdelijke tegelruns en
publiceert atomair het manifest nadat elk vereist bestand de validatie heeft doorstaan. Een onderbroken of
De verouderde index wordt gedetecteerd in het manifest en kan worden hervat of opnieuw opgebouwd zonder de volledige index te openen
netwerk in het geheugen.

## Viewport-streaming

De viewport selecteert tegels met behulp van de camera-frustum en schermruimtefout. Grove bovenliggende tegels zijn dat wel
eerst getoond. Zichtbare onderliggende tegels vervangen deze naarmate de camera dichterbij komt, buiten het scherm en
tegels met een lage impact blijven grof. RAM en VRAM hebben onafhankelijke budgetten en de minst recent gebruikte
caches. Door details los te laten, wordt nooit de grove representatie van het hele object vrijgegeven.

De planner registreert deze tegelstatussen: in de wachtrij, lezen, verwerken, uploaden, aanwezig, mislukt,
en geannuleerd. De viewport kan kubussen op staat kleuren en elke kubus in proportie vullen
vooruitgang. Bij annulering worden gedeeltelijke resultaten verwijderd en blijft de laatste volledige weergave actief.

## Verwerking en capaciteit

Een lokale werkeenheid is een tegel plus de deterministische overlap die vereist is voor de werking ervan. Gelijktijdigheid
wordt beperkt door de momenteel beschikbare RAM, het geconfigureerde geheugenpercentage, het aantal logische processors en
gemeten grootte van de werkeenheid. GPU uploaden en weergeven hebben een apart VRAM-budget. Parallel gerapporteerd
capaciteit is een schatting totdat representatieve tegels zijn gemeten.

Operaties behouden één eigenaar voor elk grenselement. Assembly valideert gedeelde grenzen,
verwijdert duplicaten, controleert aantallen en grenzen, en registreert de exacte gebruikte parameters. Hetzelfde werk
eenheid en resultaatformaat kunnen later worden gepland over gedistribueerde syntheseknooppunten.

## Veiligheidsregels

- Een globaal voorbeeld wordt gelabeld als een overzicht en niet als viewport-detail met volledige resolutie.
- Een overzicht kan niet als de volledige bronmesh worden overschreven of geëxporteerd.
- Voor vollastaanvragen die het huidige budget overschrijden, is een expliciete keuze nodig.
- Het genereren van indexen, tegelverwerking en assemblage blijven annuleerbaar en behouden de vorige
  volledige staat.
- Capaciteitswaarden zijn schattingen en geven aan of ze de huidige motor beschrijven of gepland zijn
  parallelle tegeluitvoering.
