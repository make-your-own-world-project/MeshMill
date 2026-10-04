# MeshMill

![Radharc scáthaithe MeshMill](../../images/meshmill-shaded.png)

Is feidhmchlár deisce tiomnaithe é MeshMill chun geoiméadracht mhogalra atá ró-mhór, dlúth nó deacair a láimhseáil
agus a dhéanamh níos soláimhsithe. Cuireann sé iniúchadh tapa, anailís dlúis, roghnú réigiún, bearradh, scriosadh,
agus laghdú rialaithe ar an mogalra ar fáil, gan gá le cuntas ná le geoiméadracht a uaslódáil.

Coinníonn rindreáil OpenGL luasghéaraithe ag an GPU nascleanúint an amhairc, piocadh crua-earraí, léirshamhlú dlúis agus iniúchadh idirghníomhach freagrúil. Ritheann laghdú mogail faoi láthair i bpróisis dhúchasacha CPU ar leith, ionas nach gcuireann ríomhanna fada geoiméadracha bac ar an gcomhéadan.

Oibríonn MeshMill le mogalraí ó scanóirí 3D, ó chomhaid easpórtáilte CAD agus samhaltú, ó phíblínte athchruthaithe,
ó gheoiméadracht ghinte, agus ó fhoinsí eile STL. Ullmhaíonn sé geoiméadracht d’eagarthóirí iartheachtacha,
d’uirlisí déantúsaíochta, agus do shreafaí oibre mogalra eile. Ní bhaineann sé le samhaltú ginearálta, dealbhóireacht, beochan,
ábhair ná cruthú radharcanna.

## Íoslódáil

Íoslódáil ceann de na comhaid seo ó [Eisiúintí GitHub](../../releases):

- `MeshMill-<version>-windows-x64-setup.exe`: suiteálaí don úsáideoir aonair, le rogha don roghchlár Tosaigh agus
  aicearraí deisce roghnacha.
- `MeshMill-<version>-windows-x64-portable.zip`: feidhmchlár iniompartha. Bain an t-ábhar as an gcartlann ar fad,
  agus ansin rith `MeshMill.exe`.

Tá an t-am rite feidhmchláir san áireamh sa dá phacáiste. Ní shuiteálann úsáideoirí deiridh Python, Node.js, ná
spleáchais. Tacaíonn an chéad eisiúint le Windows 10 agus Windows 11 ar chrua-earraí x64. Tá pacáistí (Linux)
 agus macOS beartaithe; níl formáidí an táirge ná na gcomhad sonrach do Windows.

D’fhéadfadh rabhadh SmartScreen Windows a bheith le feiceáil ar thógálacha pobail neamhshínithe. Tá suimeanna seiceála na n-eisiúintí liostaithe
in `SHA256SUMS.txt` in aice le gach eisiúint.

## Tús tapa

1. Oscail STL.
2. Scrúdaigh é i mód taispeána Scáthaithe (Shaded), Dlúis (Density), Fráma Sreinge (Wireframe), nó Vertices.
3. Roghnaigh leibhéal cáilíochta, algartam, agus sprioc-líon na dtriantán.
4. Roghnaigh **Optimize** chun toradh a ríomh.
5. Déan comparáid idir an mhogalra bhunaidh agus an mhogalra optamaithe, ansin roghnaigh **Apply** chun an pas a chur i bhfeidhm.
6. Roghnaigh **Save current state** nó brúigh `Ctrl+S`.

Ní thosaíonn MeshMill an próiseas optamaithe riamh ach amháin toisc gur athraíodh comhad nó socrú.

## Cumais

- Ionchur dénártha agus ASCII STL, aschur dénártha STL
- Laghdú Fast QEM a choinníonn dlús, cruth agus topolaíocht cothrom
- Modhanna taispeána: scáthaithe, dlús, fráma sreinge, agus veirteics
- Spriocanna uathoibríocha bunaithe ar gheoiméadracht seachas ar uasteorainn shocraithe triantán
- Roghnú polagán le roghnú breise ilréigiún
- Bearr, scrios, nó optamaigh an réigiún roghnaithe amháin
- Comparáid idir an mogall bunaidh, an ceann roimhe seo, agus an ceann reatha (le taisceadh)
- Cealú agus athdhéanamh athruithe geoiméadrachta a cuireadh i bhfeidhm
- Sruth toisí, céatadán laghdaithe, agus meánmhéid aschuir
- Aonaid taispeána: milliméadar, ceintiméadar, méadar, orlach, agus troigh
- Méadrachtaí maidir le CPU, cuimhne, GPU, agus gníomhaíocht gheoiméadrachta
- Lódáil forbhreathnú teoranta nuair a sháraíonn dénártha STL an buiséad cuimhne cumraithe
- GUI agus feidhmchláir ordaithe
- Próiseáil áitiúil gan spleáchas ar chuntas, teileaiméadracht, uaslódáil ná an néal

![Taispeáint dlúis MeshMill](../../images/meshmill-density.png)

## Rialuithe radhairc

| Ionchur | Gníomh |
| --- | --- |
| Tarraingt leis an gcnaipe láir | Fithis |
| Shift + tarraingt leis an gcnaipe láir | Panáil |
| Roth na luiche | Zúmáil i dtreo an phointeora |
| Ctrl + roth na luiche | Rothlú deiseal nó tuathal |
| Eochracha saigheadeolacha | Fithis timpeall lár an amhairc |
| Ctrl + eochracha saigheadeolacha | Panáil |
| Ctrl + Shift + Suas/Síos | Zúmáil |
| Ctrl + Shift + Clé/Deas | Rolla |
| `F1` / `F2` / `F3` / `F4` | Scáthaithe / Dlús / Sreangfhráma / Rinn |
| Coinnigh luch dheas | Formhéadaitheoir |
| Shift + cliceáil ar chlé | Cuir leis nó bain pointí rialóra |
| Ctrl + tarraing clé | Tarraing polagán roghnaithe |
| `Ctrl+C` | Cuir an polagán leis an rogha shábháil |
| `Ctrl+X` | Barr go dtí an roghnú |
| `Ctrl+Space` | Optamaigh an roghnú |
| `Delete` | Scrios an roghnú |
| `Escape` | Glan an roghnú gníomhach nó an rialóir |
| `Ctrl+Z` / `Ctrl+Y` | Cealaigh / athdhéan |
| `Ctrl+S` | Sábháil an staid mhogall reatha |

Leanann na gnáth-eochracha amhairc an bloc loingseoireachta sé eochair:

| Eochair | Amharc | Ctrl + eochair |
| --- | --- | --- |
| `Insert` | Ar chlé | Socraigh treoshuíomh reatha mar Chlé |
| `Home` | Tosaigh | Socraigh treoshuíomh reatha mar Tosaigh |
| `Page Up` | Ar dheis | Socraigh treoshuíomh reatha mar Ar dheis |
| `Delete` | Barr nuair nach bhfuil aon rogha ann | Socraigh treoshuíomh reatha mar Barr |
| `End` | Ar ais | Socraigh treoshuíomh reatha mar Ar Ais |
| `Page Down` | Bun | Socraigh treoshuíomh reatha mar Bhun |

Nuair a shábhálann tú amharc, nuashonraítear a radharc eile freisin. Clé agus Deas, Tosaigh agus Ar Ais, agus Barr agus Bun
fanacht péireáilte. Sa dialóg deimhnithe, is é **Sábháil** an gníomh réamhshocraithe, mar sin sábhálann Enter an
treoshuíomh. Tá an t-aghaidh le feiceáil ag barr an dá radharc Barr agus Bun.

Is féidir aicearraí a athrú nó a athshocrú sna Socruithe.

## Sreabhadh oibre roghnúcháin

Coinnigh Ctrl agus tarraing ar chlé chun polagán a tharraingt. Tarraing coirnéil chun é a athmhúnlú, clé-cliceáil ar imeall chun a
pointe, nó deaschliceáil ar imeall chun ceann a bhaint. Cuir réigiúin níos mó le `Ctrl+C`. Bogadh na seithí ceamara
an polagán spáis scáileáin agus an geoiméadracht roghnaithe á choinneáil.

Ní bhíonn tionchar ag optamú le roghnú gníomhach ach ar an roghnú sin. Tá an toradh sealadach fós
go dtí go roghnófar **Cuir i bhFeidhm**. Déanann **Cealaigh** an toradh sealadach a chaitheamh siar agus coimeádann an roghnúchán amhlaidh
is féidir cumraíocht eile a thriail. Déantar gnáth-athruithe ar mhogall do-dhéanta as oibríochtaí barr agus scrios.

## Mogaill mhóra

Sula ndéantar STL dénártha a leithdháileadh, déanann MeshMill a chuimhne oibre mheasta a chur i gcomparáid leis an gceann cumraithe
buiséad cuimhne. Osclaíonn comhad os cionn an bhuiséid mar fhorbhreathnú teoranta, inléite amháin. Tuairiscíonn na forbhreathnú
an comhaireamh triantán foinse iomlán ach díchumasaítear eagarthóireacht agus easpórtáil toisc gur sampla é, ní an t-iomlán
réad. Tá próiseáil innéacsaithe, súmáil-spleách lasmuigh den chroí beartaithe i
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md).

## Líne ordaithe

Tá `MeshMillCLI.exe` san áireamh sa dá phacáiste scaoilte:

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

Rith `.\MeshMillCLI.exe --help` le haghaidh gach rogha. Diúltaíonn MeshMill a chomhad ionchuir a fhorscríobh.

## Céimseata samplach

Tá dhá leagan den sampla forbartha ar fáil. Is mogalra ilchodach é an sampla le
sraitheanna d'aon ghnó de chéimseata iomarcach agus dlús éagsúil. Tugann sé daoine gan scanóir a
daingneán réalaíoch chun algartaim a chur i gcomparáid, dlús a iniúchadh, oibríochtaí réigiúnacha a fheidhmiú,
agus gnéithe treochláir a fhorbairt. Níl ionchur scanta ag teastáil ó MeshMill.

| Comhad | Triantáin | Méid | Seachadadh | Is fearr le haghaidh |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249,999 | 11.9 MiB | Git Gnáth | Meastóireacht thapa, CI, agus foghlaim na rialuithe |
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4,126,315 | 196.8 MiB | Git LFS | Céimseata foinse dlúth a thástáil agus feidhmíocht mogaill mhóra |

Déantar an sampla níos lú a íoslódáil le gach gnáthchlón. Tá an bunaidh gan teagmháil roghnach agus
a bhainistiú trí Git LFS ionas nach n-ardaíonn sé stair stórtha gnáth. Áirítear GitHub Deasc
Git LFS. Is féidir le húsáideoirí na líne ordaithe Git LFS a shuiteáil agus:

```powershell
git lfs pull --include="samples/original-scan.stl"
```

Foilsíonn eisiúintí tagged an STL bunaidh freisin mar íoslódáil díreach do dhaoine nach n-úsáideann Git.
Féach [`samples/README.md`](../../../samples/README.md) le haghaidh foinse, toisí agus seiceálacha.

Ba cheart do ranníocóirí algartam an
[treoir tástála algartam](docs/ALGORITHM_TESTING.md) roimh an laghdú a chur i gcomparáid nó a athrú
iompar.

## aonaid STL

Ní ionchódaíonn STL aonad. Aonaid Mhúnla a Athrú Athraíonn lipéid agus tomhais gan scálaithe
na comhordanáidí sábháilte. Roghnaigh an t-aonad a chuireann síos ar an gcéimseata foinse.

## Príobháideacht

Léann agus scríobhann MeshMill comhaid áitiúla. Níl aon chuntas, teiliméadracht, uaslódáil, fógraíocht nó
gné próiseála scamall. Úsáideann cur i bhfeidhm méadrach reatha GPU feidhmíocht áitiúil Windows
cuntair. Tá soláthraithe méadrachta dúchasacha coibhéiseacha beartaithe do Linux agus macOS.

Le haghaidh fabhtcheartaithe diagnóiseacha, is féidir le forbróirí an GUI a thosú le
`--diagnostic-log <local-file.jsonl>`. Taifeadann an loga ródú ionchuir agus staid ceamara go háitiúil agus tá
díchumasaithe le linn gnáthúsáide.

## Forbairt agus scaoileadh

- [Ag cur](CONTRIBUTING.md)
- [Próiseas scaoilte](RELEASING.md)
- [Treochlár](ROADMAP.md)
- [Fabhtcheartú](docs/TROUBLESHOOTING.md)
- [Fógraí tríú páirtí](THIRD_PARTY_NOTICES.md)

## Tacaíocht MeshMill

Déantar MeshMill a fhorbairt agus a chothabháil go neamhspleách. Léigh
[cén fáth a bhfuil tábhacht ag baint le tacú leis an obair seo](SUPPORT.md), nó tacú le forbairt leanúnach tríd
[Ceannaigh caife dom](https://buymeacoffee.com/tednv).

Tá MeshMill ceadúnaithe faoin GNU General Public License, leagan 3 nó níos déanaí. Féach
[`LICENSE`](../../../LICENSE).
