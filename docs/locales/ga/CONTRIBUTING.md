# Ag cur leis

Cuirtear fáilte roimh ranníocaíochtaí trí cheisteanna agus iarratais tarraingthe.

## Scóip an tionscadail

Déanann MeshMill comhaid rómhóra, dlútha nó dheacra atá inbhainistithe le haghaidh eagarthóireacht iartheachtacha agus
sreafaí oibre táirgthe. Ba cheart go bhfeabhsódh ranníocaíochtaí iniúchadh céimseata, mogalra agus dlús pointe
bainistíocht, barrfheabhsú, roghnú, bearradh, glanta, bailíochtú, idirmhalartú STL, feidhmíocht,
nó comhordú na n-oibríochtaí sin.

Ní chuimsíonn an tionscadal samhaltú ilfheidhmeach, dealbhóireacht, péinteáil, beochan, rindreáil,
comhdhéanamh radharc, ábhair, rigging, nó córais eile ábhar-chruthú. Tograí a thugann isteach
tá na gnéithe sin lasmuigh de scóip an tionscadail.

Ba cheart do ghnéithe nua an feidhmchlár a choinneáil dírithe, sreafaí oibre díreacha a chaomhnaíonn foinse a chaomhnú
geoiméadracht ina mogaill inláimhsithe, agus seachain rialtáin tacaíochta a iompú ina n-eagarthóireacht ghinearálta
timpeallacht.

## Logánú

Stóráiltear téacs foinse Chomhéadain Bhéarla i `locales/en-US.json`. Stóráiltear meiteashonraí Locale i
`locales/manifest.json`. Úsáideann catalóga Chomhéadain aistrithe na heochracha cobhsaí céanna agus an t-ainm comhaid
`<locale>.json`. Úsáideann doiciméadú aistrithe an fhréamhainm comhoiriúnach faoi
`docs/locales/<locale>/`.

Táirgtear aistriúcháin ar dtús le seirbhísí meaisín-aistriúcháin seachtracha agus faightear iad
bailíochtú struchtúrach uathoibrithe. Ní féidir leis an bpróiseas sin ráthaíocht a thabhairt go nádúrtha, go beacht go teicniúil, nó
teanga cheart i gcomhthéacs. Spreagtar cainteoirí dúchais chun an Chomhéadain Aistrithe a athbhreithniú agus a cheartú
téacs agus doiciméadú. Ba cheart go gcaomhnódh ceartúcháin aistriúcháin eochracha catalóige, sealbhóirí áite,
orduithe, naisc, tomhais, ainmneacha táirge, agus struchtúr Markdown....

Tar éis duit lipéid, leideanna uirlisí, dialóga nó téacs eile atá le feiceáil ag an úsáideoir a athrú, rith:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
```

Athbhreithnigh athruithe foinse agus eochracha athghinte le chéile.

## Céimseata agus athruithe algartam

Úsáid an geoiméadracht shamplach cuachta agus tú ag athrú leas iomlán a bhaint, anailís dlúis, roghnú, bearradh,
láimhseáil comhad mór, nó iompar comparáide viewport. Tá sraitheanna iomarcacha ann d'aon ghnó
agus dlús míchothrom, mar sin ba cheart go bhfeabhsódh toradh úsáideach soláimhsitheacht gan saobhadh a cheilt,
teorainneacha brí a chaitheamh i leataobh, nó céimseata a chaomhnaíonn algartam eile a bhaint go ciúin.

Taifead an t-ionchur, algartam, socruithe, comhaireamh triantáin, toisí, sruth toisí, am atá caite,
agus scáileáin scáileáin ábhartha le haghaidh comparáidí. Tástáil an dá an daingneán gnáth-Git níos lú agus, nuair a bheidh an
Baineann an t-athrú le céimseata mór nó cisealta, an daingneán bunaidh Git LFS. Ná tune algartam
don daingneán seo amháin. Cuir cásanna beaga sintéiseacha leis don athróg nó don aischéimniú ar leith
thástáil.

Féach [Tástáil algartam agus ranníocaíocht](docs/ALGORITHM_TESTING.md) don seicliosta comparáide.

## Socrú forbartha

1. Suiteáil 64-giotán Python 3.12 ar Windows.
2. Cruthaigh agus gníomhachtaigh timpeallacht fhíorúil.
3. Suiteáil `requirements-dev.txt`.
4. Rith `python meshmill.py` don GUI nó `python meshmill.py --help` le haghaidh úsáid CLI.
5. Rith `python -m py_compile meshmill.py` roimh athrú a chur isteach.

Coinnigh mogaill phríobháideacha, earraí inrite ginte, screenshots ina bhfuil faisnéis phríobháideach, agus áitiúil
eolairí a thógáil as gealltanais. Baineann céimseata tástála in-athdháilte faoi `samples/` lena
foinse, ceadúnas, toisí, agus modh giniúna doiciméadaithe. Ba cheart go n-úsáidfeadh comhaid foinse nua an
Aitheantóir SPDX `GPL-3.0-or-later`.

Bearr gach gabháil scáileáin den doiciméadacht chuig ábhar an fheidhmchláir MeshMill. Ná cuir an
tascbharra, fuinneog chrome neamhghaolmhara, fógraí, sonraí cuntais, cosáin phríobháideacha, nó cúlra
ábhar deisce.
