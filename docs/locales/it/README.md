# MeshMill

![MeshMill viewport con ombreggiatura](../../images/meshmill-shaded.png)

MeshMill è un'applicazione desktop specifica per gestire geometrie mesh
di grandi dimensioni, ad alta densità o complesse. Offre funzionalità di ispezione rapida, analisi della densità, selezione per aree, ritaglio, eliminazione,
e riduzione controllata della mesh, senza richiedere la creazione di un account o il caricamento della geometria.

Il rendering OpenGL con accelerazione GPU mantiene reattivi la navigazione della vista, la selezione hardware, la visualizzazione della densità e l’ispezione interattiva. La riduzione della mesh viene attualmente eseguita in processi CPU nativi separati, così i calcoli geometrici prolungati non bloccano l’interfaccia.

MeshMill supporta mesh provenienti da scanner 3D, esportazioni CAD e di modellazione, pipeline di ricostruzione,
geometrie generate proceduralmente e altre fonti STL. Prepara la geometria per editor a valle,
strumenti di produzione e altri flussi di lavoro basati su mesh. La modellazione generica, lo sculpting, l'animazione,
la gestione dei materiali e la creazione di scene esulano dal suo scopo.

## Download

Scarica uno di questi file dalla sezione [GitHub Releases](../../releases):

- `MeshMill-<version>-windows-x64-setup.exe`: installer per singolo utente con voci nel menu Start e
  collegamenti opzionali sul desktop.
- `MeshMill-<version>-windows-x64-portable.zip`: applicazione portatile. Estrai l'intero archivio,
  quindi avvia `MeshMill.exe`.

Entrambi i pacchetti includono il runtime dell'applicazione. Gli utenti finali non installano le dipendenze Python, Node.js o
Linux. (Windows) (Windows)
La versione iniziale supporta macOS 10 e Windows 11 su hardware x64.

Sono previsti pacchetti e Windows; i formati del prodotto e dei file non sono specifici per.
Le build della community non firmate potrebbero visualizzare un avviso SmartScreen di `SHA256SUMS.txt`.

## I checksum delle release sono elencati

1. in STL accanto a ciascuna release.
2. Guida rapida
3. Apri un.
4. Esaminalo nelle modalità di visualizzazione Shaded, Density, Wireframe o Vertices.
5. Scegli un livello di qualità, un algoritmo e un numero target di triangoli.
6. Seleziona **Optimize** per calcolare un risultato. (`Ctrl+S`)

Confronta le mesh originale e ottimizzata, quindi seleziona **Apply** per confermare l'operazione. (MeshMill)

## Seleziona **Save current state** o premi.

- STL non avvia mai l'ottimizzazione semplicemente perché un file o un'impostazione è cambiato. (STL)
- Riduzione Fast QEM con bilanciamento della densità e conservazione di forma e topologia
- Modalità di visualizzazione: ombreggiata, densità, wireframe e vertici
- Obiettivi automatici basati sulla geometria anziché su un limite fisso di triangoli
- Selezione di poligoni con modalità additiva e multi-regione
- Ritaglio, eliminazione o ottimizzazione limitati alla sola regione selezionata
- Confronto tra mesh originale, precedente e corrente (con caching)
- Funzioni Annulla e Ripristina per le modifiche geometriche confermate
- Variazione dimensionale, percentuale di riduzione e dimensione stimata dell'output
- Unità di misura visualizzabili: millimetri, centimetri, metri, pollici e piedi
- Metriche relative a CPU, memoria, GPU e attività geometrica
- Caricamento di una panoramica limitata quando un file STL binario supera il limite di memoria configurato
- Applicazioni con interfaccia grafica (GUI) e da riga di comando
- Elaborazione locale senza dipendenze da account, telemetria, caricamenti o cloud

![Visualizzazione densità MeshMill](../../images/meshmill-density.png)

## Controlli di visualizzazione

| Input | Azione |
| --- | --- |
| Trascinamento con tasto centrale | Orbita |
| Shift + trascinamento con tasto centrale | Panoramica |
| Rotellina del mouse | Zoom verso il puntatore |
| Ctrl + rotellina del mouse | Rotazione oraria o antioraria |
| Tasti freccia | Orbita attorno al centro della vista |
| Ctrl + tasti freccia | Panoramica |
| Ctrl + Shift + Su/Giù | Zoom |
| Ctrl + Maiusc + Sinistra/Destra | Rotolo |
| `F1` / `F2` / `F3` / `F4` | Ombreggiato / Densità / Wireframe / Vertici |
| Tieni premuto il tasto destro del mouse | Lente d'ingrandimento |
| Maiusc + clic con il pulsante sinistro del mouse | Aggiungi o rimuovi punti del righello |
| Ctrl + trascinamento sinistro | Disegna un poligono di selezione |
| `Ctrl+C` | Aggiungi il poligono alla selezione salvata |
| `Ctrl+X` | Ritaglia alla selezione |
| `Ctrl+Space` | Ottimizza la selezione |
| `Delete` | Elimina la selezione |
| `Escape` | Cancella la selezione attiva o il righello |
| `Ctrl+Z` / `Ctrl+Y` | Annulla/ripristina |
| `Ctrl+S` | Salva lo stato corrente della mesh |

I tasti della vista standard seguono il blocco di navigazione a sei tasti:

| Chiave | Visualizza | Ctrl + tasto |
| --- | --- | --- |
| `Insert` | Sinistra | Imposta l'orientamento corrente su Sinistra |
| `Home` | Davanti | Imposta l'orientamento corrente come Frontale |
| `Page Up` | Giusto | Imposta l'orientamento corrente su Destra |
| `Delete` | In alto quando non esiste alcuna selezione | Imposta l'orientamento corrente come Superiore |
| `End` | Indietro | Imposta l'orientamento corrente su Indietro |
| `Page Down` | In basso | Imposta l'orientamento corrente come Inferiore |

Il salvataggio di una vista aggiorna anche la vista opposta. Sinistra e destra, davanti e dietro e sopra e sotto
rimanere accoppiati. Nella finestra di dialogo di conferma, **Salva** è l'azione predefinita, quindi Invio salva il file
orientamento. La parte anteriore viene visualizzata nella parte superiore delle visualizzazioni Superiore e Inferiore.

Le scorciatoie possono essere modificate o ripristinate in Impostazioni.

## Flusso di lavoro di selezione

Tieni premuto Ctrl e trascina a sinistra per disegnare un poligono. Trascina gli angoli per rimodellarlo, fai clic con il pulsante sinistro del mouse su un bordo per aggiungere a
punto o fare clic con il pulsante destro del mouse su un bordo per rimuoverne uno. Aggiungi più regioni con `Ctrl+C`. Muovendo la telecamera si nasconde
il poligono dello screen-space mantenendo la geometria selezionata.

L'ottimizzazione con una selezione attiva influisce solo su quella selezione. Il risultato resta provvisorio
finché non viene selezionato **Applica**. **Annulla** scarta il risultato provvisorio e mantiene così la selezione
si può provare un'altra configurazione. Le operazioni di ritaglio ed eliminazione diventano normali modifiche mesh annullabili.

## Maglie larghe

Prima di allocare un STL binario, MeshMill confronta la sua memoria di lavoro stimata con quella configurata
bilancio della memoria. Un file sopra il budget si apre come panoramica limitata e di sola lettura. La panoramica riporta
il conteggio completo dei triangoli di origine ma disabilita la modifica e l'esportazione perché si tratta di un campione, non dell'intero
oggetto. È pianificata l'elaborazione out-of-core indicizzata e dipendente dallo zoom
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md).

## Riga di comando

`MeshMillCLI.exe` è incluso in entrambi i pacchetti di rilascio:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

Esegui `.\MeshMillCLI.exe --help` per tutte le opzioni. MeshMill rifiuta di sovrascrivere il file di input.

## Geometria del campione

Sono disponibili due versioni dell'esempio di sviluppo. Il campione è una mesh composita con
strati intenzionali di geometria ridondante e densità variata. Dà alle persone senza scanner a
strumento realistico per confrontare algoritmi, ispezionare la densità, esercitare operazioni regionali,
e lo sviluppo di funzionalità della roadmap. MeshMill non richiede input scansionato.

| File | Triangoli | Taglia | Consegna | Ideale per |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249.999 | 11,9 MiB | Git normale | Valutazione rapida, CI e apprendimento dei controlli |
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4.126.315| 196,8 MiB | Git LFS | Test della geometria della sorgente densa e delle prestazioni a maglia larga |

Il campione più piccolo viene scaricato con ogni clone normale. L'originale intatto è facoltativo e
gestito tramite Git LFS in modo da non gonfiare la cronologia ordinaria del repository. Il desktop GitHub include
Git LFS. Gli utenti della riga di comando possono installare Git LFS ed eseguire:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

Le versioni contrassegnate pubblicano anche l'originale STL come download diretto per le persone che non utilizzano Git.
Vedere [`samples/README.md`](../../../samples/README.md) per provenienza, dimensioni e checksum.

I contributori dell'algoritmo dovrebbero leggere anche il file
[guida al test dell'algoritmo](docs/ALGORITHM_TESTING.md) prima di confrontare o modificare la riduzione
comportamento.

## Unità STL

STL non codifica un'unità. La modifica delle unità del modello modifica le etichette e le misurazioni senza ridimensionamento
le coordinate salvate. Seleziona l'unità che descrive la geometria di origine.

## Privacy

MeshMill legge e scrive file locali. Non contiene account, telemetria, caricamento, pubblicità o
funzionalità di elaborazione cloud. L'attuale implementazione della metrica GPU utilizza le prestazioni Windows locali
contatori. Sono previsti fornitori di metriche native equivalenti per Linux e macOS.

Per la risoluzione dei problemi diagnostici, gli sviluppatori possono avviare la GUI con
`--diagnostic-log <local-file.jsonl>`. Il registro registra localmente il routing degli input e lo stato della telecamera ed è così
disabilitato durante il normale utilizzo.

## Sviluppo e rilascio

- [Contribuire](CONTRIBUTING.md)
- [Processo di rilascio](RELEASING.md)
- [Tabella di marcia](ROADMAP.md)
- [Risoluzione dei problemi](docs/TROUBLESHOOTING.md)
- [Avvisi di terze parti](THIRD_PARTY_NOTICES.md)

## Supporta MeshMill

MeshMill è sviluppato e mantenuto in modo indipendente. Leggi
[perché è importante supportare questo lavoro](SUPPORT.md) o supportare lo sviluppo continuo
[Offrimi un caffè](https://buymeacoffee.com/tednv).

MeshMill è concesso in licenza sotto la GNU General Public License, versione 3 o successiva. Vedi
[`LICENSE`](../../../LICENSE).
