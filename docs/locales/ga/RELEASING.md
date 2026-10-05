# MeshMill á scaoileadh

Tógann an píblíne scaoileadh cobhsaí déantáin Windows ar reathaithe Windows arna óstáil ag GitHub. A leithleach
Tógann sreabhadh oibre láimhe réamhamhairc sileacain Linux x86-64 agus macOS Intel/Apple gan síniú ar dhúchas
Ritheoirí arna óstáil ag GitHub. Ní shuiteálann úsáideoirí deiridh Python, Node.js, nó spleáchais.

Sula ndéantar na catalóga foinse logánaithe a thógáil, a athnuachan agus a bhailíochtú:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## Roimh an chéad eisiúint poiblí

1. Críochnaigh agus bailíochtaigh an t-iarratas atá beartaithe agus na haistriúcháin doiciméadaithe.
2. Déan athbhreithniú ar an GPL agus ar na fógraí tríú páirtí.
3. Suiteáil tástála, seoladh, luchtú STL, leas iomlán a bhaint as, onnmhairiú agus díshuiteáil ar ghlan
   Cuntas Windows nó meaisín fíorúil.
4. Rith CI i gcoinne `samples/sample-scan.stl`. Iniúchadh a dhéanamh ar gach gabháil scáileáin doiciméad agus barr amach
   an tascbharra, fuinneog chrome nach bhfuil mar chuid de MeshMill, fógraí, cosáin phríobháideacha, cuntas
   sonraí, agus ábhar deisce nach mbaineann le hábhar roimh fhoilsiú.
5. Cumraigh an t-údar Git stór-áitiúil le seoladh neamhfhreagartha GitHub an chuntais roimh an
   gealltanas ar dtús. Deimhnigh é le `git config --local --get user.email`.
6. Cumraigh rúin sínithe Authenticode roghnach:
   - `WINDOWS_CERTIFICATE_BASE64`: Teastas PFX ionchódaithe Base64.
   - `WINDOWS_CERTIFICATE_PASSWORD`: pasfhocal PFX.

Gan teastas sínithe, oibríonn na comhaid ginte fós, ach seans go dtaispeánfaidh Windows SmartScreen
rabhadh foilsitheora nach n-aithnítear. Ná cuir síos ar thógálacha neamhshínithe mar nithe sínithe nó iontaofa.

## Scanadh bunaidh agus Git LFS

Déantar `samples/original-scan.stl` a rianú trí Git LFS toisc go sáraíonn sé gnáth-100 MiB GitHub
teorainn comhaid. Roimh an gcéad ghealltanas, fíoraigh:

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

Ní mór an scagaire a bheith `lfs`, agus ní mór ID an réad pointeora a mheaitseáil `samples/SHA256SUMS.txt`. An scaoileadh
seiceálann sreabhadh oibre ábhar LFS agus foilsíonn sé an STL bunaidh mar shócmhainn scaoilte ar leithligh. Úsáideann CI
an sampla normal-Git níos lú agus ní íoslódálann sé an réad LFS.

## Tástáil a dhéanamh ar thógáil scaoileadh gan fhoilsiú

Oscail **Gníomhartha**, roghnaigh **Scaoileadh**, roghnaigh **Rith sreabhadh oibre**, agus cuir isteach leagan uimhriúil ar nós
`0.1.0`. Uaslódálann rith láimhe déantáin sreafa oibre le haghaidh tástála ach ní chruthaíonn sé GitHub poiblí
Scaoileadh.

## Eisiúint a fhoilsiú

Ó bhrainse glan, athbhreithnithe `main`:

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

Tosaíonn an chlib an sreabhadh oibre scaoileadh. sé:

1. shuiteáil na spleáchais tógála pinned;
2. gineann meiteashonraí leagan Windows meaitseáilte;
3. tógann sé na nithe féin-chuimsitheach GUI agus CLI;
4. síníonn sé na míreanna inrite nuair a bhíonn rúin sínithe cumraithe;
5. tógann sé an suiteálaí Inno Setup in aghaidh an úsáideora;
6. síníonn sé an suiteálaí nuair a bheidh sé cumraithe;
7. cruthaíonn sé an ZIP iniompartha agus an comhad seiceála SHA-256;
8. uaslódálann artifacts sreabhadh oibre;
9. cruthaíonn an GitHub Release don chlib bhrú.

Fíoraigh an suiteálaí agus an chartlann iniompartha ar chóras glan Windows sula bhfógrófar an scaoileadh.
Coinnigh an fhoinse a fhreagraíonn do gach dénártha dáilte atá ar fáil faoin gclib scaoileadh céanna.
Deimhnigh go díríonn an cnaipe GitHub chuig an URL taisclainne poiblí deiridh roimh chlibeáil an chéad cheann
scaoileadh.

## Tóg réamhamhairc Linux agus macOS

Oscail **Gníomhartha**, roghnaigh **Tógann réamhamharc ardán**, agus roghnaigh **Rith sreabhadh oibre**. Cuir isteach réamhamharc
leagan ar nós `0.2.0-réamhamharc.1`.

Fág **Foilsigh réamheisiúint phoiblí GitHub** as don chéad rith. Tógann agus tástálacha an sreabhadh oibre:

- Linux x86-64 ar Ubuntu 22.04;
- macOS x86-64 ar rádala Intel;
- macOS arm64 ar rádala sileacain Apple.

Íoslódáil na déantáin sreafa oibre agus scrúdaigh a gcuid seiceálacha agus logaí. Rith an sreabhadh oibre arís le
foilsiú cumasaithe ach amháin tar éis do gach post tógála pas a fháil. Tá réamhamhairc macOS foilsithe sínithe ad-hoc,
ní Apple-notarized. Déan cur síos orthu mar thógáil réamhamhairc agus nascann na tástálaithe le
`docs/PLATFORM_TESTING.md` agus an fhoirm eisiúna **Tástáil Réamhamhairc Ardáin**.
