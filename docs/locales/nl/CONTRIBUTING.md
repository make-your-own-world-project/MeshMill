# Bijdragen

Bijdragen zijn welkom via issues en pull-requests.

## Projectomvang

MeshMill maakt te grote, compacte of moeilijke mesh-bestanden beheersbaar voor downstream-bewerking en
productieworkflows. Bijdragen moeten de geometrie-inspectie, mesh- en puntdichtheid verbeteren
beheer, optimalisatie, selectie, bijsnijden, opschonen, validatie, STL-uitwisseling, prestaties,
of de coördinatie van deze operaties.

Het project omvat geen modellering, beeldhouwkunst, schilderkunst, animatie, rendering,
scènecompositie, materialen, rigging of andere systemen voor het creëren van inhoud. Voorstellen die introduceren
deze functies vallen buiten de reikwijdte van het project.

Nieuwe functies moeten de applicatie gefocust houden en directe workflows behouden die van bron veranderen
geometrie in beheersbare meshes, en vermijd het omzetten van ondersteunende bedieningselementen in een algemene bewerking
omgeving.

## Lokalisatie

Engelse UI-brontekst is opgeslagen in `locales/en-US.json`. Metagegevens van landinstellingen worden opgeslagen in
`locales/manifest.json`. Vertaalde UI-catalogi gebruiken dezelfde stabiele sleutels en bestandsnaam
`<locale>.json`. Vertaalde documentatie gebruikt de overeenkomende rootbestandsnaam onder
`docs/locales/<locale>/`.

Voer na het wijzigen van labels, tooltips, dialoogvensters of andere voor de gebruiker zichtbare tekst het volgende uit:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
```

Bekijk bronwijzigingen en opnieuw gegenereerde sleutels samen.

## Veranderingen in geometrie en algoritmen

Gebruik de gebundelde monstergeometrie bij het wijzigen van optimalisatie, dichtheidsanalyse, selectie, bijsnijden,
verwerking van grote bestanden of gedrag bij het vergelijken van viewports. Het bevat opzettelijk overtollige lagen
en ongelijkmatige dichtheid, dus een nuttig resultaat zou de beheersbaarheid moeten verbeteren zonder vervorming te verbergen,
het negeren van betekenisvolle grenzen, of het stilletjes verwijderen van geometrie die een ander algoritme behoudt.

Registreer de invoer, het algoritme, de instellingen, het aantal driehoeken, de afmetingen, de dimensieafwijking, de verstreken tijd,
en relevante screenshots voor vergelijkingen. Test zowel de kleinere normal-Git-fixture als, wanneer de
verandering betreft grote of gelaagde geometrie, het originele Git LFS-armatuur. Stem een algoritme niet af
alleen al aan dit armatuur. Voeg kleine synthetische gevallen toe voor het specifieke invariante of regressiewezen
getest.

Zie [Algoritmen testen en bijdrage](docs/ALGORITHM_TESTING.md) voor de vergelijkingschecklist.

## Ontwikkeling opstelling

1. Installeer 64-bit Python 3.12 op Windows.
2. Creëer en activeer een virtuele omgeving.
3. Installeer `requirements-dev.txt`.
4. Voer `python meshmill.py` uit voor de GUI of `python meshmill.py --help` voor CLI-gebruik.
5. Voer `python -m py_compile meshmill.py` uit voordat u een wijziging indient.

Bewaar privé-meshes, gegenereerde uitvoerbare bestanden, schermafbeeldingen met privé-informatie en lokaal
mappen bouwen uit commits. Herdistribueerbare testgeometrie hoort bij `samples/`
bron, licentie, afmetingen en generatiemethode gedocumenteerd. Nieuwe bronbestanden moeten de extensie
SPDX-identificatie `GPL-3.0-or-later`.

Snijd elke documentatiescreenshot bij tot de inhoud van de MeshMill-applicatie. Neem niet de
taakbalk, niet-gerelateerd vensterchroom, meldingen, accountgegevens, privépaden of achtergrond
inhoud van het bureaublad.
