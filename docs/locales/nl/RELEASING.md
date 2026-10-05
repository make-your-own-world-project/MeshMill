# MeshMill vrijgeven

De stabiele releasepijplijn bouwt Windows-artefacten op door GitHub gehoste Windows-hardware. Een aparte
handmatige workflow bouwt niet-ondertekende Linux x86-64 en macOS Intel/Apple silicium previews op native
Door GitHub gehoste hardlopers. Eindgebruikers installeren Python, Node.js of afhankelijkheden niet.

Voordat u de lokalisatiebroncatalogi gaat bouwen, moet u deze vernieuwen en valideren:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## Vóór de eerste publieke release

1. Voltooi en valideer de geplande vertalingen van applicaties en documentatie.
2. Bekijk de GPL-kennisgevingen en kennisgevingen van derden.
3. Test de installatie, start, STL laden, optimalisatie, exporteren en verwijderen op een schone manier
   Windows-account of virtuele machine.
4. Voer CI uit tegen `samples/sample-scan.stl`. Inspecteer elke documentatiescreenshot en snijd deze uit
   de taakbalk, vensterchroom dat geen deel uitmaakt van MeshMill, meldingen, privépaden, account
   details en niet-gerelateerde desktopinhoud vóór publicatie.
5. Configureer de repository-lokale Git-auteur met het GitHub no-reply-adres van het account vóór de
   eerst plegen. Bevestig het met `git config --local --get user.email`.
6. Configureer optionele Authenticode-ondertekeningsgeheimen:
   - `WINDOWS_CERTIFICATE_BASE64`: Base64-gecodeerd PFX-certificaat.
   - `WINDOWS_CERTIFICATE_PASSWORD`: PFX-wachtwoord.

Zonder handtekeningcertificaat werken de gegenereerde bestanden nog steeds, maar toont Windows SmartScreen mogelijk
een waarschuwing voor een niet-herkende uitgever. Beschrijf niet-ondertekende builds niet als ondertekend of vertrouwd.

## Originele scan en Git LFS

`samples/original-scan.stl` wordt gevolgd via Git LFS omdat deze de normale 100 MiB van GitHub overschrijdt
bestandslimiet. Controleer vóór de eerste commit:

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

Het filter moet `lfs` zijn en het pointerobject-ID moet overeenkomen met `samples/SHA256SUMS.txt`. De vrijlating
workflow checkt LFS-inhoud uit en publiceert de originele STL als een afzonderlijk release-item. CI-gebruik
het kleinere normale Git-voorbeeld en downloadt het LFS-object niet.

## Test een releasebuild zonder publicatie

Open **Acties**, selecteer **Vrijgeven**, kies **Workflow uitvoeren** en voer een numerieke versie in, zoals
`0.1.0`. Bij een handmatige uitvoering worden werkstroomartefacten geüpload voor testen, maar wordt er geen openbare GitHub gemaakt
Laat los.

## Publiceer een release

Uit een schoon, beoordeeld `main`-filiaal:

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

De tag start de releaseworkflow. Het:

1. installeert de vastgezette build-afhankelijkheden;
2. genereert bijpassende metadata van de Windows-versie;
3. bouwt de op zichzelf staande GUI- en CLI-uitvoerbare bestanden;
4. ondertekent de uitvoerbare bestanden wanneer ondertekeningsgeheimen zijn geconfigureerd;
5. bouwt het Inno Setup-installatieprogramma per gebruiker;
6. ondertekent het installatieprogramma wanneer dit is geconfigureerd;
7. creëert het draagbare ZIP- en SHA-256-controlesombestand;
8. uploadt workflow-artefacten;
9. maakt de GitHub-release voor de gepushte tag.

Controleer het installatieprogramma en het draagbare archief op een schoon Windows-systeem voordat u de release aankondigt.
Bewaar de broncode die overeenkomt met elk gedistribueerd binair bestand dat beschikbaar is onder dezelfde releasetag.
Bevestig dat de knop GitHub naar de uiteindelijke URL van de openbare repository verwijst voordat u de eerste tagt
loslaten.

## Bouw Linux- en macOS-previews

Open **Acties**, selecteer **Platformvoorbeeldbuilds** en kies **Workflow uitvoeren**. Voer een voorbeeld in
versie zoals `0.2.0-preview.1`.

Laat **Publiceer een openbare GitHub-prerelease** uitgeschakeld voor de eerste uitvoering. De workflow bouwt en test:

- Linux x86-64 op Ubuntu 22.04;
- macOS x86-64 op een Intel-runner;
- macOS arm64 op een Apple siliconen runner.

Download de werkstroomartefacten en inspecteer hun controlesommen en logboeken. Voer de workflow opnieuw uit met
publiceren wordt alleen ingeschakeld nadat elke buildtaak is voltooid. Gepubliceerde macOS-previews zijn ad-hoc ondertekend,
niet door Apple notarieel bekrachtigd. Beschrijf ze als preview-builds en koppel er testers aan
`docs/PLATFORM_TESTING.md` en het probleemformulier **Platformvoorbeeldtest**.
