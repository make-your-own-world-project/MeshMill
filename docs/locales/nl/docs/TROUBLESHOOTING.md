# Problemen oplossen

## Windows blokkeert de download

Niet-ondertekende communitybuilds kunnen Microsoft Defender SmartScreen activeren. Vergelijk de gedownloade
SHA-256-hash van het bestand met `SHA256SUMS.txt` uit dezelfde GitHub-release. Ondertekende releases identificeren
hun uitgever in de bestandseigenschappen Windows.

## De draagbare build start niet

Pak de volledige ZIP uit voordat u `MeshMill.exe` uitvoert. De map `_internal` moet de volgende blijven
naar beide uitvoerbare bestanden. Voer het uitvoerbare bestand niet uit vanuit de ZIP-viewer.

## Er wordt een grote STL geopend als overzicht

De geschatte werkset overschrijdt het geheugenbudget in Instellingen. De overzichtsmodus is opzettelijk gemaakt
alleen-lezen. Verhoog het budget alleen als de machine voldoende beschikbaar geheugen heeft, of verlaag het budget
mesh voordat u het opent voor bewerking.

## Er is geen standaardweergave opgeslagen

Druk op de sneltoets voor de door Ctrl gewijzigde weergave en kies vervolgens **Opslaan** of druk op Enter ter bevestiging
dialoog. Door één weergave op te slaan, wordt ook de tegenovergestelde bijgewerkt. De statusregel meldt de opgeslagen weergave.

## Navigatiesnelkoppelingen reageren niet

Sluit eerst een modaal dialoogvenster. Bekijk of reset snelkoppelingen in Instellingen als ze zijn aangepast. De
standaardweergavesnelkoppelingen gebruiken Invoegen, Home, Pagina omhoog, Verwijderen, Einde en Pagina omlaag.

## Maak een diagnostisch logboek voor de lokale oriëntatie

Diagnostische registratie is standaard uitgeschakeld. Om toetsenbordrouting en camerastatus lokaal vast te leggen:

```powershell
.\MeshMill.exe --diagnostic-log ".\orientation-session.jsonl" "C:\path\mesh.stl"
```

Het logbestand kan het geopende bestandspad bevatten. Controleer en redigeer het voordat u het deelt. Mesh-geometrie is dat niet
naar het logboek geschreven.

## Meld een probleem

Inclusief de MeshMill-versie, Windows-versie, GPU-model, aantal mesh-driehoeken, exacte actie
volgorde en of het installatieprogramma of het draagbare pakket is gebruikt. Gebruik het herdistribueerbare monster
mesh wanneer mogelijk. Voeg geen privéscans of diagnostische logbestanden toe zonder deze eerst te bekijken.
