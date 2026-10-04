# Rilascio di MeshMill

La pipeline di rilascio crea artefatti Windows su runner Windows ospitati da GitHub. Gli utenti finali ricevono
un programma di installazione autonomo o ZIP portatile e non installare Python, Node.js o dipendenze.

Prima di creare, aggiornare e convalidare i cataloghi delle origini di localizzazione:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## Prima della prima uscita pubblica

1. Completare e convalidare le traduzioni previste delle domande e della documentazione.
2. Esamina la GPL e gli avvisi di terze parti.
3. Testare l'installazione, l'avvio, il caricamento STL, l'ottimizzazione, l'esportazione e la disinstallazione su un ambiente pulito
   Account Windows o macchina virtuale.
4. Esegui CI contro `samples/sample-scan.stl`. Esamina ogni screenshot della documentazione e ritagliala
   barra delle applicazioni, finestra cromata che non fa parte di MeshMill, notifiche, percorsi privati, account
   dettagli e contenuti desktop non correlati prima della pubblicazione.
5. Configura l'autore Git locale del repository con l'indirizzo senza risposta GitHub dell'account prima del
   primo impegno. Confermalo con `git config --local --get user.email`.
6. Configura i segreti di firma Authenticode opzionali:
   - `WINDOWS_CERTIFICATE_BASE64`: certificato PFX con codifica Base64.
   - `WINDOWS_CERTIFICATE_PASSWORD`: password PFX.

Senza un certificato di firma, i file generati continuano a funzionare, ma Windows SmartScreen potrebbe mostrare
un avviso di editore non riconosciuto. Non descrivere le build non firmate come firmate o attendibili.

## Scansione originale e Git LFS

`samples/original-scan.stl` viene tracciato tramite Git LFS perché supera i normali 100 MiB di GitHub
limite del file. Prima del primo commit, verifica:

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

Il filtro deve essere `lfs` e l'ID dell'oggetto puntatore deve corrispondere a `samples/SHA256SUMS.txt`. Il rilascio
il flusso di lavoro controlla il contenuto LFS e pubblica lo STL originale come risorsa di rilascio separata. CI utilizza
il campione normal-Git più piccolo e non scarica l'oggetto LFS.

## Testare una build di rilascio senza pubblicare

Apri **Azioni**, seleziona **Rilascia**, scegli **Esegui flusso di lavoro** e inserisci una versione numerica come
`0.1.0`. Un'esecuzione manuale carica gli artefatti del flusso di lavoro per i test ma non crea uno GitHub pubblico
Rilascio.

## Pubblica una liberatoria

Da un ramo `main` pulito e recensito:

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

Il tag avvia il flusso di lavoro di rilascio. Esso:

1. installa le dipendenze di build aggiunte;
2. genera metadati della versione Windows corrispondenti;
3. costruisce gli eseguibili GUI e CLI autonomi;
4. firma gli eseguibili quando sono configurati i segreti di firma;
5. crea il programma di installazione Inno Setup per utente;
6. firma l'installatore una volta configurato;
7. crea il file di checksum portatile ZIP e SHA-256;
8. carica gli artefatti del flusso di lavoro;
9. crea la release GitHub per il tag inviato.

Verificare il programma di installazione e l'archivio portatile su un sistema Windows pulito prima di annunciare il rilascio.
Mantieni il codice sorgente corrispondente a ogni binario distribuito disponibile sotto lo stesso tag di rilascio.
Conferma che il pulsante GitHub punti all'URL del repository pubblico finale prima di taggare il primo
rilasciare.
