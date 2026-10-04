# Tabella di marcia MeshMill

## Supporto della piattaforma

Windows è la piattaforma confezionata iniziale. L'architettura dell'applicazione e i formati mesh lo sono
multipiattaforma e le versioni future dovrebbero aggiungere pacchetti nativi Linux e macOS. Lavoro su piattaforma
include packaging, integrazione delle applicazioni, metriche hardware, comportamento del file system e automazione
test di rilascio preservando lo stesso progetto e i flussi di lavoro STL su ogni sistema supportato.

- Aggiungi pacchetti Linux x86-64 e copertura CI.
- Aggiungi macOS pacchetti Apple Silicon e x86-64, firma, autenticazione e copertura CI.
- Aggiungi provider di metriche CPU, memoria e GPU nativi della piattaforma dietro un'interfaccia condivisa.
- Mantieni portatili le impostazioni salvate, le mappature della tastiera, il comportamento della riga di comando e i dati di progetto.

Questa tabella di marcia registra il lavoro pianificato. Non descrive le funzionalità della versione corrente.

## Ambito

MeshMill gestisce la geometria, la densità della mesh, la densità dei punti, l'ottimizzazione, la pulizia, la convalida e STL
scambiare file mesh di grandi dimensioni o pesanti che rimangono utili nei flussi di lavoro di modifica downstream.

Modellazione generica, scultura, pittura, animazione, rendering, composizione di scene, materiali,
rigging e altri sistemi di creazione di contenuti sono fuori da questa tabella di marcia. Si applica la sintesi distribuita
alle operazioni di gestione della mesh di MeshMill e non espande il prodotto in un editor generale.

## Geometria di riferimento

La mesh composita in bundle è lo strumento di sviluppo comune per gli algoritmi e la tabella di marcia attuali
lavoro. I suoi strati intenzionalmente ridondanti e la densità irregolare supportano confronti ripetibili
qualità di riduzione, analisi della densità, gestione delle sovrapposizioni, operazioni regionali, elaborazione out-of-core,
e sintesi futura. Le implementazioni della tabella di marcia dovrebbero riportare risultati rispetto a questo dispositivo e piccoli
mesh di regressione appositamente costruite, anziché ottimizzare il comportamento per un solo modello.

## Spazi di lavoro Multi-STL e sintesi statistica

Uno spazio di lavoro dovrebbe accettare più input STL come oggetti di origine separati e visibili in modo indipendente.
MeshMill dovrebbe allineare tali sorgenti, misurare il loro accordo geometrico e sintetizzarne uno utilizzabile
mesh senza conservare superfici interne duplicate o geometrie di sovrapposizione ripetute.

Comportamento pianificato:

- aggiungere, rimuovere, nascondere, isolare, riordinare e ispezionare più origini STL in un unico spazio di lavoro;
- conservare l'identità dell'origine, le unità, le trasformazioni, i limiti, la risoluzione e la cronologia delle operazioni;
- fornire la registrazione automatica con controlli di allineamento manuale e qualità di adattamento misurabile;
- partizionare le fonti in regioni spaziali prima del confronto in modo che gli input di grandi dimensioni rimangano limitati;
- analizzare l'occupazione, la distanza dalla superficie più vicina, l'accordo normale, la densità locale, la varianza e
  conteggio delle osservazioni in regioni sovrapposte;
- classificare superfici corrispondenti, superfici in conflitto, rumore di scansione, spazi vuoti e geometria univoca;
- consolidare le superfici statisticamente concordanti in una superficie rappresentativa con registrazione
  fiducia invece di impilare triangoli duplicati;
- rimuovere la geometria chiusa, coincidente e condivisa che non fornisce dettagli sulla forma esterna;
- mantenere la geometria della sorgente non sovrapposta ed esporre regioni ambigue per la revisione visiva;
- consentire la ponderazione per sorgente e per regione quando una scansione è più pulita o più dettagliata;
- convalidare l'impermeabilità, i confini, le normali, le dimensioni e la topologia dopo la sintesi;
- registrare la provenienza della fonte e i parametri di sintesi in modo che la mesh combinata sia riproducibile;
- visualizzare in anteprima il conteggio dei triangoli previsto, i limiti, la sovrapposizione rimossa e la distribuzione di confidenza prima
  confermando il risultato sintetizzato.

Questo flusso di lavoro dovrebbe utilizzare lo stesso indice spaziale esterno e il modello di unità di lavoro pianificato per grandi aziende
maglie. Anche il confronto statistico e il consolidamento delle sovrapposizioni dovrebbero essere distribuibili a livello locale
o nodi remoti MeshMill.

## Sintesi distribuita

Un cluster MeshMill dovrebbe coordinare più nodi che operano in parallelo su più nodi
postazioni di lavoro. Un nodo può ispezionare, selezionare, ridurre, convalidare, riparare o combinare una regione assegnata o
unità di lavoro. I contributi rimangono versioni indipendenti finché non vengono rivisti e incorporati
in una versione di oggetto condiviso.

Il sistema dovrebbe supportare:

- contributi simultanei da più operatori e nodi automatizzati;
- input, parametri, dipendenze e output deterministici delle unità di lavoro;
- pianificazione basata sulle funzionalità basata su CPU, GPU, memoria, algoritmi e carico corrente;
- partizionamento in base alle dipendenze di mesh, regioni, passaggi di convalida e fasi di sintesi;
- code durevoli con pausa, ripresa, annullamento, nuovo tentativo, riassegnazione e ripristino in caso di errore;
- artefatti indirizzati al contenuto e controlli di integrità tra i nodi;
- sintesi riproducibile da un insieme registrato di versioni di contributi accettati;
- postazioni di lavoro offline o connesse in modo intermittente che possono essere sincronizzate successivamente;
- operazione local-first con controllo esplicito sui nodi partecipanti e sui dati di progetto condivisi.

## Collaborazione con versioni

Ogni contributo deve registrare la versione dell'oggetto principale, la regione o l'unità di lavoro selezionata, l'operazione,
parametri, identità del nodo, timestamp, dipendenze, risultati di convalida e checksum di output.

Comportamento di collaborazione pianificato:

- i progetti contengono oggetti, rami, checkpoint, contributi e versioni sintetizzate;
- i contributori possono lavorare dalla stessa versione principale senza sovrascriversi a vicenda;
- i contributi non sovrapposti possono unirsi automaticamente dopo la convalida;
- la geometria sovrapposta o le dipendenze incompatibili creano un conflitto esplicito;
- i conflitti forniscono confronto visivo, scelta a livello di regione, rebase, riesecuzione e risoluzione manuale;
- gli stati di revisione includono in sospeso, accettato, rifiutato, sostituito, in conflitto e incorporato;
- il manifesto di sintesi finale identifica ogni contributo e dipendenza incorporati.

## Interfaccia utente di coordinamento

L'applicazione desktop dovrebbe gestire il lavoro distribuito senza richiedere una riga di comando separata
o flusso di lavoro di amministrazione del server. Le visualizzazioni pianificate includono:

- **Progetti:** oggetti, rami, versioni, contributori e stato della sintesi.
- **Cluster:** workstation e nodi connessi, funzionalità, integrità, carico e assegnazione corrente.
- **Coda:** unità di lavoro in sospeso, attive, in pausa, bloccate, non riuscite e completate.
- **Contributi:** autore, nodo, versione principale, regione interessata, parametri, controlli e stato di revisione.
- **Confronta:** viste 3D sincronizzate, differenze geometriche, metriche e ispezione dei confini.
- **Conflitti:** regioni sovrapposte, conflitti di dipendenza, scelte di risoluzione e risultati di convalida.
- **Sintesi:** grafico delle dipendenze, progresso aggregato, versioni di contributo selezionate e output finale.
- **Cronologia:** grafico di diramazione, checkpoint, unioni, versioni sintetizzate e manifest di riproducibilità.

La finestra dovrebbe mostrare la proprietà, le regioni assegnate, il lavoro completato, le modifiche in sospeso, i conflitti,
e differenze di versione senza alterare la mesh sottostante.

## Coordinamento e trasporto

La prima fase di progettazione dovrebbe definire i limiti del protocollo prima di selezionare un trasporto. Il protocollo
dovrebbe separare i metadati di coordinamento dagli artefatti mesh di grandi dimensioni, supportare il trasferimento ripristinabile e
rimangono utilizzabili su una rete locale senza un account esterno o un servizio ospitato.

Concetti di coordinamento richiesti:

- elezione del coordinatore o di un coordinatore esplicitamente selezionato;
- rilevamento dei nodi e registrazione manuale dei nodi;
- sessioni autenticate e autorizzazione nell'ambito del progetto;
- locazioni e heartbeat per la proprietà dei lavori;
- presentazione del lavoro idempotente e accettazione del risultato;
- negoziazione della versione tra diverse versioni di MeshMill;
- eventi strutturati per avanzamento, registri, convalida, errori e tentativi;
- ripristino dopo l'interruzione del coordinatore, della workstation, della rete o del nodo.

## Fasi di consegna

### Fase 0: elaborazione a maglia larga out-of-core

L'indice, lo streaming, la cache, l'unità di lavoro e il contratto di sicurezza sono documentati in
[`docs/OUT_OF_CORE.md`](docs/OUT_OF_CORE.md).

- Stimare il conteggio dei triangoli e la memoria di lavoro prima di allocare la mesh completa.
- Apri file binari STL di grandi dimensioni come panoramiche di navigazione delimitate e campionate uniformemente.
- Partiziona la geometria a piena risoluzione in cubi spaziali con confini di sovrapposizione deterministica.
- Leggi, analizza e ottimizza contemporaneamente cubi indipendenti entro CPU e limiti di memoria.
- Trasmetti in streaming livelli di visualizzazione da grossolani a fini invece di richiedere la mesh completa in memoria.
- Disegna lo stato del cubo direttamente nella finestra: in coda, in lettura, in elaborazione, completato e non riuscito.
- Mostra i progressi per cubo riempiendo ciascun cubo e mantieni una visualizzazione dell'intero oggetto di alto livello.
- Assembla i cubi elaborati con convalida dei limiti, rimozione dei duplicati e impostazioni riproducibili.
- Estendi lo scheduler del cubo locale in unità di lavoro di sintesi distribuite nelle fasi successive.

### Fase 1: fondazione locale con versione

- Definire i formati oggetto, operazione, contributo, ramo e manifest.
- Aggiungi spazi di lavoro multi-STL con visibilità per origine, trasformazioni, metadati e provenienza.
- Aggiungi parametri di qualità di registrazione e classificazione di sovrapposizione spaziale.
- Sintetizza superfici statisticamente concordanti rimuovendo la geometria duplicata e chiusa.
- Aggiungi una revisione visiva per conflitti, lacune, sicurezza e geometria univoca per un'unica fonte.
- Mantieni la cronologia locale tra le sessioni dell'applicazione.
- Aggiungi mesh visive e confronti tra regioni.
- Rendere le operazioni deterministiche e riproducibili in modo indipendente.

### Fase 2: nodi locali coordinati

- Esegui i nodi di lavoro su una workstation.
- Aggiungi accodamento, reporting sulle capacità, assegnazione di lavoro e annullamento.
- Visualizza lo stato del nodo e dell'unità di lavoro nell'interfaccia utente di MeshMill.
- Convalidare il partizionamento e l'assemblaggio dei risultati localmente.

### Fase 3: sintesi multi-workstation

- Aggiungi il rilevamento e la registrazione della LAN autenticata.
- Trasferisci input e risultati di lavoro indirizzati ai contenuti con il supporto del curriculum.
- Coordinare il lavoro simultaneo su più postazioni di lavoro.
- Recuperare le assegnazioni dopo un guasto del nodo o della rete.

### Fase 4: controllo delle versioni collaborativo

- Aggiungi contributori, rami, stati di revisione e autorizzazioni.
- Unisci contributi non sovrapposti.
- Rileva e risolvi conflitti di sovrapposizione o dipendenza.
- Sintetizzare i contributi selezionati in una versione oggetto riproducibile.

### Fase 5: rafforzamento della produzione

- Aggiungi test di compatibilità del protocollo e gestione di versioni miste.
- Aggiungi test di controllo, integrità, corruzione, interruzione e ripristino.
- Confronta le prestazioni di pianificazione, partizionamento, trasferimento, unione e sintesi.
- Distribuzione, backup, migrazione e ripristino degli incidenti dei documenti.
