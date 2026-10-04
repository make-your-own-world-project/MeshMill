# Contribuire

I contributi sono benvenuti tramite problemi e richieste pull.

## Ambito del progetto

MeshMill rende i file mesh di grandi dimensioni, densi o difficili gestibili per la modifica downstream e
flussi di lavoro di produzione. I contributi dovrebbero migliorare l'ispezione della geometria, la mesh e la densità dei punti
gestione, ottimizzazione, selezione, ritaglio, pulizia, convalida, scambio STL, prestazioni,
o il coordinamento di tali operazioni.

Il progetto non include modellazione, scultura, pittura, animazione, rendering,
composizione della scena, materiali, rigging o altri sistemi di creazione di contenuti. Proposte che introducono
tali funzionalità non rientrano nell'ambito del progetto.

Le nuove funzionalità dovrebbero mantenere focalizzata l'applicazione, preservare i flussi di lavoro diretti che trasformano l'origine
la geometria in mesh gestibili ed evitare di trasformare i controlli di supporto in una modifica generale
ambiente.

## Localizzazione

Il testo di origine dell'interfaccia utente in inglese è archiviato in `locales/en-US.json`. I metadati locali sono archiviati in
`locales/manifest.json`. I cataloghi dell'interfaccia utente tradotti utilizzano le stesse chiavi stabili e il nome file
`<locale>.json`. La documentazione tradotta utilizza il nome file root corrispondente sotto
`docs/locales/<locale>/`.

Dopo aver modificato etichette, descrizioni comandi, finestre di dialogo o altro testo visibile all'utente, esegui:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
```

Esamina insieme le modifiche all'origine e le chiavi rigenerate.

## Modifiche alla geometria e all'algoritmo

Utilizzare la geometria del campione in bundle quando si modifica l'ottimizzazione, l'analisi della densità, la selezione, il ritaglio,
gestione di file di grandi dimensioni o comportamento di confronto delle viste. Contiene intenzionalmente livelli ridondanti
e densità irregolare, quindi un risultato utile dovrebbe migliorare la gestibilità senza nascondere la distorsione,
scartando confini significativi o rimuovendo silenziosamente la geometria preservata da un altro algoritmo.

Registra l'input, l'algoritmo, le impostazioni, il conteggio dei triangoli, le dimensioni, la deriva delle dimensioni, il tempo trascorso,
e screenshot pertinenti per i confronti. Testa sia il dispositivo normal-Git più piccolo che, quando il
il cambiamento riguarda la geometria ampia o stratificata, l'attrezzatura originale Git LFS. Non ottimizzare un algoritmo
solo a questo apparecchio. Aggiungi piccoli casi sintetici per l'invariante specifico o l'essere di regressione
testato.

Consulta [Test e contributo dell'algoritmo](docs/ALGORITHM_TESTING.md) per l'elenco di controllo del confronto.

## Configurazione dello sviluppo

1. Installa Python 3.12 a 64 bit su Windows.
2. Creare e attivare un ambiente virtuale.
3. Installa `requirements-dev.txt`.
4. Esegui `python meshmill.py` per la GUI o `python meshmill.py --help` per l'utilizzo della CLI.
5. Esegui `python -m py_compile meshmill.py` prima di inviare una modifica.

Mantieni mesh private, eseguibili generati, screenshot contenenti informazioni private e locali
creare directory dai commit. La geometria di prova ridistribuibile appartiene a `samples/` con il suo
sorgente, licenza, dimensioni e metodo di generazione documentati. I nuovi file sorgente dovrebbero utilizzare l'estensione
Identificatore SPDX `GPL-3.0-or-later`.

Ritaglia ogni screenshot della documentazione nel contenuto dell'applicazione MeshMill. Non includere il
barra delle applicazioni, cromatura di finestre non correlate, notifiche, dettagli dell'account, percorsi privati o sfondo
contenuto del desktop.
