# Contribuind

Contribuțiile sunt binevenite prin probleme și solicitări de tragere.

## Domeniul proiectului

MeshMill face ca fișierele mesh supradimensionate, dense sau dificile să fie gestionate pentru editare în aval și
fluxurile de lucru de producție. Contribuțiile ar trebui să îmbunătățească inspecția geometriei, densitatea ochiurilor și a punctelor
management, optimizare, selecție, decupare, curățare, validare, schimb STL, performanță,
sau coordonarea acelor operațiuni.

Proiectul nu include modelare de uz general, sculptură, pictură, animație, randare,
compoziția scenei, materialele, manipularea sau alte sisteme de creare a conținutului. Propuneri care introduc
aceste caracteristici sunt în afara domeniului de aplicare al proiectului.

Noile funcții ar trebui să mențină aplicația concentrată, să păstreze fluxurile de lucru directe care transformă sursa
geometria în rețele ușor de gestionat și evitați să transformați controalele de sprijin într-o editare generală
mediu.

## Localizare

Textul sursă al interfeței de utilizare în limba engleză este stocat în `locales/en-US.json`. Metadatele locale sunt stocate în
`locales/manifest.json`. Cataloagele de UI traduse folosesc aceleași chei stabile și numele fișierului
`<locale>.json`. Documentația tradusă folosește numele de fișier rădăcină potrivit sub
`docs/locales/<locale>/`.

Traducerile sunt inițial produse cu servicii externe de traducere automată și primesc
validare structurală automată. Acest proces nu poate garanta natural, precis din punct de vedere tehnic sau
limbaj corect din punct de vedere contextual. Vorbitorii nativi sunt încurajați să revizuiască și să corecteze interfața de utilizare tradusă
text și documentație. Corecțiile de traducere ar trebui să păstreze cheile de catalog, substituenții,
comenzi, linkuri, măsurători, nume de produse și structură Markdown.

După ce schimbați etichetele, sfaturile cu instrumente, casetele de dialog sau alt text vizibil de utilizator, rulați:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
```

Examinați împreună modificările sursei și cheile regenerate.

## Modificări de geometrie și algoritm

Utilizați geometria eșantionului grupat atunci când modificați optimizarea, analiza densității, selecția, decuparea,
manipularea fișierelor mari sau comportamentul de comparare a ferestrelor de vizualizare. Conține în mod intenționat straturi redundante
și densitate neuniformă, astfel încât un rezultat util ar trebui să îmbunătățească manevrarea fără a ascunde distorsiunea,
eliminarea granițelor semnificative sau eliminarea în tăcere a geometriei pe care o păstrează un alt algoritm.

Înregistrați intrarea, algoritmul, setările, numărul triunghiurilor, dimensiunile, deriva dimensiunii, timpul scurs,
și capturi de ecran relevante pentru comparații. Testați atât dispozitivul mai mic normal-Git, cât și, când
schimbarea se referă la geometria mare sau stratificată, dispozitivul original Git LFS. Nu reglați un algoritm
numai la acest dispozitiv. Adăugați mici cazuri sintetice pentru invariantul sau regresia specifică
testat.

Consultați [Testarea algoritmului și contribuția](docs/ALGORITHM_TESTING.md) pentru lista de verificare a comparației.

## Configurare de dezvoltare

1. Instalați Python 3.12 pe 64 de biți pe Windows.
2. Creați și activați un mediu virtual.
3. Instalați `requirements-dev.txt`.
4. Rulați `python meshmill.py` pentru GUI sau `python meshmill.py --help` pentru utilizarea CLI.
5. Rulați `python -m py_compile meshmill.py` înainte de a trimite o modificare.

Păstrați rețele private, executabile generate, capturi de ecran care conțin informații private și locale
construiți directoare din comiteri. Geometria de testare redistribuibilă aparține sub `samples/` cu ea
sursa, licența, dimensiunile și metoda de generare documentate. Noile fișiere sursă ar trebui să utilizeze
Identificator SPDX `GPL-3.0-or-later`.

Decupați fiecare captură de ecran a documentației în conținutul aplicației MeshMill. Nu includeți
bară de activități, fereastră Chrome fără legătură, notificări, detalii contului, căi private sau fundal
conținut desktop.
