# Risoluzione dei problemi

## Windows blocca il download

Le build della community non firmate possono attivare Microsoft Defender SmartScreen. Confronta quello scaricato
l'hash SHA-256 del file con `SHA256SUMS.txt` dalla stessa versione GitHub. Le versioni firmate identificano
il loro editore nelle proprietà del file Windows.

## La build portatile non si avvia

Estrarre lo ZIP completo prima di eseguire `MeshMill.exe`. La directory `_internal` deve rimanere la successiva
su entrambi gli eseguibili. Non eseguire l'eseguibile dal visualizzatore ZIP.

## Si apre un grande STL come panoramica

Il working set stimato supera il budget di memoria in Impostazioni. La modalità Panoramica è intenzionalmente
sola lettura. Aumentare il budget solo quando la macchina ha memoria disponibile sufficiente, oppure ridurla
mesh prima di aprirlo per la modifica.

## Non è stata salvata una vista standard

Premi la scorciatoia per la visualizzazione modificata da Ctrl, quindi scegli **Salva** o premi Invio nella conferma
dialogo. Il salvataggio di una vista aggiorna anche quella opposta. La riga di stato riporta la vista salvata.

## Le scorciatoie di navigazione non rispondono

Chiudere prima qualsiasi finestra di dialogo modale. Controlla o reimposta le scorciatoie in Impostazioni se sono state personalizzate. Il
le scorciatoie di visualizzazione predefinite utilizzano Inserisci, Home, Pagina su, Elimina, Fine e Pagina giù.

## Creare un log diagnostico di orientamento locale

La registrazione diagnostica è disabilitata per impostazione predefinita. Per registrare localmente il routing della tastiera e lo stato della fotocamera:

```powershell
.\MeshMill.exe --diagnostic-log ".\orientation-session.jsonl" "C:\path\mesh.stl"
```

Il registro può contenere il percorso del file aperto. Rivedilo e correggilo prima di condividerlo. La geometria della mesh no
scritto nel registro.

## Segnala un problema

Include la versione MeshMill, la versione Windows, il modello GPU, conteggio dei triangoli mesh, azione esatta
sequenza e se è stato utilizzato il programma di installazione o il pacchetto portatile. Utilizzare il campione ridistribuibile
rete quando possibile. Non allegare scansioni private o registri diagnostici senza prima esaminarli.
