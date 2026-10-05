# Hozzájárulás

A hozzászólásokat kérdéseken és kéréseken keresztül várjuk.

## Projekt hatóköre

A MeshMill a túlméretezett, sűrű vagy nehéz hálófájlokat kezelhetővé teszi a későbbi szerkesztéshez és
gyártási munkafolyamatok. A hozzájárulásoknak javítaniuk kell a geometria vizsgálatát, a háló- és pontsűrűséget
kezelés, optimalizálás, kiválasztás, vágás, tisztítás, érvényesítés, STL csere, teljesítmény,
vagy azon műveletek koordinálása.

A projekt nem tartalmaz általános célú modellezést, szobrászatot, festést, animációt, renderelést,
jelenetkompozíció, anyagok, kötélzet vagy egyéb tartalom-létrehozó rendszerek. Javaslatok, amelyek bemutatják
ezek a funkciók kívül esnek a projekt hatókörén.

Az új funkcióknak meg kell őrizniük az alkalmazást, meg kell őrizniük a közvetlen munkafolyamatokat, amelyek a forrást váltják
a geometriát kezelhető hálókká alakítsa át, és kerülje a támogató vezérlők általános szerkesztéssé való átalakítását
környezet.

## Lokalizáció

Az angol felhasználói felület forrásszövege a `locales/en-US.json`-ben van tárolva. A nyelvi metaadatok tárolása a következő helyen történik:
`locales/manifest.json`. A lefordított felhasználói felület katalógusok ugyanazokat a stabil kulcsokat és a fájlnevet használják
`<locale>.json`. A lefordított dokumentáció a megfelelő gyökér fájlnevet használja
`docs/locales/<locale>/`.

A fordításokat kezdetben külső gépi fordítási szolgáltatásokkal állítják elő és fogadják
automatizált szerkezeti érvényesítés. Az a folyamat nem garantálja a természetes, technikailag pontos, ill
kontextus szerint helyes nyelvezet. Az anyanyelvi beszélőket arra biztatjuk, hogy nézzék át és javítsák ki a lefordított felhasználói felületet
szöveg és dokumentáció. A fordítási javításoknak meg kell őrizniük a katalóguskulcsokat, a helyőrzőket,
parancsok, hivatkozások, mérések, terméknevek és Markdown szerkezet.

A címkék, elemleírások, párbeszédpanelek vagy más, a felhasználó által látható szövegek módosítása után futtassa:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
```

Tekintse át együtt a forrásmódosításokat és az újragenerált kulcsokat.

## Geometria és algoritmus változások

Használja a kötegelt minta geometriát az optimalizálás, a sűrűségelemzés, a kiválasztás, a kivágás,
nagy fájlkezelés vagy nézetablak összehasonlítási viselkedés. Szándékosan tartalmaz redundáns rétegeket
és egyenetlen sűrűség, így a hasznos eredmény javítja a kezelhetőséget a torzítások elrejtése nélkül,
értelmes határok elvetése, vagy egy másik algoritmus által megőrzött geometria csendben történő eltávolítása.

Rögzítse a bemenetet, az algoritmust, a beállításokat, a háromszögek számát, a méreteket, a méreteltolódást, az eltelt időt,
és releváns képernyőképeket az összehasonlításhoz. Tesztelje a kisebb normál-Git fixture-t és ha a
a változás nagy vagy réteges geometriát érint, az eredeti Git LFS lámpatestet. Ne hangoljon algoritmust
egyedül ehhez a berendezéshez. Adjon hozzá kis szintetikus eseteket az adott invariáns vagy regressziós lényhez
tesztelve.

Az összehasonlító ellenőrzőlistát lásd: [Algoritmus tesztelése és hozzájárulás] (docs/ALGORITHM_TESTING.md).

## Fejlesztési beállítás

1. Telepítse a 64 bites Python 3.12-t a Windows-re.
2. Virtuális környezet létrehozása és aktiválása.
3. Telepítse a `requirements-dev.txt`-t.
4. Futtassa a `python meshmill.py`-t a grafikus felhasználói felülethez, vagy a `python meshmill.py --help`-t a CLI használatához.
5. A módosítás benyújtása előtt futtassa a `python -m py_compile meshmill.py` fájlt.

Tartsa meg a privát hálókat, a generált végrehajtható fájlokat, a személyes információkat tartalmazó képernyőképeket és a helyi fájlokat
könyvtárakat építeni a véglegesítésekből. Az újraelosztható tesztgeometria a `samples/` alá tartozik
forrás, licenc, méretek és generálási módszer dokumentálva. Az új forrásfájloknak a
SPDX azonosító: `GPL-3.0-or-later`.

Vágjon le minden dokumentációs képernyőképet a MeshMill alkalmazás tartalmára. Ne tartalmazza a
tálca, nem kapcsolódó ablak króm, értesítések, fiókadatok, privát útvonalak vagy háttér
asztali tartalom.
