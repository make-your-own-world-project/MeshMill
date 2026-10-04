# MeshMill kiadás

A kiadási folyamat Windows műtermékeket épít a GitHub által hosztolt Windows futókra. A végfelhasználók megkapják
egy önálló telepítő vagy hordozható ZIP, és ne telepítse a Python, Node.js vagy függőségeket.

Építés előtt frissítse és érvényesítse a lokalizációs forráskatalógusokat:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## Az első nyilvános megjelenés előtt

1. Fejezze be és érvényesítse a tervezett pályázati és dokumentációs fordításokat.
2. Tekintse át a GPL és a harmadik fél értesítéseit.
3. Teszttelepítés, indítás, STL betöltés, optimalizálás, exportálás és eltávolítás tiszta felületen
   Windows fiók vagy virtuális gép.
4. Futtassa a CI-t a `samples/sample-scan.stl` ellen. Vizsgáljon meg minden dokumentáció képernyőképet, és vágja ki
   a tálca, ablak króm, amely nem része a MeshMill-nek, értesítések, privát elérési utak, fiók
   részleteket és a nem kapcsolódó asztali tartalmat közzététel előtt.
5. Konfigurálja a repository-local Git szerzőt a fiók GitHub válasz nélküli címével, mielőtt
   első elköteleződés. Erősítse meg a `git config --local --get user.email`-vel.
6. Állítsa be az opcionális hitelesítőkód-aláírási titkokat:
   - `WINDOWS_CERTIFICATE_BASE64`: Base64 kódolású PFX tanúsítvány.
   - `WINDOWS_CERTIFICATE_PASSWORD`: PFX jelszó.

Aláíró tanúsítvány nélkül a generált fájlok továbbra is működnek, de a Windows SmartScreen megjelenhet
egy fel nem ismert kiadó figyelmeztetése. Az aláíratlan buildeket ne írja alá aláírtnak vagy megbízhatónak.

## Eredeti szkennelés és Git LFS

A `samples/original-scan.stl` a Git LFS-n keresztül követhető, mert meghaladja a GitHub normál 100 MiB-jét
fájlkorlát. Az első véglegesítés előtt ellenőrizze:

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

A szűrőnek `lfs` értékűnek kell lennie, és a mutatóobjektum azonosítójának egyeznie kell a `samples/SHA256SUMS.txt` formátummal. A kiadás
munkafolyamat ellenőrzi az LFS-tartalmat, és külön kiadási eszközként teszi közzé az eredeti STL-t. CI használ
a kisebb normál Git mintát, és nem tölti le az LFS objektumot.

## Teszteljen egy kiadási buildet közzététel nélkül

Nyissa meg a **Műveletek** lehetőséget, válassza a **Kiadás** lehetőséget, válassza a **Munkafolyamat futtatása** lehetőséget, és adja meg a numerikus verziót, például
`0.1.0`. A kézi futtatás feltölti a munkafolyamat-termékeket tesztelés céljából, de nem hoz létre nyilvános GitHub-t
Kiadás.

## Közzététel közzététele

Egy tiszta, átvizsgált `main` fiókból:

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

A címke elindítja a kiadási munkafolyamatot. Ez:

1. telepíti a rögzített összeállítási függőségeket;
2. megfelelő Windows verzió metaadatokat állít elő;
3. összeállítja az önálló GUI és CLI végrehajtható fájlokat;
4. aláírja a végrehajtható fájlokat az aláírási titkok beállításakor;
5. létrehozza a felhasználónkénti Inno Setup telepítőt;
6. konfigurálva aláírja a telepítőt;
7. létrehozza a hordozható ZIP és SHA-256 ellenőrzőösszeg fájlt;
8. feltölti a munkafolyamat-termékeket;
9. létrehozza a GitHub kiadást a kitolt címkéhez.

A kiadás bejelentése előtt ellenőrizze a telepítőt és a hordozható archívumot egy tiszta Windows rendszeren.
Tartsa meg minden elosztott binárisnak megfelelő forrást ugyanazon kiadási címke alatt.
Győződjön meg arról, hogy a GitHub gomb a végső nyilvános adattár URL-címére mutat, mielőtt megcímkézi az első
kiadás.
