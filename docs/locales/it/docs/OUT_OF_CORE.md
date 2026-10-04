# Architettura mesh out-of-core

L'attuale protezione per file di grandi dimensioni di MeshMill stima la memoria di lavoro prima di allocarne una completa
maglia. I file che superano il budget configurato possono essere aperti come panoramiche di navigazione limitate. An
la panoramica è una geometria campionata, è visibilmente identificata come tale e non può essere modificata o esportata come
sebbene fosse la fonte completa.

Il vero dettaglio dipendente dallo zoom richiede un indice spaziale persistente. Il disegno seguente lo definisce
successiva fase di attuazione.

## Formato indice

Ogni mesh di origine riceve una directory `.meshmill-index` con versione contenente:

- `manifest.json`, con dimensione della sorgente, ora di modifica, hash dei contenuti campionati, limiti,
  conteggio dei triangoli, versione dell'indice, precisione delle coordinate e descrizioni dei livelli;
- tessere spaziali indirizzate dal livello ottree e dal codice Morton;
- una mesh di visualizzazione grossolana per ogni tessera madre occupata;
- record triangolari a piena risoluzione in tessere fogliari; E
- proprietà dei confini e metadati di sovrapposizione utilizzati durante le operazioni regionali e l'assemblaggio.

La creazione dell'indice legge l'origine in sequenza in blocchi delimitati. Scrive sequenze di tessere temporanee e
pubblica in modo atomico il manifest dopo che ogni file richiesto ha superato la convalida. Un interrotto o
l'indice obsoleto viene rilevato dal suo manifest e può essere ripreso o ricostruito senza aprire il file completo
maglia in memoria.

## Streaming della vista

Il viewport seleziona i riquadri utilizzando il tronco della fotocamera e l'errore di spazio sullo schermo. Le tessere genitore grossolane lo sono
mostrato per primo. I riquadri secondari visibili li sostituiscono man mano che la telecamera si avvicina, mentre è fuori dallo schermo e
le piastrelle a basso impatto rimangono grossolane. RAM e VRAM hanno budget indipendenti e sono utilizzati meno di recente
cache. Il rilascio dei dettagli non rilascia mai la rappresentazione grossolana dell'intero oggetto.

Lo scheduler registra questi stati delle tessere: in coda, in lettura, in elaborazione, in caricamento, residente, non riuscito,
e cancellato. La finestra può colorare i cubi per stato e riempire ciascun cubo in proporzione al suo
progresso. La cancellazione rimuove i risultati parziali e lascia attiva l'ultima rappresentazione completa.

## Elaborazione e capacità

Un'unità di lavoro locale è una tessera più la sovrapposizione deterministica richiesta dal suo funzionamento. Concorrenza
è limitato dallo RAM attualmente disponibile, dalla percentuale di memoria configurata, dal conteggio del processore logico e
dimensione misurata dell’unità di lavoro. Il caricamento e la visualizzazione di GPU hanno un budget VRAM separato. Segnalato parallelo
la capacità è una stima finché non vengono misurate le piastrelle rappresentative.

Le operazioni mantengono un proprietario per ogni elemento di confine. L'assemblea convalida i confini condivisi,
rimuove i duplicati, controlla conteggi e limiti e registra i parametri esatti utilizzati. Lo stesso lavoro
il formato dell'unità e del risultato può essere successivamente pianificato tra i nodi di sintesi distribuiti.

## Norme di sicurezza

- Un campione globale è etichettato come panoramica, non come dettaglio della finestra a risoluzione completa.
- Una panoramica non può sovrascrivere o esportare come mesh di origine completa.
- Le richieste a pieno carico che superano il budget attuale richiedono una scelta esplicita.
- La generazione dell'indice, l'elaborazione delle tessere e l'assemblaggio rimangono cancellabili e preservano il precedente
  stato completo.
- I valori di capacità sono stime e identificano se descrivono il motore attuale o pianificato
  esecuzione a piastrelle parallele.
