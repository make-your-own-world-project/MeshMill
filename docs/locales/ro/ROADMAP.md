# MeshMill foaie de parcurs

## Suport platformă

Windows este platforma inițială ambalată. Arhitectura aplicației și formatele de plasă sunt
multi-platformă, iar versiunile viitoare ar trebui să adauge pachete native Linux și macOS. Munca pe platformă
include ambalarea, integrarea aplicațiilor, valorile hardware, comportamentul sistemului de fișiere și automatizarea
testarea lansării, păstrând în același timp același proiect și fluxurile de lucru STL pe fiecare sistem acceptat.

- Validați pachetul de previzualizare Linux x86-64 în distribuții, medii desktop, afișaj
  servere și drivere GPU înainte de a-l promova la stabil.
- Validați pachetele de previzualizare macOS Apple și x86-64 pe hardware real, apoi adăugați Dezvoltator
  Semnarea actului de identitate și legalizarea înainte de a le promova la stabil.
- Adăugați furnizori de valori CPU, memorie și GPU nativi pentru platformă în spatele unei interfețe partajate.
- Păstrați setările salvate, mapările tastaturii, comportamentul liniei de comandă și datele de proiect portabile.

Această foaie de parcurs înregistrează lucrările planificate. Nu descrie caracteristicile din versiunea curentă.

## Domeniul de aplicare

MeshMill gestionează geometria, densitatea rețelei, densitatea punctelor, optimizarea, curățarea, validarea și STL
schimb, astfel încât fișierele cu rețea mari sau grele rămân utile în fluxurile de lucru de editare din aval.

Modelare de uz general, sculptură, pictură, animație, redare, compoziție scene, materiale,
trucaj și alte sisteme de creare de conținut sunt în afara acestei foi de parcurs. Se aplică sinteza distribuită
la operațiunile de gestionare a rețelei MeshMill și nu extinde produsul într-un editor general.

## Geometrie de referință

Mesh-ul compozit combinat este dispozitivul comun de dezvoltare pentru algoritmii și foaia de parcurs actuale
munca. Straturile sale redundante în mod intenționat și densitatea neuniformă permit comparații repetabile ale
reducerea calității, analiza densității, manipularea suprapunerii, operațiuni regionale, procesare în afara nucleului,
si sinteza viitoare. Implementările foii de parcurs ar trebui să raporteze rezultate în raport cu acest program și mici
rețele de regresie create special, mai degrabă decât optimizarea comportamentului pentru un singur model.

## Spații de lucru multi-STL și sinteză statistică

Un spațiu de lucru ar trebui să accepte mai multe intrări STL ca obiecte sursă separate, vizibile independent.
MeshMill ar trebui să alinieze acele surse, să le măsoare acordul geometric și să sintetizeze una utilizabilă
plasă fără a reține suprafețele interne duplicate sau geometria de suprapunere repetă.

Comportament planificat:

- adăugați, eliminați, ascundeți, izolați, reordonați și inspectați mai multe surse STL într-un singur spațiu de lucru;
- păstrează identitatea sursei, unitățile, transformările, limitele, rezoluția și istoricul operațiunilor;
- asigura înregistrarea automată cu controale manuale de aliniere și calitate măsurabilă a potrivirii;
- partiționați sursele în regiuni spațiale înainte de comparare, astfel încât intrările mari să rămână mărginite;
- analizați gradul de ocupare, distanța cea mai apropiată de suprafață, acordul normal, densitatea locală, varianța și
  numărul de observații în regiuni suprapuse;
- clasifică suprafețele potrivite, suprafețele conflictuale, zgomotul de scanare, golurile și geometria unică;
- consolidarea suprafețelor de acord statistic într-o suprafață reprezentativă cu înregistrate
  încredere în loc de a stivui triunghiuri duplicat;
- eliminați geometria închisă, coincidentă și comună care nu contribuie cu detalii de formă exterioară;
- păstrează geometria sursă care nu se suprapun și expune regiuni ambigue pentru revizuire vizuală;
- permite ponderarea per sursă și per regiune atunci când o scanare este mai curată sau mai detaliată;
- validați etanșeitatea, limitele, normalele, dimensiunile și topologia după sinteză;
- înregistrați proveniența sursei și parametrii de sinteză, astfel încât plasa combinată să fie reproductibilă;
- previzualizați numărul de triunghi așteptat, limitele, suprapunerea eliminată și distribuția de încredere înainte
  comiterea rezultatului sintetizat.

Acest flux de lucru ar trebui să utilizeze același index spațial din afara nucleului și același model de unitate de lucru planificat pentru mari
ochiuri. Comparația statistică și consolidarea suprapunerii ar trebui, de asemenea, să fie distribuite la nivel local
sau noduri MeshMill la distanță.

## Sinteză distribuită

Un cluster MeshMill ar trebui să coordoneze mai multe noduri care operează în paralel peste mai multe
posturi de lucru. Un nod poate inspecta, selecta, reduce, valida, repara sau combina o regiune alocată sau
unitate de lucru. Contribuțiile rămân versiunea independentă până când sunt revizuite și încorporate
într-o versiune de obiect partajată.

Sistemul ar trebui să suporte:

- contribuții concomitente de la mai mulți operatori și noduri automate;
- intrări, parametri, dependențe și ieșiri deterministe ale unității de lucru;
- programare bazată pe CPU, GPU, memorie, algoritmi și încărcare curentă;
- partiționarea conștientă de dependență a rețelelor, regiunilor, trecerilor de validare și etapelor de sinteză;
- cozi durabile cu pauză, reluare, anulare, reîncercare, reatribuire și recuperare a erorilor;
- artefacte abordate de conținut și verificări de integritate între noduri;
- sinteză reproductibilă dintr-un set înregistrat de versiuni de contribuții acceptate;
- stații de lucru offline sau conectate intermitent care se pot sincroniza mai târziu;
- operațiune locală mai întâi cu control explicit asupra nodurilor participante și a datelor de proiect partajate.

## Colaborare cu versiuni

Fiecare contribuție ar trebui să înregistreze versiunea obiectului părinte, regiunea sau unitatea de lucru selectată, operațiunea,
parametrii, identitatea nodului, marcajele de timp, dependențele, rezultatele validării și suma de verificare a ieșirii.

Comportamentul de colaborare planificat:

- proiectele conțin obiecte, ramuri, puncte de control, contribuții și versiuni sintetizate;
- colaboratorii pot lucra din aceeași versiune părinte fără a se suprascrie unul pe celălalt;
- contribuțiile care nu se suprapun pot fuziona automat după validare;
- geometria suprapusă sau dependențele incompatibile creează un conflict explicit;
- conflictele oferă comparație vizuală, alegere la nivel de regiune, rebazare, reexecuție și rezolvare manuală;
- stările de revizuire includ în așteptare, acceptate, respinse, înlocuite, conflictuale și încorporate;
- manifestul de sinteză finală identifică fiecare contribuție și dependență încorporate.

## UI de coordonare

Aplicația desktop ar trebui să gestioneze munca distribuită fără a necesita o linie de comandă separată
sau fluxul de lucru de administrare a serverului. Vizualizările planificate includ:

- **Proiecte:** obiecte, ramuri, versiuni, colaboratori și starea sintezei.
- **Cluster:** stații de lucru și noduri conectate, capabilități, sănătate, încărcare și alocare curentă.
- **Coadă:** unități de lucru în așteptare, active, întrerupte, blocate, eșuate și finalizate.
- **Contribuții:** autor, nod, versiune părinte, regiunea afectată, parametri, verificări și stare de revizuire.
- **Comparați:** vederi 3D sincronizate, diferențe de geometrie, valori și inspecție a limitelor.
- **Conflicte:** regiuni suprapuse, conflicte de dependență, opțiuni de rezolvare și rezultate de validare.
- **Sinteză:** graficul dependenței, progresul agregat, versiunile de contribuție selectate și rezultatul final.
- **Istoric:** grafic de ramuri, puncte de control, îmbinări, versiuni sintetizate și manifeste de reproductibilitate.

Fenestra de vizualizare ar trebui să arate calitatea de proprietar, regiunile alocate, lucrările finalizate, modificările în așteptare, conflicte,
și diferențele de versiuni fără a modifica rețeaua de bază.

## Coordonare si transport

Prima fază de proiectare ar trebui să definească limitele protocolului înainte de a selecta un transport. Protocolul
ar trebui să separe metadatele de coordonare de artefactele rețele mari, să accepte transferul reluabil și
rămâne utilizabil într-o rețea locală fără un cont extern sau un serviciu găzduit.

Concepte de coordonare necesare:

- alegerea coordonatorului sau un coordonator selectat în mod explicit;
- descoperirea nodurilor și înregistrarea manuală a nodurilor;
- sesiuni autentificate și autorizare pentru proiect;
- leasing și bătăi de inimă pentru proprietatea muncii;
- depunerea muncii idempotente și acceptarea rezultatului;
- negocierea versiunii între diferite versiuni MeshMill;
- evenimente structurate pentru progres, jurnale, validare, eșecuri și reîncercări;
- recuperare după întreruperea coordonatorului, stației de lucru, rețelei sau nodului.

## Fazele de livrare

### Faza 0: procesare în afara miezului cu ochiuri mari

Indexul, streamingul, memoria cache, unitatea de lucru și contractul de siguranță sunt documentate în
[`docs/OUT_OF_CORE.md`](docs/OUT_OF_CORE.md).

- Estimați numărul de triunghi și memoria de lucru înainte de a aloca rețeaua completă.
- Deschideți fișiere STL binare supradimensionate ca prezentări de navigare delimitate, eșantionate uniform.
- Partiționați geometria cu rezoluție completă în cuburi spațiale cu granițe de suprapunere deterministe.
- Citiți, analizați și optimizați cuburile independente simultan în limitele CPU și de memorie.
- Evaluați implementări de calcul GPU pentru etapele de reducere, cum ar fi evaluarea erorilor, candidat
  punctare, interogări spațiale și procesare independentă a unității de lucru. Descărcați o etapă numai atunci când aceasta
  oferă o viteză măsurabilă de la capăt la capăt sau un beneficiu de memorie fără a reduce determinismul, plasa
  calitate, garanții de topologie sau compatibilitate cu sistemele cărora le lipsește un GPU adecvat.
- Transmiteți în flux niveluri de vizualizare grosieră până la fine, în loc să solicitați rețeaua completă în memorie.
- Desenați starea cubului direct în fereastra de vizualizare: în coadă, citit, procesare, finalizat și eșuat.
- Afișați progresul pe cub umplând fiecare cub și păstrați o vizualizare la nivel înalt a întregului obiect.
- Asamblați cuburi procesate cu validarea limitelor, eliminarea duplicatelor și setări reproductibile.
- Extindeți planificatorul de cub local în unități de lucru de sinteză distribuite în fazele ulterioare.

### Faza 1: fundație locală versionată

- Definiți formatele obiect, operațiune, contribuție, ramură și manifest.
- Adăugați spații de lucru multi-STL cu vizibilitate, transformări, metadate și proveniență per sursă.
- Adăugați valori privind calitatea înregistrării și clasificarea prin suprapunere spațială.
- Sintetizați suprafețe care concordă statistic în timp ce eliminați geometria duplicată și închisă.
- Adăugați o recenzie vizuală pentru conflicte, lacune, încredere și geometrie unică pentru o singură sursă.
- Persistați istoricul local pe parcursul sesiunilor de aplicație.
- Adăugați ochiuri vizuale și comparații de regiuni.
- Faceți operațiunile deterministe și reproductibile independent.

### Faza 2: noduri locale coordonate

- Rulați noduri de lucru pe o stație de lucru.
- Adăugați la coadă, raportarea capacităților, atribuirea de muncă și anularea.
- Afișați starea nodului și a unității de lucru în interfața de utilizare MeshMill.
- Validați partiționarea și rezultatul asamblarii la nivel local.

### Faza 3: sinteza multi-stație de lucru

- Adăugați descoperirea și înregistrarea LAN autentificate.
- Transferați intrările și rezultatele de lucru adresate conținutului cu suport pentru CV.
- Coordonați munca concomitentă pe mai multe stații de lucru.
- Recuperați atribuirile după defecțiunea nodului sau a rețelei.

### Faza 4: versiunea colaborativă

- Adăugați colaboratori, ramuri, stări de revizuire și permisiuni.
- Îmbinați contribuțiile care nu se suprapun.
- Detectați și rezolvați conflictele de suprapunere sau de dependență.
- Sintetizați contribuțiile selectate într-o versiune de obiect reproductibilă.

### Faza 5: întărirea producției

- Adăugați teste de compatibilitate cu protocolul și gestionarea versiunilor mixte.
- Adăugați teste de audit, integritate, corupție, întrerupere și recuperare.
- Evaluați performanța de planificare, partiționare, transfer, îmbinare și sinteză.
- Implementarea documentelor, backup, migrare și recuperarea incidentelor.
