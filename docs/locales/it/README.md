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

MeshMill è un'applicazione desktop specifica per gestire geometrie mesh
di grandi dimensioni, ad alta densità o complesse. Offre funzionalità di ispezione rapida, analisi della densità, selezione per aree, ritaglio, eliminazione,
e riduzione controllata della mesh, senza richiedere la creazione di un account o il caricamento della geometria.

Il rendering OpenGL accelerato dalla GPU mantiene la navigazione nel viewport, la selezione dell'hardware, la visualizzazione della densità,
e ispezione interattiva reattiva. La riduzione della mesh attualmente viene eseguita in lavoratori CPU nativi separati,
mantenendo i calcoli geometrici lunghi lontano dall'interfaccia.

MeshMill supporta mesh provenienti da scanner 3D, esportazioni CAD e di modellazione, pipeline di ricostruzione,
geometrie generate proceduralmente e altre fonti STL. Prepara la geometria per editor a valle,
strumenti di produzione e altri flussi di lavoro basati su mesh. La modellazione generica, lo sculpting, l'animazione,
la gestione dei materiali e la creazione di scene esulano dal suo scopo.

## Download

Scegli il tuo sistema operativo. Ogni pacchetto è autonomo. Python, Node.js e altri
le dipendenze di sviluppo non sono richieste.

| Sistema | Download consigliato | Stato |
| --- | --- | --- |
| **Finestrex64** | **[Scarica il programma di installazione di Windows][windows-installer]** | Versione supportata | <!-- Windows -->
| Windows x64, nessuna installazione | [Scarica lo ZIP portatile][windows-portable] | Versione supportata |
| Linux x86-64 | [Scarica l'anteprima di Linux][linux-preview] | Anteprima dei primi test |
| macOS Apple silicio | [Scarica l'anteprima del silicio Apple][mac-arm-preview] | Anteprima dei primi test |
| macOS Intel | [Scarica l'anteprima di Intel Mac][mac-intel-preview] | Anteprima dei primi test |

**La maggior parte degli utenti Windows dovrebbe scegliere il programma di installazione di Windows.** Utilizza lo ZIP portatile solo quando lo fai
non desideri MeshMill installato o non disponga dell'autorizzazione per installare applicazioni.

I pacchetti Linux e macOS sono anteprime iniziali non firmate. Passano build native automatizzate e
test del fumo confezionati, ma necessitano ancora di test sull'hardware reale. Leggi il
[Note di anteprima su Linux e macOS](../../PLATFORM_TESTING.md) prima di installarli.

Windows SmartScreen o macOS Gatekeeper potrebbero avvisare della presenza di pacchetti non firmati.
Una mesh di esempio opzionale è inclusa nella versione Windows supportata: [STL][sample-mesh].
Le versioni precedenti e i checksum dei download sono disponibili su [GitHub Releases][all-releases].

[windows-installer]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-0.1.1-windows-x64-setup.exe
[windows-portable]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-0.1.1-windows-x64-portable.zip
[linux-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-linux-x86_64.tar.gz
[mac-arm-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-arm64.zip
[mac-intel-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-x86_64.zip
[sample-mesh]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-sample-scan-original.stl
[all-releases]: https://github.com/make-your-own-world-project/MeshMill/releases

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
- Viewport OpenGL con accelerazione GPU, selezione hardware e visualizzazione della densità
- Operatori nativi della geometria dello sfondo per la riduzione della mesh
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

## Ispezionare la geometria prima di ridurla

La visualizzazione ombreggiata fornisce una visione chiara della superficie e della sagoma. È utile per confrontare
conservazione della forma prima di applicare una passata di ottimizzazione.

![Vista ombreggiata di MeshMill che mostra la mesh campione in bundle](../../images/meshmill-shaded.png)

La visualizzazione Vertici espone la distribuzione dei punti effettiva. Regioni di scansione dense, aree sparse e
cambiamenti bruschi nel campionamento sono visibili senza modificare la geometria. Il pannello delle metriche espanso
tiene traccia dell'attività di CPU, memoria, GPU e elaborazione della geometria mentre si lavora con la mesh.

![Visualizzazione dei vertici di MeshMill con parametri prestazionali ampliati](../../images/meshmill-vertices.png)

La visualizzazione Wireframe mostra direttamente la struttura del triangolo. Aiuta a identificare la densità non necessaria,
triangolazione irregolare e regioni in cui la semplificazione può rimuovere una geometria sostanziale.

![Visualizzazione MeshMill Wireframe che mostra la variazione nella densità del triangolo](../../images/meshmill-wireframe.png)

## Analizzare la densità della mesh

La visualizzazione Densità mappa la densità locale relativa nel modello. Le regioni sparse rimangono fresche
regioni sempre più dense si muovono attraverso colori più luminosi, rendendo visibile a colpo d'occhio il campionamento irregolare.

![Visualizzazione della densità di MeshMill che mostra la densità relativa della mesh](../../images/meshmill-density.png)

La densità rimane disponibile mentre si valuta un'ottimizzazione provvisoria. La casella degli strumenti segnala il
algoritmo, target, conteggi di triangoli e vertici risultanti, percentuale di riduzione, dimensioni e
dimensione di output stimata prima dell'applicazione del passaggio.

![Visualizzazione della densità di MeshMill che mostra un'ottimizzazione provvisoria](../../images/meshmill-density-overview.png)

Tieni premuto il pulsante destro del mouse per ispezionare una regione attraverso la lente d'ingrandimento circolare. La vista ingrandita
rimane centrato sul puntatore e rivela la densità locale senza modificare la posizione della telecamera principale.

![Visualizzazione della densità di MeshMill con la lente di ingrandimento del viewport](../../images/meshmill-density-zoom.png)

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

Il pannello di selezione riporta i vertici, i triangoli, la condivisione della mesh selezionati cumulativi, stimati
dimensione e dimensioni. Le sue azioni ritagliano, aggiungono, ottimizzano, eliminano, fanno un passo indietro o cancellano ciò che è stato conservato
selezione senza nascondere la geometria circostante.

![MeshMill mostra una selezione regionale mantenuta e le relative statistiche sulla geometria](../../images/meshmill-crop-selection.png)

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

Il testo e la documentazione dell'interfaccia utente localizzati vengono inizialmente prodotti con una traduzione automatica esterna
servizi e controllati automaticamente per eventuali danni strutturali. La traduzione automatica può ancora esserlo
innaturale o scorretto. I madrelingua sono incoraggiati a rivedere e correggere le traduzioni
il processo di contribuzione.

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
