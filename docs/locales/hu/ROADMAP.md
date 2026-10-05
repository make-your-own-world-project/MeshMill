# MeshMill ütemterv

## Platform támogatás

A Windows a kezdeti csomagolt platform. Az alkalmazás architektúrája és a mesh formátumok
többplatformos, és a jövőbeli kiadásoknak natív Linux és macOS csomagokat kell hozzáadniuk. Platformos munka
magában foglalja a csomagolást, az alkalmazások integrációját, a hardver mérőszámait, a fájlrendszer viselkedését és az automatizált
kiadásteszt, miközben megőrzi ugyanazt a projektet és a STL munkafolyamatokat minden támogatott rendszeren.

- Érvényesítse a Linux x86-64 előnézeti csomagot disztribúciók, asztali környezetek és megjelenítések között
  szervereket és GPU-illesztőprogramokat, mielőtt stabillá tenné elő.
- Érvényesítse a macOS Apple Silicon és az x86-64 előnézeti csomagokat valódi hardveren, majd adja hozzá a Fejlesztőt
  Személyi igazolvány aláírása és közjegyzői igazolása az istállóba lépés előtt.
- Adjon hozzá platform-natív CPU, memória és GPU metrikaszolgáltatókat egy megosztott felület mögé.
- A mentett beállítások, a billentyűzetkiosztás, a parancssori viselkedés és a projektadatok hordozhatóak legyenek.

Ez az ütemterv a tervezett munkát rögzíti. Nem írja le a jelenlegi kiadás jellemzőit.

## Hatály

A MeshMill kezeli a geometriát, a hálósűrűséget, a pontsűrűséget, az optimalizálást, a tisztítást, az érvényesítést és a STL-t
felcserélni, így a nagy vagy nehéz mesh fájlok hasznosak maradnak a későbbi szerkesztési munkafolyamatokban.

Általános célú modellezés, szobrászat, festés, animáció, renderelés, jelenetkompozíció, anyagok,
kötélzet és más tartalom-létrehozó rendszerek kívül esnek ezen az ütemterven. Az elosztott szintézis érvényes
a MeshMill mesh-kezelési műveleteihez, és nem bővíti ki a terméket általános szerkesztővé.

## Referencia geometria

A kötegelt kompozit háló a jelenlegi algoritmusok és ütemterv általános fejlesztési eszköze
munka. Szándékosan redundáns rétegei és egyenetlen sűrűsége megismételhető összehasonlításokat tesz lehetővé
redukciós minőség, sűrűségelemzés, átfedéskezelés, regionális műveletek, magon kívüli feldolgozás,
és a jövőbeni szintézis. Az ütemterv implementációinak jelentést kell adniuk az eredményekről ehhez a rendszerhez képest
célirányosan felépített regressziós hálók, ahelyett, hogy egyetlen modell viselkedését optimalizálnák.

## Multi-STL munkaterületek és statisztikai szintézis

Egy munkaterületnek több STL bemenetet kell fogadnia különálló, egymástól függetlenül látható forrásobjektumként.
A MeshMill-nek össze kell hangolnia ezeket a forrásokat, meg kell mérnie geometriai egyezésüket, és szintetizálnia kell egy használhatót
háló a duplikált belső felületek vagy az ismétlődő átfedési geometria megtartása nélkül.

Tervezett viselkedés:

- több STL forrás hozzáadása, eltávolítása, elrejtése, elkülönítése, átrendezése és ellenőrzése egy munkaterületen;
- megőrzi a forrás azonosságát, egységeit, átalakításait, határait, felbontását és működési előzményeit;
- automatikus regisztrációt biztosítanak kézi igazítási vezérlőkkel és mérhető illeszkedési minőséggel;
- a forrásokat az összehasonlítás előtt térbeli régiókra osztja fel, így a nagy bemenetek korlátozottak maradnak;
- elemezze a foglaltságot, a legközelebbi felszín távolságát, a normál egyezést, a helyi sűrűséget, a szórást és
  megfigyelések száma az átfedő régiókban;
- osztályozhatja az egyező felületeket, az ütköző felületeket, a szkennelési zajt, a hézagokat és az egyedi geometriát;
- statisztikailag egyező felületek konszolidálása egy reprezentatív felületté rögzítéssel
  magabiztosság az ismétlődő háromszögek egymásra halmozása helyett;
- távolítsa el a zárt, egybeeső és megosztott geometriát, amely nem járul hozzá a külső formarészletekhez;
- megőrizni a nem átfedő forrásgeometriát, és a kétértelmű területeket vizuális áttekintésre kitenni;
- forrásonkénti és régiónkénti súlyozás engedélyezése, ha egy szkennelés tisztább vagy részletesebb;
- a szintézis után a vízzáróság, a határok, a normálok, a méretek és a topológia érvényesítése;
- rögzíti a forrás eredetét és a szintézis paramétereit, hogy a kombinált háló reprodukálható legyen;
- megtekintheti a várható háromszögszámot, a határokat, az átfedés eltávolítását és a megbízhatósági eloszlást
  a szintetizált eredmény végrehajtása.

Ennek a munkafolyamatnak ugyanazt a magon kívüli térbeli indexet és munkaegység-modellt kell használnia, amelyet nagyra terveztek
hálók. A statisztikai összehasonlításnak és az átfedési konszolidációnak is eloszthatónak kell lennie a helyi szinten
vagy távoli MeshMill csomópontok.

## Elosztott szintézis

A MeshMill fürtnek több, párhuzamosan működő csomópontot kell koordinálnia
munkaállomások. Egy csomópont megvizsgálhat, kiválaszthat, csökkenthet, érvényesíthet, javíthat vagy kombinálhat egy hozzárendelt régiót vagy
munkaegység. A hozzájárulások független verziójúak maradnak, amíg felül nem vizsgálják és be nem építik őket
megosztott objektumverzióba.

A rendszernek támogatnia kell:

- több operátor és automatizált csomópontok egyidejű hozzájárulása;
- determinisztikus munkaegység-bemenetek, paraméterek, függőségek és kimenetek;
- képesség-tudatos ütemezés a CPU, GPU, a memória, az algoritmusok és az aktuális terhelés alapján;
- hálók, régiók, érvényesítési lépések és szintézis szakaszok függőség-tudatos particionálása;
- tartós várólisták szüneteltetéssel, folytatással, törléssel, újrapróbálkozással, átcsoportosítással és hibajavítással;
- tartalom-címzett műtermékek és csomópontok közötti integritás-ellenőrzések;
- reprodukálható szintézis az elfogadott hozzájárulási változatok rögzített halmazából;
- offline vagy szakaszosan csatlakoztatott munkaállomások, amelyek később szinkronizálhatók;
- helyi-első művelet a résztvevő csomópontok és a megosztott projektadatok explicit vezérlésével.

## Verziózott együttműködés

Minden hozzájárulásnak rögzítenie kell a szülőobjektum verzióját, a kiválasztott régiót vagy munkaegységet, műveletet,
paraméterek, csomópont-azonosító, időbélyegek, függőségek, érvényesítési eredmények és kimeneti ellenőrző összeg.

Tervezett együttműködési viselkedés:

- a projektek objektumokat, ágakat, ellenőrzőpontokat, hozzájárulásokat és szintetizált verziókat tartalmaznak;
- a közreműködők ugyanabból a szülőverzióból dolgozhatnak anélkül, hogy felülírnák egymást;
- a nem átfedő hozzájárulások az érvényesítés után automatikusan egyesülhetnek;
- az átfedő geometria vagy az inkompatibilis függőségek kifejezett konfliktust okoznak;
- a konfliktusok vizuális összehasonlítást, régiószintű választást, újrabázist, újrafutást és kézi feloldást biztosítanak;
- a felülvizsgálati állapotok közé tartozik a függőben lévő, elfogadott, elutasított, felülírt, ütköző és beépített állapot;
- a végső szintézis manifesztum minden beépített hozzájárulást és függőséget azonosít.

## Koordinációs UI

Az asztali alkalmazásnak külön parancssor nélkül kell kezelnie az elosztott munkát
vagy szerver-adminisztrációs munkafolyamat. A tervezett nézetek a következők:

- **Projektek:** objektumok, ágak, verziók, közreműködők és szintézis állapota.
- **Cluster:** csatlakoztatott munkaállomások és csomópontok, képességek, állapot, terhelés és aktuális hozzárendelés.
- **Várólista:** függőben lévő, aktív, szüneteltetett, blokkolt, sikertelen és befejezett munkaegységek.
- **Hozzájárulások:** szerző, csomópont, szülőverzió, érintett régió, paraméterek, ellenőrzések és felülvizsgálati állapot.
- **Összehasonlítás:** szinkronizált 3D nézetek, geometriai különbségek, metrikák és határellenőrzés.
- **Ütközések:** átfedő régiók, függőségi konfliktusok, megoldási lehetőségek és ellenőrzési eredmények.
- **Szintézis:** függőségi grafikon, összesített előrehaladás, kiválasztott hozzájárulási verziók és végső kimenet.
- **Előzmények:** elágazási grafikonok, ellenőrzőpontok, egyesítések, szintetizált verziók és reprodukálhatósági jegyzékek.

A nézetben meg kell jeleníteni a tulajdonjogot, a hozzárendelt régiókat, a befejezett munkát, a függőben lévő változtatásokat, az ütközéseket,
és verzióbeli különbségek a mögöttes háló megváltoztatása nélkül.

## Koordináció és szállítás

Az első tervezési fázisban meg kell határozni a protokoll határait az átvitel kiválasztása előtt. A protokoll
el kell különítenie a koordinációs metaadatokat a nagy hálós műtermékektől, támogatnia kell a folytatható átvitelt, és
használható marad a helyi hálózaton külső fiók vagy hosztolt szolgáltatás nélkül.

Szükséges koordinációs koncepciók:

- koordinátorválasztás vagy kifejezetten kiválasztott koordinátor;
- csomópont-felderítés és kézi csomópont-regisztráció;
- hitelesített munkamenetek és projekt-hatókörű engedélyezés;
- bérleti szerződések és szívverések a munka tulajdonjogáért;
- idempotens munkabeadás és eredmény elfogadás;
- verzió egyeztetés a különböző MeshMill kiadások között;
- strukturált események az előrehaladás, naplók, érvényesítés, hibák és újrapróbálkozás érdekében;
- helyreállítás koordinátor, munkaállomás, hálózat vagy csomópont megszakítása után.

## Szállítási fázisok

### Phase 0: out-of-core large-mesh processing

Az index, az adatfolyam, a gyorsítótár, a munkaegység és a biztonsági szerződés dokumentálva van
[`docs/OUT_OF_CORE.md`](docs/OUT_OF_CORE.md).

- A teljes háló kiosztása előtt becsülje meg a háromszögek számát és a munkamemóriát.
- Nyissa meg a túlméretezett bináris STL fájlokat korlátos, egyenletes mintavételű navigációs áttekintésként.
- A teljes felbontású geometria felosztása determinisztikus átfedési határokkal rendelkező térkockákra.
- Független kockák egyidejű olvasása, elemzése és optimalizálása a CPU és a memória határain belül.
- Benchmark GPU-számítási megvalósítások csökkentési szakaszokhoz, például hibaértékeléshez, jelölt
  pontozás, térbeli lekérdezések és független munkaegység-feldolgozás. Csak akkor töltsön le egy színpadot
  mérhető végponttól végpontig terjedő sebesség- vagy memóriaelőnyt biztosít a determinizmus, a háló csökkentése nélkül
  minőség, topológia garanciák vagy kompatibilitás a megfelelő GPU-t nem tartalmazó rendszerekkel.
- A durva-finom nézetablak szintek streamelése ahelyett, hogy a teljes hálót megkövetelné a memóriában.
- Rajzolja meg a kocka állapotát közvetlenül a nézetablakban: sorban állás, olvasás, feldolgozás, befejezett és sikertelen.
- Mutasson kockánkénti haladást az egyes kockák kitöltésével, és őrizze meg a magas szintű teljes objektum nézetet.
- Állítsa össze a feldolgozott kockákat határellenőrzéssel, ismétlődések eltávolításával és reprodukálható beállításokkal.
- Bővítse ki a helyi kockaütemezőt elosztott szintézis munkaegységekre a későbbi fázisokban.

### Phase 1: versioned local foundation

- Határozza meg az objektum-, művelet-, hozzájárulás-, ág- és jegyzékformátumokat.
- Adjon hozzá több STL munkaterületet forrásonkénti láthatósággal, átalakításokkal, metaadatokkal és származással.
- Adjon hozzá regisztrációs minőségi mutatókat és térbeli átfedések osztályozását.
- Szintetizáljon statisztikailag egyező felületeket, miközben eltávolítja az ismétlődő és zárt geometriát.
- Vizuális áttekintést adhat az ütközésekről, hiányosságokról, magabiztosságról és az egyetlen forrás egyedi geometriájáról.
- Megőrzi a helyi előzményeket az alkalmazási munkameneteken keresztül.
- Vizuális háló és régió-összehasonlítás hozzáadása.
- Tegye a műveleteket determinisztikussá és függetlenül reprodukálhatóvá.

### Phase 2: coordinated local nodes

- Munkavégző csomópontok futtatása egy munkaállomáson.
- Adjon hozzá sorban állást, képességjelentéseket, munkafeladatokat és lemondást.
- Csomópont és munkaegység állapotának megjelenítése a MeshMill felhasználói felületen.
- Helyileg érvényesítse a particionálást és az eredmény-összeállítást.

### Phase 3: multi-workstation synthesis

- Hitelesített LAN-felderítés és regisztráció hozzáadása.
- Tartalomközpontú munkabemenetek és eredmények átvitele az önéletrajz támogatásával.
- Koordinálja az egyidejű munkát több munkaállomáson.
- Hozzárendelések helyreállítása csomópont vagy hálózati hiba után.

### Phase 4: collaborative versioning

- Közreműködők, fiókok, áttekintési állapotok és engedélyek hozzáadása.
- Egyesítse a nem átfedő hozzájárulásokat.
- Az átfedő vagy függőségi konfliktusok észlelése és megoldása.
- Szintetizálja a kiválasztott hozzájárulásokat reprodukálható objektumverzióvá.

### Phase 5: production hardening

- Protokollkompatibilitási tesztek és vegyes verziókezelés hozzáadása.
- Adjon hozzá audit-, integritás-, korrupció-, megszakítási és helyreállítási teszteket.
- Ütemezési, particionálási, átviteli, egyesítési és szintézisteljesítmény összehasonlítása.
- Dokumentumtelepítés, biztonsági mentés, áttelepítés és incidensek helyreállítása.
