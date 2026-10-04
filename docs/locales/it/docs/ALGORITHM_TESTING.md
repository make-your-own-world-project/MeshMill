# Test e contributo degli algoritmi

Gli algoritmi MeshMill dovrebbero rendere gestibili le geometrie difficili mantenendone visibili gli effetti,
misurabile e reversibile prima che venga applicato un risultato.

## Infissi di riferimento

Utilizza entrambe le versioni in bundle della geometria del campione composito:

- `samples/sample-scan.stl` è il dispositivo normal-Git più piccolo per lo sviluppo di routine, automatizzato
  controlli e apprendimento dei controlli.
- `samples/original-scan.stl` è l'apparecchiatura Git LFS completa per il comportamento di file di grandi dimensioni, livelli ridondanti,
  densità irregolare, sovrapposizione e lavoro prestazionale.

Le regioni ridondanti e dense sono caratteristiche di test intenzionali. Un test potrebbe prenderli di mira, ma
non dovrebbe dare per scontato che ogni superficie sovrapposta sia usa e getta. Aggiungere reti sintetiche compatte quando a
il cambiamento necessita di un confine noto, di una curvatura, di una topologia, di una densità o di un invariante di sovrapposizione.

## Lista di controllo di confronto

Per una modifica di un algoritmo o di un parametro, registrare:

- Versione o commit MeshMill;
- dispositivo di input e checksum;
- algoritmo, preimpostazione della qualità, destinazione e impostazioni avanzate;
- conteggi di triangoli e vertici originali e risultanti;
- percentuale di riduzione, dimensioni e deriva dimensionale;
- tempo trascorso e memoria di picco quando le prestazioni sono rilevanti;
- screenshot dalle stesse viste salvate e modalità di visualizzazione;
- cambiamenti visibili di confini, buchi, autointersezioni, sovrapposizioni o distorsioni;
- se il risultato proviene da un'operazione di mesh intera o di sola selezione.

Confrontalo con il comportamento attuale dello stesso target, non solo con un altro preset con a
conteggio di output diverso. Ispeziona le visualizzazioni di ombreggiatura, densità, wireframe e vertici, ove applicabile.

## Guida all'accettazione

Una modifica di ottimizzazione dovrebbe evitare cambiamenti dimensionali imprevisti, evidente inversione della superficie,
crepe tra regioni elaborate, perdita di confini significativi e ampie regressioni di qualità a
conteggio di output simile. I cambiamenti orientati alla densità dovrebbero dimostrare che la concentrazione rimossa lo ha fatto
non portano curvatura o topologia utile.

I risultati delle prestazioni dovrebbero identificare il processore, la capacità di memoria, l'hardware grafico, il funzionamento
sistema, dimensione dell'input e se i dati erano già memorizzati nella cache. Validazione strutturale e screenshot
supportare la revisione ma non sostituire l'ispezione da parte di contributori che abbiano familiarità con la geometria di origine.

## Test di regressione

Preferire test deterministici con tolleranze esplicite. Mantieni le nuove apparecchiature abbastanza piccole per il normale Git,
documentarne l'origine e la licenza e utilizzare la geometria sintetica quando i dati di origine reali non sono necessari.
I test dovrebbero coprire la cancellazione e il ripristino dello stato quando un'operazione può modificare la geometria.
