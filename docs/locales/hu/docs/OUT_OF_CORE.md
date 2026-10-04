# Magon kívüli mesh architektúra

A MeshMill jelenlegi nagy fájlokat tartalmazó biztonsági rendszere megbecsüli a munkamemóriát, mielőtt lefoglalná a teljes
háló. A beállított költségkeretet meghaladó fájlok korlátos navigációs áttekintésként nyílhatnak meg. An
Az áttekintés minta geometria, láthatóan ilyenként azonosítható, és nem szerkeszthető vagy exportálható
bár ez volt a teljes forrás.

A valódi nagyítástól függő részletességhez állandó térbeli indexre van szükség. Az alábbi tervezés ezt határozza meg
következő megvalósítási szakasz.

## Index formátum

Minden forrásháló kap egy verziózott `.meshmill-index` könyvtárat, amely tartalmazza:

- `manifest.json`, a forrás méretével, módosítási idejével, mintavételezett tartalomkivonatokkal, korlátokkal,
  háromszögszám, index verzió, koordináta pontosság és szintleírások;
- oktfaszinttel és Morton-kóddal címzett térbeli lapok;
- egy durva kijelzőháló minden elfoglalt szülőlapkához;
- teljes felbontású háromszög rekordok levéllapokban; és
- határtulajdonlási és átfedési metaadatok a regionális műveletek és összeszerelés során.

Az index létrehozása sorban, korlátos blokkokban olvassa be a forrást. Ideiglenes csempefuttatásokat ír és
atomikusan közzéteszi a jegyzéket, miután minden szükséges fájl átment az ellenőrzésen. Egy megszakított ill
elavult indexet észlel a jegyzékéből, és a teljes megnyitása nélkül folytatható vagy újraépíthető
háló a memóriában.

## Viewport streaming

A nézetablak a csonka kamera és a képernyőtér hibája alapján választja ki a csempéket. Durva szülőlapok vannak
először látható. A látható gyermekcsempék felváltják őket, ahogy a kamera közelebb kerül, míg a képernyőn kívül és
az alacsony ütésálló lapok durva maradnak. A RAM és a VRAM független költségvetéssel rendelkeznek, és a legutóbb használt
gyorsítótárak. A részletek felszabadítása soha nem engedi el a durva teljes objektum-ábrázolást.

Az ütemező ezeket a csempe állapotokat rögzíti: sorban állás, olvasás, feldolgozás, feltöltés, rezidens, sikertelen,
és törölték. A nézetablak állapotonként színezheti a kockákat, és az egyes kockákat annak arányában töltheti ki
haladás. A törlés eltávolítja a részleges eredményeket, és aktívan hagyja az utolsó teljes megjelenítést.

## Feldolgozás és kapacitás

A helyi munkaegység egy csempe, plusz a működéséhez szükséges determinisztikus átfedés. Egyidejűség
korlátozza a jelenleg elérhető RAM, a konfigurált memóriaszázalék, a logikai processzorok száma és
mért munkaegység mérete. A GPU feltöltés és megjelenítés külön VRAM költségvetéssel rendelkezik. Párhuzamosan jelentették
A kapacitás egy becslés, amíg a reprezentatív lapokat meg nem mérik.

A műveletek minden határelemhez egy tulajdonost tartanak meg. Az összeállítás érvényesíti a megosztott határokat,
eltávolítja a duplikációkat, ellenőrzi a számokat és a korlátokat, valamint rögzíti a használt paramétereket. Ugyanaz a munka
Az egység és az eredmény formátum később ütemezhető az elosztott szintézis csomópontok között.

## Biztonsági szabályok

- A globális minta áttekintésnek, nem pedig teljes felbontású nézetablak-részletnek van címkézve.
- Az áttekintés nem írható felül vagy exportálható teljes forráshálóként.
- Az aktuális költségvetést meghaladó, teljes terhelésű kérelmek kifejezett választást igényelnek.
- Az index generálása, a csempe feldolgozása és összeállítása törölhető marad, és megőrzi az előzőt
  komplett állapot.
- A kapacitásértékek becslések, és meghatározzák, hogy az aktuális vagy tervezett motort írják-e le
  párhuzamos csempe végrehajtás.
