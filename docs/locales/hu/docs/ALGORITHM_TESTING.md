# Algoritmus tesztelés és hozzájárulás

A MeshMill algoritmusoknak kezelhetővé kell tenniük a bonyolult geometriát, miközben láthatóvá teszik hatásukat,
mérhető és visszafordítható az eredmény alkalmazása előtt.

## Referencia lámpatestek

Használja az összetett minta geometriájának mindkét kötegelt változatát:

- A `samples/sample-scan.stl` a kisebb normál Git készülék a rutinfejlesztéshez, automatizált
  ellenőrzéseket és a vezérlőelemek megtanulását.
- A `samples/original-scan.stl` a teljes Git LFS lámpatest nagy fájlok viselkedéséhez, redundáns rétegekhez,
  egyenetlen sűrűség, átfedés és teljesítménymunka.

A redundáns és sűrű régiók szándékos tesztjellemzők. Egy teszt célba veheti őket, de
nem szabad azt feltételezni, hogy minden átfedő felület eldobható. Adjon hozzá kompakt szintetikus hálókat, ha a
a változtatáshoz ismert határ, görbület, topológia, sűrűség vagy átfedési invariáns szükséges.

## Összehasonlító ellenőrző lista

Algoritmus- vagy paramétermódosításhoz rögzítse:

- MeshMill verzió vagy véglegesítés;
- bemeneti rögzítés és ellenőrző összeg;
- algoritmus, előre beállított minőség, cél és speciális beállítások;
- eredeti és eredő háromszög- és csúcsszámok;
- csökkentési százalék, méretek és méreteltolódás;
- az eltelt idő és a csúcsmemória, amikor a teljesítmény releváns;
- képernyőképek ugyanazokból a mentett nézetekből és megjelenítési módokból;
- látható határ, lyuk, önmetszés, átfedés vagy torzítás változásai;
- hogy az eredmény teljes hálós vagy csak kiválasztási műveletből származott.

Hasonlítsa össze az aktuális viselkedéssel ugyanazon a célon, ne csak egy másik előre beállított értékkel a
eltérő kimeneti szám. Vizsgálja meg az árnyékolt, sűrűségű, drótvázas és csúcsos kijelzőket, ahol lehetséges.

## Elfogadási útmutató

Az optimalizálási változtatásnak el kell kerülnie a váratlan méretváltozásokat, a nyilvánvaló felületi inverziót,
repedések a feldolgozott régiók között, értelmes határok elvesztése és nagy minőségi regressziók a
hasonló kimeneti szám. A sűrűség-orientált változásoknak azt kell mutatniuk, hogy az eltávolított koncentráció igen
nem hordoznak hasznos görbületet vagy topológiát.

A teljesítményeredményeknek azonosítaniuk kell a processzort, a memóriakapacitást, a grafikus hardvert és a működést
rendszer, a bemeneti méret, és hogy az adatok már gyorsítótárban vannak-e. Strukturális ellenőrzés és képernyőképek
támogatja az áttekintést, de nem helyettesíti a forrásgeometriát ismerő közreműködők által végzett ellenőrzést.

## Regression tests

Részesítse előnyben az explicit tűrésekkel rendelkező determinisztikus teszteket. Legyen elég kicsi az új szerelvények a normál Githez,
dokumentálja eredetüket és licencüket, és szintetikus geometriát használjon, ha a valódi forrásadatokra nincs szükség.
A teszteknek ki kell terjedniük a törlésre és az állapot-visszaállításra, ha egy művelet módosíthatja a geometriát.
