# Ailtireacht mogalra lasmuigh den chroí

Measann cosaint mhórchomhaid reatha MeshMill cuimhne oibre sula leithdháilfear iomlán
mogalra. Is féidir comhaid a sháraíonn an buiséad cumraithe a oscailt mar fhorbhreathnú nascleanúna teoranta. An
is céimseata samplach é forbhreathnú, sainaithnítear é mar sin go feiceálach, agus ní féidir é a chur in eagar nó a easpórtáil mar
cé gurbh é an fhoinse iomlán é.

Tá innéacs spásúlachta marthanach ag teastáil ó fhíor mhionsonraí súmáil-spleách. Sainmhíníonn an dearadh thíos é sin
an chéad chéim eile cur i bhfeidhm.

## Formáid innéacs

Faigheann gach mogalra foinse eolaire `.meshmill-index` leagan ina bhfuil:

- `manifest.json`, leis an méid foinse, am modhnú, hashes ábhar sampláilte, teorainneacha,
  comhaireamh triantáin, leagan innéacs, cruinneas a chomhordú, agus cur síos ar leibhéil;
- tíleanna spásúla dírithe ag leibhéal ochtrí agus cód Morton;
- mogalra taispeána garbh do gach tíl tuismitheora áitithe;
- taifid triantáin lántaifeach i tíleanna duille; agus
- úinéireacht teorann agus meiteashonraí forluiteacha a úsáidtear le linn oibríochtaí réigiúnacha agus tionóil.

Léann cruthú innéacs an fhoinse go seicheamhach i mbloic teorann. Scríobhann sé ritheann tíl sealadach agus
Foilsíonn atomically an léiriú tar éis gach comhad riachtanach bailíochtú. Idirbhriseadh nó
aimsítear an t-innéacs sean óna léiriú agus is féidir é a atosú nó a atógáil gan an t-iomlán a oscailt
mogalra i gcuimhne.

## Viewport sruthú

Roghnaíonn an t-amharcmharc tíleanna trí úsáid a bhaint as frustum an cheamara agus earráid spáis scáileáin. Tá tíleanna tuismitheora garbh
léirithe ar dtús. Cuirtear tíleanna leanaí infheicthe ina n-áit de réir mar a ghluaiseann an ceamara níos gaire, agus é as an scáileán agus
tá tíleanna íseal-thionchar fós garbh. Tá buiséid neamhspleácha ag RAM agus VRAM agus is lú a úsáideadh le déanaí
taisce. Ní scaoileann sonraí a scaoileadh an léiriú garbh uile-ábhar ar fad.

Taifeadann an sceidealóir na stáit tíl seo: ciúáilte, léamh, próiseáil, uaslódáil, cónaitheoir, teipthe,
agus curtha ar ceal. Is féidir leis an radharc cubanna a dhathú de réir stáit agus gach ciúb a líonadh i gcomhréir lena
dul chun cinn. Baineann cealú torthaí páirteacha agus fágtar an léiriú iomlán deireanach gníomhach.

## Próiseáil agus cumas

Is tíl é aonad oibre áitiúil móide an forluí cinntitheach a theastaíonn dá oibriú. Comhairgeadra
cuirtear teorainn leis an RAM atá ar fáil faoi láthair, céatadán cuimhne cumraithe, comhaireamh próiseálaí loighciúil, agus
méid aonad oibre tomhaiste. Tá buiséad ar leith VRAM ag uaslódáil agus taispeáint GPU. Tuairiscíodh comhthreomhar
is meastachán é toilleadh go dtí go mbeidh tíleanna ionadaíocha tomhaiste.

Coinníonn oibríochtaí úinéir amháin do gach eilimint teorann. Déanann an Tionól teorainneacha comhroinnte a bhailíochtú,
baintear dúblaigh, seiceálann sé comhaireamh agus teorainneacha, agus taifeadann sé na paraiméadair bheachta a úsáidtear. An obair chéanna
is féidir formáid aonaid agus torthaí a sceidealú níos déanaí trasna nóid shintéise dáilte.

## Rialacha sábháilteachta

- Tá sampla domhanda lipéadaithe mar fhorbhreathnú, ní mar mhionsonraí amhairc lántaifigh.
- Ní féidir forbhreathnú a fhorscríobh ná a easpórtáil mar mhogalra iomlán na foinse.
- Teastaíonn rogha shainráite maidir le hiarratais lánualaigh a sháraíonn an buiséad reatha.
- Tá giniúint innéacs, próiseáil tíleanna, agus cóimeáil fós inchealaithe agus caomhnaíonn siad an ceann roimhe sin
  staid iomlán.
- Is meastacháin iad luachanna acmhainne agus sainaithnítear cé acu an gcuireann siad síos ar an inneall reatha nó an bhfuil sé beartaithe
  forghníomhú tíl comhthreomhar.
