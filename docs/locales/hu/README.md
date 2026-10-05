<p align="center">
  <img src="assets/meshmill-logo.svg" width="620" alt="MeshMill: Dirty geometry? Clean it up!">
</p>

A MeshMill egy célzott asztali alkalmazás, amely lehetővé teszi a túlméretezett, nagy sűrűségű vagy összetett hálógeometriák
kezelését. Gyors ellenőrzést, sűrűségelemzést, régiókijelölést, vágást, törlést,
valamint szabályozott hálóegyszerűsítést kínál anélkül, hogy fiókra vagy a geometria feltöltésére lenne szükség.

A GPU-gyorsítású OpenGL-megjelenítés lehetővé teszi a nézetablak navigációját, a hardveres kijelölést, a sűrűség megjelenítését,
és interaktív ellenőrzésre reagáló. A hálócsökkentés jelenleg különálló natív CPU-munkásokon fut,
távol tartva a hosszú geometriai számításokat az interfésztől.

A MeshMill együttműködik a 3D szkennerekből, CAD- és modellezőszoftverek exportjaiból, rekonstrukciós folyamatokból,
generált geometriákból és egyéb STL-forrásokból származó hálókkal. Előkészíti a geometriát további szerkesztőprogramok,
gyártási eszközök és egyéb hálóalapú munkafolyamatok számára. Az általános célú modellezés, szobrászat, animáció,
anyagbeállítás és jelenetkészítés nem tartozik a funkciói közé.

## Letöltés

Töltse le az alábbi fájlok egyikét a [GitHub kiadások](../../releases) közül:

- `MeshMill-<version>-windows-x64-setup.exe`: felhasználóspecifikus telepítő Start menüvel és opcionális
  asztali parancsikonokkal.
- `MeshMill-<version>-windows-x64-portable.zip`: hordozható (portable) alkalmazás. Csomagolja ki a teljes archívumot,
  majd futtassa a `MeshMill.exe`-t.

Mindkét csomag tartalmazza az alkalmazás futtatásához szükséges összetevőket. A végfelhasználók nem telepítik a Python, Node.js vagy
függőségek. A stabil kiadás támogatja a Windows 10 és Windows 11 operációs rendszert x64-es hardveren.

Aláíratlan Linux x86-64 és macOS Intel/Apple Silicon előnézeti csomagok is megjelenhetnek a kiadásokban.
Natív GitHub által hosztolt futókra épülnek, és megfelelnek a csomagolt CLI és mintaháló füstteszteken,
de még mindig tesztelni kell valódi hardveren. Lásd: [Linux és macOS előzetes tesztelése] (docs/PLATFORM_TESTING.md)
a telepítés vagy az eredmények jelentése előtt.

Az aláíratlan közösségi buildek Windows SmartScreen vagy macOS Gatekeeper figyelmeztetést jeleníthetnek meg. Kiadás
Az ellenőrző összegek az egyes kiadások mellett szerepelnek.

## Gyors útmutató

1. Nyisson meg egy STL-t.
2. Vizsgálja meg Shaded (árnyékolt), Density (sűrűség), Wireframe (drótváz) vagy Vertices (csúcspontok) megjelenítési módban.
3. Válasszon minőségi szintet, algoritmust és cél háromszögszámot.
4. Az eredmény kiszámításához válassza az **Optimize** (Optimalizálás) lehetőséget.
5. Hasonlítsa össze az eredeti és az optimalizált hálókat, majd válassza az **Apply** (Alkalmazás) lehetőséget a művelet véglegesítéséhez.
6. Válassza a **Save current state** (Aktuális állapot mentése) lehetőséget, vagy nyomja meg a `Ctrl+S` billentyűt.

A MeshMill soha nem indítja el az optimalizálást pusztán azért, mert egy fájl vagy beállítás megváltozott.

## Funkciók

- Bináris és ASCII STL bemenet, bináris STL kimenet
- Fast QEM: sűrűségkiegyenlített, alak- és topológiamegtartó redukció
- GPU-gyorsított OpenGL nézet, hardveres kiválasztás és sűrűség-vizualizáció
- Natív háttérgeometriai munkások a hálók csökkentésére
- Árnyékolt, sűrűség, drótváz és vertex megjelenítési módok
- Automatikus célbeállítások geometria alapján, fix háromszögszám-korlát helyett
- Poligonkijelölés, több régióra kiterjedő, összeadódó kijelölési lehetőséggel
- Csak a kijelölt régió vágása, törlése vagy optimalizálása
- Gyorsítótárazott összehasonlítás az eredeti, az előző és az aktuális háló között
- Visszavonás és újbóli végrehajtás a véglegesített geometriai módosításoknál
- Méreteltérés, redukciós arány és becsült kimeneti méret
- Megjelenítési mértékegységek: milliméter, centiméter, méter, hüvelyk és láb
- CPU, memória, GPU és geometriai műveleti mutatók
- Korlátozott áttekintő betöltése, ha a bináris STL mérete meghaladja a beállított memóriakeretet
- GUI- és parancssori alkalmazások
- Helyi feldolgozás; nincs szükség fiókra, telemetriára, feltöltésre vagy felhőalapú szolgáltatásra

## Ellenőrizze a geometriát, mielőtt kicsinyítené

Az árnyékolt kijelző tiszta képet ad a felületről és a sziluettről. Hasznos az összehasonlításhoz
alakmegőrzés az optimalizálási lépés alkalmazása előtt.

![MeshMill árnyékolt nézetablak, amely a kötegelt mintahálót mutatja](../../images/meshmill-shaded.png)

A Csúcsok képernyő megjeleníti az aktuális ponteloszlást. Sűrű letapogatási régiók, ritka területek és
a mintavétel hirtelen változásai a geometria megváltoztatása nélkül láthatók. A kibontott metrikapanel
nyomon követi a CPU, a memória, a GPU és a geometria-feldolgozási tevékenységet, miközben dolgozik a hálóval.

![MeshMill Vertices kijelző kiterjesztett teljesítménymutatókkal](../../images/meshmill-vertices.png)

A Wireframe kijelző közvetlenül a háromszög szerkezetet mutatja. Segít azonosítani a szükségtelen sűrűséget,
szabálytalan háromszögelés, és olyan területek, ahol az egyszerűsítés jelentős geometriát eltávolíthat.

![MeshMill Wireframe kijelző a háromszög sűrűségének változását mutatja](../../images/meshmill-wireframe.png)

## Elemezze a hálósűrűséget

A Sűrűség kijelző leképezi a relatív helyi sűrűséget a modellben. A ritka régiók hűvösek maradnak
az egyre sűrűbb területek élénkebb színeken mozognak, így egy pillantással láthatóvá válik az egyenetlen mintavétel.

![MeshMill sűrűségű kijelző, amely a relatív hálósűrűséget mutatja] (docs/images/meshmill-density.png)

A sűrűség elérhető marad az ideiglenes optimalizálás kiértékelése közben. Az eszköztár beszámol a
algoritmus, cél, az eredményül kapott háromszög- és csúcsszámok, csökkentési százalék, méretek és
becsült kimeneti méret az átigazolás alkalmazása előtt.

![MeshMill Density kijelző ideiglenes optimalizálást mutat](../../images/meshmill-density-overview.png)

Tartsa lenyomva a jobb egérgombot, hogy megvizsgáljon egy területet a kör alakú nagyítón keresztül. A nagyított kilátás
a mutató középpontjában marad, és a fő kamera pozíciójának megváltoztatása nélkül felfedi a helyi sűrűséget.

![MeshMill Density kijelző a nézetablak nagyítójával](../../images/meshmill-density-zoom.png)

## Nézetvezérlők

| Bemenet | Művelet |
| --- | --- |
| Középső egérgombbal húzás | Keringés |
| Shift + középső egérgombbal húzás | Eltolás |
| Egérgörgő | Nagyítás a mutató felé |
| Ctrl + egérgörgő | Forgatás az óramutató járásával megegyező vagy ellentétes irányba |
| Nyílbillentyűk | Keringés a nézet középpontja körül |
| Ctrl + nyílbillentyűk | Eltolás |
| Ctrl + Shift + Fel/Le | Nagyítás |
| Ctrl + Shift + Bal/Jobb | Roll |
| `F1` / `F2` / `F3` / `F4` | Árnyékolt / Sűrűség / Drótváz / Csúcsok |
| Jobb egér tartása | Nagyító |
| Shift + bal kattintás | Vonalzópontok hozzáadása vagy eltávolítása |
| Ctrl + balra húzás | Rajzolj egy kiválasztási sokszöget |
| `Ctrl+C` | A sokszög hozzáadása a mentett kijelöléshez |
| `Ctrl+X` | Vágás a kijelöléshez |
| `Ctrl+Space` | A kijelölés optimalizálása |
| `Delete` | Kijelölés törlése |
| `Escape` | Az aktív kijelölés vagy vonalzó törlése |
| `Ctrl+Z` / `Ctrl+Y` | Visszavonás / ismétlés |
| `Ctrl+S` | Az aktuális háló állapot mentése |

A normál nézetbillentyűk a hatgombos navigációs blokkot követik:

| Kulcs | Megtekintés | Ctrl + billentyű |
| --- | --- | --- |
| `Insert` | Bal | Állítsa be az aktuális tájolást Balra |
| `Home` | Elöl | Az aktuális tájolás beállítása Elülső |
| `Page Up` | Jobbra | Állítsa be az aktuális tájolást Jobbra |
| `Delete` | Felül, ha nincs kijelölés | Az aktuális tájolás beállítása Top |
| `End` | Vissza | Az aktuális tájolás beállítása Vissza |
| `Page Down` | Alul | Állítsa be az aktuális tájolást az alsó |

Egy nézet elmentésével az ellenkező nézet is frissül. Bal és jobb, elöl és hátul, valamint felül és alul
párban maradnak. A megerősítő párbeszédpanelen a **Mentés** az alapértelmezett művelet, így az Enter menti a
orientáció. Az Elülső felirat a felső és az alsó nézet tetején is megjelenik.

A parancsikonokat a Beállításokban módosíthatja vagy visszaállíthatja.

## Kiválasztási munkafolyamat

Sokszög rajzolásához tartsa lenyomva a Ctrl billentyűt, és húzza balra. Húzza el a sarkokat az átformáláshoz, kattintson bal gombbal egy élre a hozzáadáshoz
pontot, vagy kattintson a jobb gombbal egy élre az egyik él eltávolításához. Adjon hozzá további régiókat a `Ctrl+C` segítségével. A kamera mozgatása elrejti
a képernyőtér sokszögét, miközben megtartja a kiválasztott geometriát.

Az aktív kijelöléssel végzett optimalizálás csak erre a kijelölésre van hatással. Az eredmény továbbra is ideiglenes
amíg az **Alkalmaz** ki nem választja. A **Mégse** elveti az ideiglenes eredményt, és megtartja a kijelölést
más konfiguráció is kipróbálható. A vágási és törlési műveletek normál, visszavonhatatlan hálószerkesztésekké válnak.

A kijelölőpanel jelenti az összesített kiválasztott csúcsokat, háromszögeket, hálómegosztást, becsült értéket
méretek és méretek. Műveletei levágják, hozzáadják, optimalizálják, törlik, visszalépnek vagy törlik a megtartottakat
kijelölés a környező geometria elrejtése nélkül.

![A MeshMill egy megtartott regionális kijelölést és annak geometriai statisztikáit mutatja](../../images/meshmill-crop-selection.png)

## Nagy hálók

A bináris STL lefoglalása előtt a MeshMill összehasonlítja a becsült munkamemóriáját a konfigurált memóriával.
memória költségvetés. A költségvetés feletti fájl korlátos, csak olvasható áttekintésként nyílik meg. Az áttekintő jelentések
a teljes forrásháromszög száma, de letiltja a szerkesztést és az exportálást, mert ez egy minta, nem a teljes
tárgyat. Indexelt, nagyítástól függő, magon kívüli feldolgozást terveznek
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md).

## Parancssor

A `MeshMillCLI.exe` mindkét kiadási csomagban megtalálható:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

Futtassa a `.\MeshMillCLI.exe --help`-t az összes lehetőséghez. A MeshMill nem hajlandó felülírni a bemeneti fájlját.

## Minta geometria

A fejlesztési mintának két változata érhető el. A minta egy összetett háló
a redundáns geometria és a változó sűrűség szándékos rétegei. Szkenner nélküli embereknek ad a
reális eszköz az algoritmusok összehasonlításához, a sűrűség vizsgálatához, a regionális műveletek végrehajtásához,
és ütemterv-funkciók fejlesztése. A MeshMill nem igényel szkennelt bemenetet.

| Fájl | Háromszögek | Méret | Szállítás | Legjobb a |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249 999 | 11,9 MiB | Normál Git | Gyors kiértékelés, CI és a vezérlőelemek megtanulása | (249,999)
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4,126,315 | 196,8 MiB | Git LFS | A sűrű forrásgeometria és a nagy hálós teljesítmény tesztelése |

A kisebb minta minden normál klónnal letöltődik. Az érintetlen eredeti opcionális és
a Git LFS-n keresztül kezelhető, így nem növeli a szokásos adattárelőzményeket. A GitHub Desktop tartalmazza
Git LFS. A parancssori felhasználók telepíthetik a Git LFS-t és futtathatják:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

A címkézett kiadások az eredeti STL-t is közzéteszik közvetlen letöltésként azok számára, akik nem használják a Git-et.
A származást, a méreteket és az ellenőrző összegeket lásd: [`samples/README.md`](../../../samples/README.md).

Az algoritmus közreműködőinek el kell olvasniuk a
[algoritmus tesztelési útmutató] (docs/ALGORITHM_TESTING.md) a csökkentés összehasonlítása vagy megváltoztatása előtt
viselkedés.

## STL egységek

A STL nem kódol egységet. A modell mértékegységeinek módosítása méretezés nélkül módosítja a címkéket és a méreteket
a mentett koordinátákat. Válassza ki a forrásgeometriát leíró egységet.

## Adatvédelem

A MeshMill helyi fájlokat olvas és ír. Nem tartalmaz fiókot, telemetriát, feltöltést, hirdetést vagy
felhő feldolgozási funkció. A jelenlegi GPU metrikák megvalósítása helyi Windows teljesítményt használ
számlálók. Egyenértékű natív metrikaszolgáltatókat terveznek a Linux és a macOS számára.

A diagnosztikai hibaelhárításhoz a fejlesztők elindíthatják a grafikus felhasználói felületet
`--diagnostic-log <local-file.jsonl>`. A napló helyileg rögzíti a bemeneti útválasztást és a kamera állapotát
normál használat során le van tiltva.

## Fejlesztés és kiadás

A lokalizált felhasználói felület szövege és dokumentációja kezdetben külső gépi fordítással készül
szolgáltatást, és automatikusan ellenőrizni kell a szerkezeti sérüléseket. A gépi fordítás még mindig lehet
természetellenes vagy helytelen. Az anyanyelvi beszélőket arra biztatjuk, hogy nézzék át és javítsák ki a fordításokat
a hozzájárulási folyamat.

- [Hozzájárulás] (CONTRIBUTING.md)
- [Kiadási folyamat] (RELEASING.md)
- [Útiterv] (ROADMAP.md)
- [Hibaelhárítás] (docs/TROUBLESHOOTING.md)
- [Harmadik felek értesítései](THIRD_PARTY_NOTICES.md)

## Támogatja a MeshMill-t

A MeshMill független fejlesztésű és karbantartású. Olvassa el
[miért számít ennek a munkának a támogatása] (SUPPORT.md), vagy támogassa a folyamatos fejlesztést
[Vegyél nekem egy kávét] (https://buymeacoffee.com/tednv).

A MeshMill a GNU General Public License 3-as vagy újabb verziójának licence alá tartozik. Lásd
[`LICENSE`](../../../LICENSE).
