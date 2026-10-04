# Testarea algoritmului și contribuția

Algoritmii MeshMill ar trebui să facă geometria dificilă gestionabilă, păstrând efectele vizibile,
măsurabil și reversibil înainte de aplicarea unui rezultat.

## Corpuri de referință

Utilizați ambele versiuni grupate ale geometriei probei compozite:

- `samples/sample-scan.stl` este dispozitivul Git normal mai mic pentru dezvoltarea de rutină, automatizat
  verificări și învățarea controalelor.
- `samples/original-scan.stl` este dispozitivul complet Git LFS pentru comportamentul fișierelor mari, straturi redundante,
  densitate neuniformă, suprapunere și performanță.

Regiunile redundante și dense sunt caracteristici de testare intenționate. Un test îi poate viza, dar
nu trebuie să presupună că fiecare suprafață suprapusă este de unică folosință. Adăugați ochiuri sintetice compacte când a
schimbarea necesită o limită cunoscută, o curbură, o topologie, o densitate sau un invariant de suprapunere.

## Lista de verificare a comparației

Pentru o modificare a algoritmului sau a unui parametru, înregistrați:

- MeshMill versiune sau commit;
- dispozitiv de intrare și sumă de control;
- algoritm, setări prestabilite de calitate, țintă și setări avansate;
- numărul de triunghiuri și vârfuri inițiale și rezultate;
- procentul de reducere, dimensiunile și deriva de dimensiune;
- timpul scurs și memoria de vârf atunci când performanța este relevantă;
- capturi de ecran din aceleași vizualizări și moduri de afișare salvate;
- limită vizibilă, gaură, auto-intersecție, suprapunere sau modificări de distorsiune;
- indiferent dacă rezultatul a provenit dintr-o operație cu plasă întreagă sau numai de selecție.

Comparați cu comportamentul actual la aceeași țintă, nu numai cu o altă presetare cu a
număr diferit de ieșiri. Inspectați afișajele umbrite, de densitate, wireframe și vârfuri, acolo unde este cazul.

## Îndrumări de acceptare

O modificare de optimizare ar trebui să evite schimbările neașteptate de dimensiune, inversarea evidentă a suprafeței,
fisuri între regiunile procesate, pierderea granițelor semnificative și regresii mari de calitate la a
număr de ieșiri similar. Modificările orientate pe densitate ar trebui să demonstreze că concentrația îndepărtată a făcut-o
nu poartă curbură sau topologie utilă.

Rezultatele de performanță ar trebui să identifice procesorul, capacitatea de memorie, hardware-ul grafic, funcționarea
sistem, dimensiunea de intrare și dacă datele au fost deja stocate în cache. Validare structurală și capturi de ecran
susține revizuirea, dar nu înlocuiește inspecția de către colaboratori familiarizați cu geometria sursei.

## Teste de regresie

Preferați teste deterministe cu toleranțe explicite. Păstrați noile dispozitive suficient de mici pentru Git normal,
documentați originea și licența acestora și utilizați geometria sintetică atunci când datele sursă reale nu sunt necesare.
Testele ar trebui să acopere anularea și restabilirea stării atunci când o operațiune poate modifica geometria.
