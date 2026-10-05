<p align="center">
  <img src="assets/meshmill-logo.svg" width="620" alt="MeshMill: Dirty geometry? Clean it up!">
</p>

MeshMill este o aplicație desktop specializată pentru gestionarea geometriilor de tip mesh
de dimensiuni mari, cu densitate ridicată sau complexe. Oferă funcții de inspecție rapidă, analiză a densității, selecție pe regiuni, decupare, ștergere,
precum și reducere controlată a mesh-ului, fără a necesita crearea unui cont sau încărcarea geometriei.

Redarea OpenGL accelerată de GPU păstrează navigarea în fereastra de vizualizare, alegerea hardware-ului, vizualizarea densității,
și receptiv la inspecție interactivă. Reducerea rețelei se execută în prezent în lucrători nativi separati ai procesorului, (CPU)
ținând calculele lungi de geometrie departe de interfață.

MeshMill funcționează cu mesh-uri provenite de la scanere 3D, exporturi CAD și de modelare, fluxuri de lucru de reconstrucție,
geometrii generate și alte surse STL. Pregătește geometria pentru editoare ulterioare,
unelte de fabricație și alte fluxuri de lucru care implică mesh-uri. Modelarea generală, sculptarea, animația,
materialele și crearea de scene nu fac parte din domeniul său de aplicare.

## Descărcare

Descărcați unul dintre aceste fișiere din secțiunea [Lansări GitHub](../../releases):

- `MeshMill-<version>-windows-x64-setup.exe`: instalator per utilizator, cu integrare în meniul Start și opțiune
  pentru comenzi rapide pe desktop.
- `MeshMill-<version>-windows-x64-portable.zip`: aplicație portabilă. Extrageți întreaga arhivă,
  apoi rulați `MeshMill.exe`.

Ambele pachete includ mediul de rulare (runtime) al aplicației. Utilizatorii finali nu instalează dependențele Python, Node.js sau
dependențe. Versiunea stabilă acceptă Windows 10 și Windows 11 pe hardware x64.

Pachetele de previzualizare Linux x86-64 și macOS Intel/Apple silicon nesemnate pot apărea și în versiuni.
Acestea sunt construite pe rulare native găzduite de GitHub și trec teste de fum CLI și eșantion-mesh.
dar mai trebuie testat pe hardware real. Consultați [Testarea de previzualizare Linux și macOS](../../PLATFORM_TESTING.md)
înainte de instalare sau raportare rezultate.

Compilările comunității nesemnate pot afișa un avertisment Windows SmartScreen sau macOS Gatekeeper. Eliberare
sumele de verificare sunt listate lângă fiecare lansare.

## Pornire rapidă

1. Deschideți un STL.
2. Examinați-l în modul de afișare Shaded (Umbrit), Density (Densitate), Wireframe (Cadru de sârmă) sau Vertices (Vârfuri).
3. Alegeți un nivel de calitate, un algoritm și un număr țintă de triunghiuri.
4. Selectați **Optimize** (Optimizare) pentru a calcula un rezultat.
5. Comparați mesh-urile (rețelele poligonale) original și optimizat, apoi selectați **Apply** (Aplicare) pentru a confirma operațiunea.
6. Selectați **Save current state** (Salvare stare curentă) sau apăsați `Ctrl+S`.

MeshMill nu inițiază niciodată optimizarea doar pentru că s-a modificat un fișier sau o setare.

## Capabilități

- Intrare STL în format binar și ASCII, ieșire STL în format binar
- Reducere Fast QEM cu păstrarea densității, a formei și a topologiei
- Vizualizare OpenGL accelerată de GPU, alegere hardware și vizualizare a densității
- Lucrători nativi cu geometrie de fundal pentru reducerea ochiurilor
- Moduri de afișare: umbrit, densitate, cadru de sârmă (wireframe) și noduri (vertex)
- Ținte automate derivate din geometrie, nu dintr-o limită fixă ​​a numărului de triunghiuri
- Selectarea poligoanelor cu opțiune de selecție aditivă pe mai multe regiuni
- Decuparea, ștergerea sau optimizarea exclusivă a regiunii selectate
- Compararea în cache a rețelei (mesh) originale, anterioare și curente
- Funcții „Anulare” (Undo) și „Refacere” (Redo) pentru modificările geometrice aplicate
- Afișarea deviației dimensionale, a procentului de reducere și a dimensiunii estimate a fișierului de ieșire
- Unități de măsură: milimetri, centimetri, metri, inchi și picioare
- Indicatori pentru CPU, memorie, GPU și activitatea geometrică
- Încărcarea unei vederi de ansamblu limitate atunci când un fișier binar STL depășește bugetul de memorie configurat
- Aplicații cu interfață grafică (GUI) și linie de comandă
- Procesare locală, fără dependență de cont, telemetrie, încărcare de date sau cloud

## Inspectați geometria înainte de a o reduce

Ecranul Shaded oferă o vedere clară a suprafeței și a siluetei. Este util pentru comparare
conservarea formei înainte de aplicarea unei treceri de optimizare.

![Port de vizualizare umbrit MeshMill care arată rețeaua de probă grupată](../../images/meshmill-shaded.png)

Ecranul Vertices expune distribuția reală a punctelor. Regiuni dense de scanare, zone rare și
modificările bruște ale eșantionării sunt vizibile fără modificarea geometriei. Panoul de valori extins
urmărește CPU, memorie, GPU și activitatea de procesare a geometriei în timp ce lucrezi cu rețeaua.

![Afișează MeshMill Vertices cu valori de performanță extinse](../../images/meshmill-vertices.png)

Afișajul Wireframe arată direct structura triunghiului. Ajută la identificarea densității inutile,
triangulație neregulată și regiuni în care simplificarea poate elimina geometrie substanțială.

![Afișajul MeshMill Wireframe care arată variația densității triunghiului](../../images/meshmill-wireframe.png)

## Analizați densitatea ochiurilor

Afișarea Density hărți densitatea locală relativă pe întreg modelul. Regiunile rare rămân reci în timp ce
regiunile din ce în ce mai dense se deplasează prin culori mai strălucitoare, făcând eșantionarea neuniformă vizibilă dintr-o privire.

![Afișarea densității MeshMill care arată densitatea relativă a ochiurilor](../../images/meshmill-density.png)

Densitatea rămâne disponibilă în timp ce se evaluează o optimizare provizorie. Cutia de instrumente raportează
algoritm, țintă, triunghiul rezultat și numărul de vârfuri, procentul de reducere, dimensiunile și
dimensiunea estimată a ieșirii înainte de aplicarea trecerii.

![Afișajul MeshMill Density care arată o optimizare provizorie](../../images/meshmill-density-overview.png)

Țineți apăsat butonul din dreapta al mouse-ului pentru a inspecta o regiune prin lupa circulară. Vederea mărită
rămâne centrat pe indicator și dezvăluie densitatea locală fără a schimba poziția principală a camerei.

![Afișarea densității MeshMill cu lupa de vizualizare](../../images/meshmill-density-zoom.png)

## Comenzi pentru vizualizare

| Intrare | Acțiune |
| --- | --- |
| Tragere cu butonul din mijloc | Orbitare |
| Shift + tragere cu butonul din mijloc | Deplasare (panoramare) |
| Rotița mouse-ului | Zoom spre cursor |
| Ctrl + rotița mouse-ului | Rotire în sens orar sau antiorar |
| Tastele săgeată | Orbitare în jurul centrului vizualizării |
| Ctrl + tastele săgeată | Deplasare (panoramare) |
| Ctrl + Shift + Sus/Jos | Zoom |
| Ctrl + Shift + Stânga/Dreapta | Roll |
| `F1` / `F2` / `F3` / `F4` | Umbrit / Densitate / Wireframe / Vertices |
| Țineți apăsat mouse-ul dreapta | Lupa |
| Shift + clic stânga | Adăugați sau eliminați puncte de riglă |
| Ctrl + trage la stânga | Desenați un poligon de selecție |
| `Ctrl+C` | Adăugați poligonul la selecția salvată |
| `Ctrl+X` | Decupați la selecție |
| `Ctrl+Space` | Optimizați selecția |
| `Delete` | Ștergeți selecția |
| `Escape` | Ștergeți selecția activă sau rigla |
| `Ctrl+Z` / `Ctrl+Y` | Anulați/refaceți |
| `Ctrl+S` | Salvați starea actuală a rețelei |

Tastele de vizualizare standard urmează blocul de navigare cu șase taste:

| Cheie | Vizualizare | Ctrl + tasta |
| --- | --- | --- |
| `Insert` | Stânga | Setați orientarea curentă ca Stânga |
| `Home` | Față | Setați orientarea curentă ca Front |
| `Page Up` | Corect | Setați orientarea curentă ca Dreapta |
| `Delete` | Top când nu există selecție | Setați orientarea curentă ca Top |
| `End` | Înapoi | Setați orientarea curentă ca Înapoi |
| `Page Down` | De jos | Setați orientarea curentă ca Inferioară |

Salvarea unei vizualizări actualizează și vizualizarea opusă a acesteia. Stânga și dreapta, față și spate și sus și jos
rămâne pereche. În dialogul de confirmare, **Salvare** este acțiunea implicită, așa că Enter salvează
orientare. Fața apare în partea de sus a vizualizărilor de sus și de jos.

Comenzile rapide pot fi modificate sau resetate în Setări.

## Flux de lucru de selecție

Țineți apăsat Ctrl și trageți stânga pentru a desena un poligon. Trageți colțurile pentru a o remodela, faceți clic stânga pe o margine pentru a adăuga o
punct sau faceți clic dreapta pe o margine pentru a elimina una. Adăugați mai multe regiuni cu `Ctrl+C`. Mutarea camerei se ascunde
poligonul ecran-spațiu păstrând în același timp geometria selectată.

Optimizarea cu o selecție activă afectează numai selecția respectivă. Rezultatul rămâne provizoriu
până când este selectat **Aplicare**. **Anulare** renunță la rezultatul provizoriu și reține selecția
se poate incerca o alta configuratie. Operațiunile de decupare și ștergere devin editări normale de rețea care nu pot fi anulate.

Panoul de selecție raportează vârfurile, triunghiurile, cota de plasă, estimate cumulate selectate
dimensiune și dimensiuni. Acțiunile sale decupează, adaugă, optimizează, șterg, dau înapoi sau șterg cele reținute
selecție fără a ascunde geometria înconjurătoare.

![MeshMill afișând o selecție regională păstrată și statisticile de geometrie ale acesteia](../../images/meshmill-crop-selection.png)

## Ochiuri mari

Înainte de a aloca un STL binar, MeshMill compară memoria de lucru estimată cu memoria configurată
buget de memorie. Un fișier deasupra bugetului se deschide ca o prezentare generală limitată, numai pentru citire. Prezentare generală raportează
numărul complet de triunghi sursă, dar dezactivează editarea și exportul deoarece este un eșantion, nu complet
obiect. Procesarea out-of-core indexată, dependentă de zoom este planificată în
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md).

## Linia de comandă

`MeshMillCLI.exe` este inclus în ambele pachete de lansare:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

Rulați `.\MeshMillCLI.exe --help` pentru toate opțiunile. MeshMill refuză să-și suprascrie fișierul de intrare.

## Geometria eșantionului

Sunt disponibile două versiuni ale eșantionului de dezvoltare. Proba este o plasă compozită cu
straturi intentionate de geometrie redundanta si densitate variata. Oferă oamenilor fără scaner a
dispozitiv realist pentru compararea algoritmilor, inspectarea densității, exercitarea operațiunilor regionale,
și dezvoltarea de caracteristici ale foii de parcurs. MeshMill nu necesită intrare scanată.

| Fișier | Triunghiuri | Dimensiune | Livrare | Cel mai bun pentru |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249.999 | 11,9 MiB | Git normal | Evaluare rapidă, CI și învățarea controalelor |
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4.126.315 | 196,8 MiB | Git LFS | Testarea geometriei sursei dense și a performanței cu ochiuri mari |

Eșantionul mai mic este descărcat cu fiecare clonă normală. Originalul neatins este opțional și
gestionat prin Git LFS, astfel încât să nu umfle istoricul obișnuit al depozitului. GitHub Desktop include
Git LFS. Utilizatorii de linie de comandă pot instala Git LFS și pot rula:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

Lansările etichetate publică și STL original ca descărcare directă pentru persoanele care nu folosesc Git.
Consultați [`samples/README.md`](../../../samples/README.md) pentru proveniență, dimensiuni și sume de control.

Colaboratorii algoritmului ar trebui să citească și
[Ghid de testare a algoritmului](docs/ALGORITHM_TESTING.md) înainte de a compara sau de a modifica reducerea
comportament.

## Unități STL

STL nu codifică o unitate. Schimbarea unităților de model modifică etichetele și măsurătorile fără scalare
coordonatele salvate. Selectați unitatea care descrie geometria sursei.

## Confidențialitate

MeshMill citește și scrie fișiere locale. Nu conține cont, telemetrie, încărcare, publicitate sau
caracteristică de procesare în cloud. Actuala implementare a valorilor GPU utilizează performanța locală Windows
contoare. Pentru Linux și macOS sunt planificați furnizori de valori native echivalente.

Pentru depanarea de diagnosticare, dezvoltatorii pot porni GUI cu
`--diagnostic-log <local-file.jsonl>`. Jurnalul înregistrează ruta de intrare și starea camerei la nivel local și este
dezactivat în timpul utilizării normale.

## Dezvoltare și lansare

Textul și documentația UI localizate sunt inițial produse cu traducere automată externă
servicii și verificate automat pentru daune structurale. Traducerea automată poate fi încă
nenaturale sau incorecte. Vorbitorii nativi sunt încurajați să revizuiască și să corecteze traducerile
procesul de contribuție.

- [Contribuie](CONTRIBUTING.md)
- [Proces de lansare](RELEASING.md)
- [Foaie de parcurs](ROADMAP.md)
- [Depanare](docs/TROUBLESHOOTING.md)
- [Notificări de la terți](THIRD_PARTY_NOTICES.md)

## Suport MeshMill

MeshMill este dezvoltat și întreținut independent. Citiți
[de ce contează sprijinirea acestei lucrări](SUPPORT.md) sau sprijiniți dezvoltarea continuă prin
[Cumpără-mi o cafea](https://buymeacoffee.com/tednv).

MeshMill este licențiat sub licența publică generală GNU, versiunea 3 sau o versiune ulterioară. Vezi
[`LICENSE`](../../../LICENSE).
