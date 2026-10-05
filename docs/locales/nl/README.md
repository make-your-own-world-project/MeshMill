<p align="center">
  <img src="assets/meshmill-logo.svg" width="620" alt="MeshMill: Dirty geometry? Clean it up!">
</p>

<!-- localization-navigation:start -->
<p align="center">
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/README.md">English</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ar/README.md">العربية</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/bn/README.md">বাংলা</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/de/README.md">Deutsch</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/el/README.md">Ελληνικά</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/es/README.md">Español</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/fa/README.md">فارسی</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/fr/README.md">Français</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ga/README.md">Gaeilge</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/hi/README.md">हिन्दी</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/hu/README.md">Magyar</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/id/README.md">Bahasa Indonesia</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/it/README.md">Italiano</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ja/README.md">日本語</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ko/README.md">한국어</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/nl/README.md">Nederlands</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/pl/README.md">Polski</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/pt/README.md">Português</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ro/README.md">Română</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ru/README.md">Русский</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/sr/README.md">Српски</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/th/README.md">ไทย</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/tr/README.md">Türkçe</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/uk/README.md">Українська</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ur/README.md">اردو</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/vi/README.md">Tiếng Việt</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/zh-CN/README.md">简体中文</a>
</p>
<!-- localization-navigation:end -->

MeshMill is een gespecialiseerde desktopapplicatie om zeer grote, complexe of
dichte mesh-geometrie hanteerbaar te maken. Het biedt snelle inspectie, dichtheidsanalyse,
selectie van gebieden, bijsnijden, verwijderen en gecontroleerde mesh-reductie, zonder dat een account of upload van geometrie nodig is.

GPU-versnelde OpenGL-rendering houdt viewport-navigatie, hardware-picking, dichtheidsvisualisatie,
en interactieve, responsieve inspectie. Mesh-reductie wordt momenteel uitgevoerd in afzonderlijke native CPU-werknemers,
lange geometrieberekeningen buiten de interface houden.

MeshMill werkt met meshes van 3D-scanners, CAD- en modelleerexportbestanden, reconstructiepipelines,
gegenereerde geometrie en andere STL-bronnen. Het bereidt geometrie voor op verdere verwerking in editors,
productietools en andere mesh-workflows. Algemene modellering, sculpting, animatie,
materialen en scène-opbouw vallen buiten het toepassingsgebied.

## Downloaden

Kies uw besturingssysteem. Elk pakket staat op zichzelf. Python, Node.js en andere
ontwikkelingsafhankelijkheden zijn niet vereist.

| Systeem | Aanbevolen download | Staat |
| --- | --- | --- |
| **Windows x64** | **[Download het Windows-installatieprogramma][windows-installer]** | Ondersteunde versie |
| Windows x64, geen installatie | [Download de draagbare ZIP][windows-portable] | Ondersteunde versie |
| Linux x86-64 | [Download de Linux-preview][linux-preview] | Vroege testvoorbeeld |
| macOS Apple silicium | [Download de Apple Silicon Preview][mac-arm-preview] | Vroege testvoorbeeld |
| macOS Intel | [Download de Intel Mac-preview][mac-intel-preview] | Vroege testvoorbeeld |

**De meeste Windows-gebruikers zouden het Windows-installatieprogramma moeten kiezen.** Gebruik de draagbare ZIP alleen als u dat doet
wil niet dat MeshMill wordt geïnstalleerd of heb geen toestemming om applicaties te installeren.

Linux- en macOS-pakketten zijn niet-ondertekende vroege previews. Ze passeren geautomatiseerde native builds en
verpakte rooktests, maar er moeten nog steeds echte hardwaretests worden uitgevoerd. Lees de
[Linux en macOS preview-opmerkingen](../../PLATFORM_TESTING.md) voordat u ze installeert.

Windows SmartScreen of macOS Gatekeeper kan waarschuwen voor niet-ondertekende pakketten.
Een optioneel voorbeeldmesh wordt meegeleverd met de ondersteunde Windows-release: [STL][sample-mesh].
Oudere versies en downloadcontrolesommen zijn beschikbaar op [GitHub Releases][all-releases].

[windows-installer]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-0.1.1-windows-x64-setup.exe
[windows-portable]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-0.1.1-windows-x64-portable.zip
[linux-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-linux-x86_64.tar.gz
[mac-arm-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-arm64.zip
[mac-intel-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-x86_64.zip
[sample-mesh]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-sample-scan-original.stl
[all-releases]: https://github.com/make-your-own-world-project/MeshMill/releases

## Snelstart

1. Open een STL.
2. Bekijk het model in de weergavemodus Shaded, Density, Wireframe of Vertices.
3. Kies een kwaliteitsniveau, algoritme en gewenst aantal driehoeken.
4. Selecteer **Optimize** om een ​​resultaat te berekenen.
5. Vergelijk het originele en het geoptimaliseerde mesh en selecteer vervolgens **Apply** om de bewerking toe te passen.
6. Selecteer **Save current state** of druk op `Ctrl+S`.

MeshMill start nooit automatisch een optimalisatie enkel omdat een bestand of instelling is gewijzigd.

## Mogelijkheden

- Invoer in binair en ASCII STL-formaat, uitvoer in binair STL-formaat
- Fast QEM-reductie met behoud van dichtheid, vorm en topologie
- GPU-versnelde OpenGL-viewport, hardware-picking en dichtheidsvisualisatie
- Native achtergrondgeometriewerkers voor maasreductie
- Weergavemodi: gearceerd, dichtheid, draadmodel (wireframe) en hoekpunten (vertex)
- Automatische doelwaarden afgeleid van de geometrie in plaats van een vast maximumaantal driehoeken
- Polygoonselectie met mogelijkheid tot additieve selectie van meerdere regio's
- Alleen de geselecteerde regio bijsnijden, verwijderen of optimaliseren
- Vergelijking van het originele, vorige en huidige mesh (met caching)
- Ongedaan maken en opnieuw uitvoeren van doorgevoerde geometrie-wijzigingen
- Afwijkingsmaat (drift), reductiepercentage en geschatte uitvoergrootte
- Weergave-eenheden: millimeter, centimeter, meter, inch en voet
- Statistieken voor CPU, geheugen, GPU en geometrie-activiteit
- Beperkt laden van overzichten wanneer een binair STL-bestand het ingestelde geheugenbudget overschrijdt
- Toepassingen met GUI en opdrachtregelinterface
- Lokale verwerking zonder afhankelijkheid van accounts, telemetrie, uploads of de cloud

## Inspecteer de geometrie voordat u deze verkleint

Het schaduwrijke display biedt een helder zicht op het oppervlak en het silhouet. Het is handig om te vergelijken
vormbehoud voordat een optimalisatiepas wordt toegepast.

![MeshMill gearceerd venster met het gebundelde voorbeeldgaas](../../images/meshmill-shaded.png)

Het Hoekpunten-display toont de feitelijke puntenverdeling. Dichte scangebieden, schaarse gebieden en
abrupte veranderingen in de bemonstering zijn zichtbaar zonder de geometrie te veranderen. Het uitgebreide deelvenster Metrieken
houdt CPU-, geheugen-, GPU- en geometrieverwerkingsactiviteiten bij tijdens het werken met de mesh.

![MeshMill Vertices worden weergegeven met uitgebreide prestatiestatistieken](../../images/meshmill-vertices.png)

Het Wireframe-display toont de driehoeksstructuur direct. Het helpt bij het identificeren van onnodige dichtheid,
onregelmatige triangulatie, en gebieden waar vereenvoudiging substantiële geometrie kan verwijderen.

![MeshMill Wireframe-weergave toont variatie in driehoeksdichtheid](../../images/meshmill-wireframe.png)

## Analyseer de maasdichtheid

De weergave Densiteit brengt de relatieve lokale dichtheid in het hele model in kaart. Schaarse gebieden blijven koel terwijl
steeds dichtere gebieden bewegen zich door helderdere kleuren, waardoor ongelijkmatige bemonstering in één oogopslag zichtbaar wordt.

![MeshMill-dichtheidsweergave toont de relatieve mesh-dichtheid](../../images/meshmill-density.png)

De dichtheid blijft beschikbaar tijdens het evalueren van een voorlopige optimalisatie. De toolbox rapporteert de
algoritme, doel, resulterende aantallen driehoeken en hoekpunten, reductiepercentage, afmetingen en
geschatte uitvoergrootte voordat de doorgang wordt toegepast.

![MeshMill Density-weergave toont een voorlopige optimalisatie](../../images/meshmill-density-overview.png)

Houd de rechtermuisknop ingedrukt om een gebied te inspecteren via het ronde vergrootglas. Het vergrote beeld
blijft gecentreerd op de aanwijzer en onthult de lokale dichtheid zonder de hoofdcamerapositie te veranderen.

![MeshMill-dichtheidsweergave met het vergrootglas](../../images/meshmill-density-zoom.png)

## Weergavebediening

| Invoer | Actie |
| --- | --- |
| Middelste muisknop slepen | Draaien (Orbit) |
| Shift + middelste muisknop slepen | Verschuiven (Pan) |
| Muiswiel | In-/uitzoomen op de aanwijzer |
| Ctrl + muiswiel | Rechtsom of linksom draaien |
| Pijltjestoetsen | Draaien rond het midden van het beeld |
| Ctrl + pijltjestoetsen | Verschuiven (Pan) |
| Ctrl + Shift + Omhoog/Omlaag | Zoomen |
| Ctrl + Shift + Links/Rechts | Rol |
| `F1` / `F2` / `F3` / `F4` | Schaduwrijk / Dichtheid / Draadframe / Hoekpunten |
| Rechtermuisknop ingedrukt houden | Vergrootglas |
| Shift + klik met de linkermuisknop | Liniaalpunten toevoegen of verwijderen |
| Ctrl + slepen naar links | Teken een selectiepolygoon |
| `Ctrl+C` | Voeg de polygoon toe aan de opgeslagen selectie |
| `Ctrl+X` | Bijsnijden tot selectie |
| `Ctrl+Space` | Optimaliseer de selectie |
| `Delete` | Verwijder de selectie |
| `Escape` | Wis de actieve selectie of liniaal |
| `Ctrl+Z` / `Ctrl+Y` | Ongedaan maken / opnieuw uitvoeren |
| `Ctrl+S` | Bewaar de huidige mesh-status |

Standaardweergavetoetsen volgen het navigatieblok met zes toetsen:

| Sleutel | Bekijk | Ctrl + toets |
| --- | --- | --- |
| `Insert` | Links | Stel de huidige oriëntatie in als Links |
| `Home` | Voorzijde | Stel de huidige oriëntatie in als Voorkant |
| `Page Up` | Juist | Stel de huidige oriëntatie in als Rechts |
| `Delete` | Top als er geen selectie bestaat | Stel de huidige oriëntatie in als Top |
| `End` | Terug | Stel de huidige oriëntatie in als Terug |
| `Page Down` | Onder | Stel de huidige oriëntatie in als Onder |

Als u een weergave opslaat, wordt ook de tegenovergestelde weergave bijgewerkt. Links en rechts, voor en achter, en boven en onder
blijven gepaard. In het bevestigingsvenster is **Opslaan** de standaardactie, dus Enter slaat het bestand op
oriëntatie. De voorkant wordt bovenaan zowel het boven- als het onderaanzicht weergegeven.

Snelkoppelingen kunnen worden gewijzigd of gereset in Instellingen.

## Selectieworkflow

Houd Ctrl ingedrukt en sleep naar links om een polygoon te tekenen. Versleep hoeken om deze een nieuwe vorm te geven, klik met de linkermuisknop op een rand om een rand toe te voegen
punt of klik met de rechtermuisknop op een rand om er een te verwijderen. Voeg meer regio's toe met `Ctrl+C`. Het bewegen van de camera verbergt
de schermruimtepolygoon terwijl de geselecteerde geometrie behouden blijft.

Optimalisatie met een actieve selectie heeft alleen invloed op die selectie. Het resultaat blijft voorlopig
totdat **Toepassen** is geselecteerd. **Annuleren** verwijdert het voorlopige resultaat en behoudt de selectie
een andere configuratie kan worden geprobeerd. Bijsnijden en verwijderen worden normale, ongedaan te maken mesh-bewerkingen.

Het selectiepaneel rapporteert de cumulatief geselecteerde hoekpunten, driehoeken, mesh-aandeel, geschat
maat en afmetingen. De acties bijsnijden, toevoegen, optimaliseren, verwijderen, een stap terug doen of de bewaarde bestanden wissen
selecteren zonder de omringende geometrie te verbergen.

![MeshMill toont een behouden regionale selectie en de bijbehorende geometriestatistieken](../../images/meshmill-crop-selection.png)

## Grote mazen

Voordat een binaire STL wordt toegewezen, vergelijkt de MeshMill het geschatte werkgeheugen met het geconfigureerde
geheugenbudget. Een bestand boven de begroting wordt geopend als een begrensd, alleen-lezen overzicht. Het overzicht rapporteert
het volledige aantal brondriehoeken, maar het bewerken en exporteren wordt uitgeschakeld omdat het een voorbeeld is en niet het volledige
voorwerp. Geïndexeerde, zoom-afhankelijke out-of-core-verwerking is gepland
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md).

## Commandoregel

`MeshMillCLI.exe` is opgenomen in beide releasepakketten:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

Voer `.\MeshMillCLI.exe --help` uit voor alle opties. MeshMill weigert het invoerbestand te overschrijven.

## Voorbeeldgeometrie

Er zijn twee versies van het ontwikkelingsvoorbeeld beschikbaar. Het monster is een samengesteld gaas met
opzettelijke lagen van redundante geometrie en gevarieerde dichtheid. Het geeft mensen zonder scanner een
realistisch instrument voor het vergelijken van algoritmen, het inspecteren van de dichtheid, het uitoefenen van regionale operaties,
en het ontwikkelen van routekaartfuncties. MeshMill vereist geen gescande invoer.

| Bestand | Driehoeken | Maat | Levering | Beste voor |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249.999 | 11,9 MiB | Normale Git | Snelle evaluatie, CI en het leren van de bedieningselementen |
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4.126.315 | 196,8 MiB | Git LFS | Testen van dichte brongeometrie en prestaties met grote mazen |

Het kleinere voorbeeld wordt bij elke normale kloon gedownload. Het onaangeroerde origineel is optioneel en
beheerd via Git LFS, zodat de gewone repositorygeschiedenis niet wordt opgeblazen. GitHub Desktop inclusief
Git LFS. Commandoregelgebruikers kunnen Git LFS installeren en uitvoeren:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

Getagde releases publiceren ook de originele STL als directe download voor mensen die Git niet gebruiken.
Zie [`samples/README.md`](../../../samples/README.md) voor herkomst, afmetingen en controlesommen.

Bijdragers van algoritmen moeten ook de
[gids voor het testen van algoritmen](docs/ALGORITHM_TESTING.md) voordat u de reductie vergelijkt of wijzigt
gedrag.

## STL-eenheden

STL codeert geen eenheid. Door modeleenheden te wijzigen, worden labels en metingen gewijzigd zonder te schalen
de opgeslagen coördinaten. Selecteer de eenheid die de brongeometrie beschrijft.

## Privacy

MeshMill leest en schrijft lokale bestanden. Het bevat geen account, telemetrie, upload, reclame of
cloudverwerkingsfunctie. De huidige implementatie van GPU-statistieken maakt gebruik van lokale Windows-prestaties
tellers. Equivalente aanbieders van native metrische gegevens zijn gepland voor Linux en macOS.

Voor diagnostische probleemoplossing kunnen ontwikkelaars de GUI starten met
`--diagnostic-log <local-file.jsonl>`. Het logboek registreert de invoerroutering en de camerastatus lokaal en is
uitgeschakeld tijdens normaal gebruik.

## Ontwikkeling en uitgave

Gelokaliseerde UI-tekst en documentatie worden in eerste instantie geproduceerd met externe machinevertaling
diensten en automatisch gecontroleerd op structurele schade. Machinevertaling kan nog steeds
onnatuurlijk of onjuist. Moedertaalsprekers worden aangemoedigd vertalingen te beoordelen en te corrigeren
het contributieproces.

- [Bijdragen](CONTRIBUTING.md)
- [Vrijgaveproces](RELEASING.md)
- [Routekaart](ROADMAP.md)
- [Problemen oplossen](docs/TROUBLESHOOTING.md)
- [Mededelingen van derden](THIRD_PARTY_NOTICES.md)

## Ondersteuning MeshMill

MeshMill wordt onafhankelijk ontwikkeld en onderhouden. Lees
[waarom ondersteuning van dit werk belangrijk is](SUPPORT.md), of ondersteun voortdurende ontwikkeling via
[Koop een koffie voor mij](https://buymeacoffee.com/tednv).

MeshMill valt onder de GNU General Public License, versie 3 of hoger. Zie
[`LICENSE`](../../../LICENSE).
