# Hibaelhárítás

## A Windows blokkolja a letöltést

Az aláíratlan közösségi buildek aktiválhatják a Microsoft Defender SmartScreen-t. Hasonlítsa össze a letöltötteket
fájl SHA-256 hash-je `SHA256SUMS.txt`-vel ugyanabból a GitHub kiadásból. Az aláírt kiadások azonosítják
a kiadójukat a Windows fájl tulajdonságaiban.

## A hordozható build nem indul el

Bontsa ki a teljes ZIP-fájlt a `MeshMill.exe` futtatása előtt. A `_internal` könyvtárnak a következő helyen kell maradnia
mindkét végrehajtható fájlhoz. Ne futtassa a végrehajtható fájlt a ZIP-nézegetőn belülről.

## Áttekintésként egy nagy STL nyílik meg

A becsült működési készlet meghaladja a Beállításokban megadott memóriaköltségkeretet. Áttekintés mód szándékosan
csak olvasható. Csak akkor növelje a költségvetést, ha a gépnek elegendő szabad memóriája van, vagy csökkentse a
hálót, mielőtt szerkesztésre megnyitná.

## Normál nézet nem lett elmentve

Nyomja meg a Ctrl-módosított nézet billentyűparancsát, majd válassza a **Mentés** lehetőséget, vagy nyomja meg az Entert a megerősítésként
párbeszédpanel. Az egyik nézet mentése az ellenkezőjét is frissíti. Az állapotsor a mentett nézetet jelzi.

## A navigációs billentyűparancsok nem reagálnak

Először zárjon be minden modális párbeszédpanelt. Tekintse át vagy állítsa vissza a parancsikonokat a Beállításokban, ha azok testreszabottak. A
Az alapértelmezett nézet billentyűparancsai a Beszúrás, Kezdőlap, Oldal felfelé, Törlés, Befejezés és Oldal lefelé.

## Hozzon létre egy helyi tájolási diagnosztikai naplót

A diagnosztikai naplózás alapértelmezés szerint le van tiltva. A billentyűzet útválasztásának és a kamera állapotának helyi rögzítéséhez:

```powershell
.\MeshMill.exe --diagnostic-log ".\orientation-session.jsonl" "C:\path\mesh.stl"
```

A napló tartalmazhatja a megnyitott fájl elérési útját. Megosztás előtt tekintse át és szerkessze. A háló geometriája nem
a naplóba írva.

## Probléma bejelentése

Tartalmazza a MeshMill verziót, a Windows verziót, a GPU modellt, a hálós háromszögek számát, a pontos cselekvést
sorrendben, és hogy a telepítőt vagy a hordozható csomagot használták-e. Használja az újraterjeszthető mintát
hálót, ha lehetséges. Ne csatoljon privát szkenneléseket vagy diagnosztikai naplókat anélkül, hogy azokat előbb átnézné.
