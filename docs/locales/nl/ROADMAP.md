# MeshMill-routekaart

## Platformondersteuning

Windows is het eerste verpakte platform. De applicatiearchitectuur en mesh-formaten zijn
platformonafhankelijk, en toekomstige releases zouden native Linux- en macOS-pakketten moeten toevoegen. Platformwerk
omvat verpakking, applicatie-integratie, hardwarestatistieken, gedrag van bestandssystemen en geautomatiseerd
releasetests met behoud van dezelfde project- en STL-workflows op elk ondersteund systeem.

- Valideer het Linux x86-64 preview-pakket voor distributies, desktopomgevingen en beeldschermen
  servers en GPU-stuurprogramma's voordat u deze naar stable promoveert.
- Valideer de macOS Apple Silicon- en x86-64 preview-pakketten op echte hardware en voeg vervolgens Developer toe
  ID-ondertekening en notariële bekrachtiging voordat ze naar stabiel worden gepromoveerd.
- Voeg platform-native CPU-, geheugen- en GPU-metriekenproviders toe achter een gedeelde interface.
- Houd opgeslagen instellingen, toetsenbordtoewijzingen, opdrachtregelgedrag en projectgegevens draagbaar.

In dit stappenplan worden de geplande werkzaamheden vastgelegd. Er worden geen functies in de huidige release beschreven.

## Reikwijdte

MeshMill beheert geometrie, meshdichtheid, puntdichtheid, optimalisatie, opschoning, validatie en STL
kunnen worden uitgewisseld, zodat grote of zware mesh-bestanden nuttig blijven in de stroomafwaartse bewerkingsworkflows.

Modellering voor algemene doeleinden, beeldhouwen, schilderen, animatie, rendering, scènecompositie, materialen,
rigging en andere systemen voor het creëren van inhoud vallen buiten deze routekaart. Gedistribueerde synthese is van toepassing
aan de mesh-beheerbewerkingen van MeshMill en breidt het product niet uit naar een algemene editor.

## Referentiegeometrie

Het gebundelde composietgaas is het gemeenschappelijke ontwikkelingsmiddel voor de huidige algoritmen en routekaart
werk. De opzettelijk redundante lagen en ongelijkmatige dichtheid ondersteunen herhaalbare vergelijkingen van
reductiekwaliteit, dichtheidsanalyse, afhandeling van overlappingen, regionale operaties, out-of-core verwerking,
en toekomstige synthese. Roadmap-implementaties moeten resultaten rapporteren tegen deze armatuur en klein
speciaal gebouwde regressienetwerken, in plaats van het gedrag voor één model alleen te optimaliseren.

## Multi-STL-werkruimten en statistische synthese

Een werkruimte moet meerdere STL-invoer accepteren als afzonderlijke, onafhankelijk zichtbare bronobjecten.
MeshMill zou deze bronnen op één lijn moeten brengen, hun geometrische overeenkomst moeten meten en er één moeten synthetiseren die bruikbaar is
mesh zonder dubbele interne oppervlakken of herhaalde overlapgeometrie te behouden.

Gepland gedrag:

- meerdere STL-bronnen toevoegen, verwijderen, verbergen, isoleren, opnieuw ordenen en inspecteren in één werkruimte;
- bronidentiteit, eenheden, transformaties, grenzen, resolutie en werkingsgeschiedenis behouden;
- zorgen voor automatische registratie met handmatige uitlijningscontroles en meetbare pasvormkwaliteit;
- verdeel bronnen vóór vergelijking in ruimtelijke gebieden, zodat grote inputs begrensd blijven;
- analyseer bezetting, afstand tot het oppervlak, normale overeenkomst, lokale dichtheid, variantie, en
  aantal observaties over overlappende gebieden;
- classificeer overeenkomende oppervlakken, conflicterende oppervlakken, scanruis, gaten en unieke geometrie;
- statistisch overeenkomende oppervlakken consolideren tot een representatief oppervlak met vastgelegde gegevens
  vertrouwen in plaats van dubbele driehoeken op elkaar te stapelen;
- verwijder ingesloten, samenvallende en gedeelde geometrie die geen uiterlijke vormdetails toevoegt;
- behoud niet-overlappende brongeometrie en leg dubbelzinnige gebieden bloot voor visuele beoordeling;
- weging per bron en per regio mogelijk maken wanneer één scan schoner of gedetailleerder is;
- valideren van waterdichtheid, grenzen, normalen, dimensies en topologie na synthese;
- registreer de herkomst van de bron en de syntheseparameters zodat de gecombineerde mesh reproduceerbaar is;
- bekijk een voorbeeld van het verwachte aantal driehoeken, de grenzen, de verwijderde overlap en de betrouwbaarheidsverdeling ervoor
  het vastleggen van het gesynthetiseerde resultaat.

Deze workflow moet hetzelfde out-of-core ruimtelijke index- en werkeenheidmodel gebruiken dat is gepland voor groot
mazen. Statistische vergelijking en overlapconsolidatie moeten ook over lokaal verspreid kunnen worden
of externe MeshMill-knooppunten.

## Gedistribueerde synthese

Een MeshMill-cluster moet meerdere knooppunten coördineren die parallel over meerdere knooppunten werken
werkstations. Een knooppunt kan een toegewezen regio of gebied inspecteren, selecteren, reduceren, valideren, repareren of combineren
werk eenheid. Bijdragen blijven onafhankelijk van versie tot ze zijn beoordeeld en opgenomen
naar een gedeelde objectversie.

Het systeem moet het volgende ondersteunen:

- gelijktijdige bijdragen van meerdere operators en geautomatiseerde knooppunten;
- deterministische inputs, parameters, afhankelijkheden en outputs van werkeenheden;
- capaciteitsbewuste planning op basis van CPU, GPU, geheugen, algoritmen en huidige belasting;
- afhankelijkheidsbewuste verdeling van meshes, regio's, validatiepassen en synthesefasen;
- duurzame wachtrijen met pauzeren, hervatten, annuleren, opnieuw proberen, opnieuw toewijzen en herstel van fouten;
- op inhoud gerichte artefacten en integriteitscontroles tussen knooppunten;
- reproduceerbare synthese uit een opgenomen reeks geaccepteerde bijdrageversies;
- offline of met tussenpozen verbonden werkstations die later kunnen synchroniseren;
- local-first-operatie met expliciete controle over deelnemende knooppunten en gedeelde projectgegevens.

## Versie-samenwerking

Elke bijdrage moet de versie van het bovenliggende object, de geselecteerde regio of werkeenheid, de werking,
parameters, knooppuntidentiteit, tijdstempels, afhankelijkheden, validatieresultaten en uitvoercontrolesom.

Gepland samenwerkingsgedrag:

- projecten bevatten objecten, vertakkingen, controlepunten, bijdragen en gesynthetiseerde versies;
- bijdragers kunnen vanuit dezelfde bovenliggende versie werken zonder elkaar te overschrijven;
- niet-overlappende bijdragen kunnen na validatie automatisch worden samengevoegd;
- overlappende geometrie of incompatibele afhankelijkheden creëren een expliciet conflict;
- conflicten bieden visuele vergelijking, keuze op regioniveau, rebase, herhaling en handmatige oplossing;
- beoordelingsstatussen omvatten hangende, geaccepteerde, afgewezen, vervangen, tegenstrijdige en opgenomen;
- het uiteindelijke synthesemanifest identificeert elke opgenomen bijdrage en afhankelijkheid.

## Coördinatie-UI

De desktopapplicatie moet gedistribueerd werk beheren zonder dat een aparte opdrachtregel nodig is
of serverbeheerworkflow. Geplande weergaven omvatten:

- **Projecten:** objecten, vertakkingen, versies, bijdragers en synthesestatus.
- **Cluster:** verbonden werkstations en knooppunten, mogelijkheden, status, belasting en huidige toewijzing.
- **Wachtrij:** werkeenheden in behandeling, actief, onderbroken, geblokkeerd, mislukt en voltooid.
- **Bijdragen:** auteur, knooppunt, bovenliggende versie, getroffen regio, parameters, controles en beoordelingsstatus.
- **Vergelijk:** gesynchroniseerde 3D-weergaven, geometrieverschillen, statistieken en grensinspectie.
- **Conflicten:** overlappende regio's, afhankelijkheidsconflicten, oplossingskeuzes en validatieresultaten.
- **Synthese:** afhankelijkheidsgrafiek, totale voortgang, geselecteerde bijdrageversies en uiteindelijke output.
- **Geschiedenis:** vertakkingsgrafiek, controlepunten, samenvoegingen, gesynthetiseerde versies en reproduceerbaarheidsmanifesten.

De viewport moet eigendom, toegewezen regio's, voltooid werk, openstaande wijzigingen, conflicten,
en versieverschillen zonder de onderliggende mesh te wijzigen.

## Coördinatie en transport

De eerste ontwerpfase moet protocolgrenzen definiëren voordat een transport wordt geselecteerd. Het protocol
coördinatie-metagegevens moeten scheiden van grote mesh-artefacten, hervatbare overdracht moeten ondersteunen, en
bruikbaar blijven op een lokaal netwerk zonder een extern account of gehoste service.

Vereiste coördinatieconcepten:

- coördinatorverkiezing of een expliciet gekozen coördinator;
- knooppuntdetectie en handmatige knooppuntinschrijving;
- geauthenticeerde sessies en projectgerichte autorisatie;
- huurovereenkomsten en hartslagen voor werkeigendom;
- idempotente werkinzending en resultaatacceptatie;
- versieonderhandelingen tussen verschillende MeshMill-releases;
- gestructureerde gebeurtenissen voor voortgang, logboeken, validatie, mislukkingen en nieuwe pogingen;
- herstel na onderbreking van coördinator, werkstation, netwerk of knooppunt.

## Leveringsfasen

### Fase 0: out-of-core grootschalige verwerking

Het index-, streaming-, cache-, werkeenheid- en veiligheidscontract zijn gedocumenteerd in
[`docs/OUT_OF_CORE.md`](docs/OUT_OF_CORE.md).

- Schat het aantal driehoeken en het werkgeheugen voordat u de volledige mesh toewijst.
- Open extra grote binaire STL-bestanden als begrensde, gelijkmatig bemonsterde navigatieoverzichten.
- Verdeel geometrie met volledige resolutie in ruimtelijke kubussen met deterministische overlappende grenzen.
- Lees, analyseer en optimaliseer gelijktijdig onafhankelijke kubussen binnen de CPU- en geheugenlimieten.
- Benchmark GPU-compute-implementaties voor reductiefasen zoals foutevaluatie, kandidaat
  scores, ruimtelijke zoekopdrachten en onafhankelijke verwerking van werkeenheden. Offload een fase alleen wanneer deze is bereikt
  biedt een meetbaar end-to-end snelheids- of geheugenvoordeel zonder het determinisme, mesh, te verminderen
  kwaliteit, topologiegaranties of compatibiliteit met systemen die geen geschikte GPU hebben.
- Stream grof-naar-fijn viewport-niveaus in plaats van dat u de volledige mesh in het geheugen nodig heeft.
- Teken de kubusstatus rechtstreeks in de viewport: in de wachtrij, lezen, verwerken, voltooid en mislukt.
- Toon de voortgang per kubus door elke kubus te vullen en een overzicht van het hele object op hoog niveau te behouden.
- Stel verwerkte kubussen samen met grensvalidatie, dubbele verwijdering en reproduceerbare instellingen.
- Breid de lokale kubusplanner in latere fasen uit naar gedistribueerde synthesewerkeenheden.

### Fase 1: lokale fundering met versieversie

- Definieer object-, bewerkings-, bijdrage-, vertakkings- en manifestformaten.
- Voeg meerdere STL-werkruimten toe met zichtbaarheid per bron, transformaties, metagegevens en herkomst.
- Voeg registratiekwaliteitsstatistieken en ruimtelijke overlapclassificatie toe.
- Synthetiseer statistisch overeenkomende oppervlakken en verwijder dubbele en ingesloten geometrie.
- Voeg visuele beoordeling toe voor conflicten, hiaten, vertrouwen en geometrie die uniek zijn voor één bron.
- Bewaar de lokale geschiedenis tijdens applicatiesessies.
- Voeg visuele mesh- en regiovergelijkingen toe.
- Maak bewerkingen deterministisch en onafhankelijk reproduceerbaar.

### Fase 2: gecoördineerde lokale knooppunten

- Voer werkknooppunten uit op één werkstation.
- Voeg wachtrijen, capaciteitsrapportage, werktoewijzing en annulering toe.
- Geef knooppunt- en werkeenheidstatus weer in de MeshMill-gebruikersinterface.
- Valideer de partitie en resultaatassemblage lokaal.

### Fase 3: synthese van meerdere werkstations

- Voeg geverifieerde LAN-detectie en -inschrijving toe.
- Draag op inhoud gerichte werkinvoer en resultaten over met CV-ondersteuning.
- Coördineer gelijktijdig werk op meerdere werkstations.
- Herstel toewijzingen na een knooppunt- of netwerkfout.

### Fase 4: collaboratief versiebeheer

- Voeg bijdragers, vertakkingen, beoordelingsstatussen en machtigingen toe.
- Voeg niet-overlappende bijdragen samen.
- Detecteer en los overlappende of afhankelijkheidsconflicten op.
- Synthetiseer geselecteerde bijdragen tot een reproduceerbare objectversie.

### Fase 5: productieharding

- Voeg protocolcompatibiliteitstests en verwerking van gemengde versies toe.
- Voeg audit-, integriteits-, corruptie-, onderbrekings- en hersteltests toe.
- Benchmark prestaties op het gebied van planning, partitionering, overdracht, samenvoeging en synthese.
- Documentimplementatie, back-up, migratie en incidentherstel.
