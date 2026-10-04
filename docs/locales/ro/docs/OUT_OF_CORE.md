# Arhitectură de plasă în afara nucleului

Protecția actuală a fișierelor mari a MeshMill estimează memoria de lucru înainte de a aloca un
plasă. Fișierele care depășesc bugetul configurat se pot deschide ca prezentări de navigare limitate. An
Prezentare generală este o geometrie eșantionată, este vizibil identificată ca atare și nu poate fi editată sau exportată ca
deși era sursa completă.

Detaliile adevărate dependente de zoom necesită un index spațial persistent. Designul de mai jos definește asta
următoarea etapă de implementare.

## Format index

Fiecare rețea sursă primește un director `.meshmill-index` versionat care conține:

- `manifest.json`, cu dimensiunea sursei, timpul de modificare, hash-uri de conținut eșantionat, limite,
  numărarea triunghiurilor, versiunea indexului, precizia coordonatelor și descrierile nivelurilor;
- dale spațiale adresate prin nivel octree și cod Morton;
- o plasă de afișare grosieră pentru fiecare placă părinte ocupată;
- înregistrări triunghiulare cu rezoluție completă în plăci de frunze; şi
- Proprietatea limitelor și metadatele de suprapunere utilizate în timpul operațiunilor și asamblarii regionale.

Crearea indexului citește sursa secvenţial în blocuri mărginite. Scrie piese temporare și
publică atomic manifestul după ce fiecare fișier necesar trece validarea. Un întrerupt sau
indexul învechit este detectat din manifestul său și poate fi reluat sau reconstruit fără a deschide complet
plasă în memorie.

## Vizualizare în flux

Vizualizarea selectează piese folosind trunchiul camerei și eroarea de spațiu pe ecran. Plăcile părinte grosiere sunt
arătat mai întâi. Placile pentru copii vizibile le înlocuiesc pe măsură ce camera se apropie, în afara ecranului și
plăcile cu impact redus rămân grosiere. RAM și VRAM au bugete independente și sunt utilizate cel mai puțin recent
cache-urile. Eliberarea detaliilor nu eliberează niciodată reprezentarea grosieră a întregului obiect.

Programatorul înregistrează aceste stări: în coadă, citire, procesare, încărcare, rezident, eșuat,
si anulat. Fereastra poate colora cuburi după stare și umple fiecare cub proporțional cu el
progres. Anularea elimină rezultatele parțiale și lasă activă ultima reprezentare completă.

## Prelucrare și capacitate

O unitate locală de lucru este o țiglă plus suprapunerea deterministă cerută de funcționarea sa. Concurență
este limitat de RAM disponibil în prezent, procentul de memorie configurat, numărul de procesoare logice și
dimensiunea măsurată a unității de lucru. Încărcarea și afișarea GPU au un buget separat VRAM. Raportat paralel
capacitatea este o estimare până când plăcile reprezentative au fost măsurate.

Operațiunile păstrează un proprietar pentru fiecare element de limită. Asamblarea validează granițele comune,
elimină duplicatele, verifică numărătoarea și limitele și înregistrează exact parametrii utilizați. Aceeași lucrare
formatul de unitate și rezultat pot fi programate ulterior în nodurile de sinteză distribuite.

## Reguli de siguranță

- Un eșantion global este etichetat ca o vedere de ansamblu, nu ca un detaliu de vizualizare cu rezoluție completă.
- O prezentare generală nu poate suprascrie sau exporta ca rețea sursă completă.
- Solicitările complete care depășesc bugetul actual necesită o alegere explicită.
- Generarea indexului, procesarea plăcilor și asamblarea rămân anulabile și păstrează cele anterioare
  stare completă.
- Valorile capacității sunt estimări și identifică dacă descriu motorul actual sau planificat
  executie paralela de tigla.
