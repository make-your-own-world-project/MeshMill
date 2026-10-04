# MeshMill

![MeshMill shaded viewport](../../images/meshmill-shaded.png)

MeshMill is een gespecialiseerde desktopapplicatie om zeer grote, complexe of
dichte mesh-geometrie hanteerbaar te maken. Het biedt snelle inspectie, dichtheidsanalyse,
selectie van gebieden, bijsnijden, verwijderen en gecontroleerde mesh-reductie, zonder dat een account of upload van geometrie nodig is.

MeshMill werkt met meshes van 3D-scanners, CAD- en modelleerexportbestanden, reconstructiepipelines,
gegenereerde geometrie en andere STL-bronnen. Het bereidt geometrie voor op verdere verwerking in editors,
productietools en andere mesh-workflows. Algemene modellering, sculpting, animatie,
materialen en scène-opbouw vallen buiten het toepassingsgebied.

## Downloaden

Download een van deze bestanden via [GitHub Releases](../../releases):

- `MeshMill-<version>-windows-x64-setup.exe`: installatieprogramma per gebruiker, inclusief Startmenu-item en optionele
  snelkoppelingen op het bureaublad.
- `MeshMill-<version>-windows-x64-portable.zip`: portable applicatie. Pak het volledige archief uit,
  en start vervolgens `MeshMill.exe`.

Beide pakketten bevatten de runtime voor de applicatie. Eindgebruikers installeren geen Python-, Node.js- of
afhankelijkheden. De eerste release ondersteunt Windows 10 en Windows 11 op x64-hardware. Linux- en
macOS-pakketten staan ​​gepland; de product- en bestandsformaten zijn niet specifiek voor Windows.

Niet-ondertekende community-builds kunnen een Windows SmartScreen-waarschuwing weergeven. Release-checksums staan ​​vermeld
in `SHA256SUMS.txt` naast elke release.

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

![MeshMill-dichtheidsweergave](../../images/meshmill-density.png)

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
