# Fabhtcheartú

## Windows bloc an íoslódáil

Is féidir le tógálacha pobail gan síniú tús le Microsoft Defender SmartScreen. Déan comparáid idir an íoslódáil
hash an chomhaid SHA-256 le `SHA256SUMS.txt` ón Scaoileadh GitHub céanna. Aithníonn eisiúintí sínithe
a bhfoilsitheoir i airíonna comhaid Windows.

## Ní thosaíonn an tógáil iniompartha

Sliocht an ZIP iomlán roimh `MeshMill.exe` a rith. Ní mór don eolaire `_internal` fanacht ina dhiaidh sin
don dá inrite. Ná rith an inrite ón taobh istigh den amharcóir ZIP.

## Osclaíonn STL mór mar fhorbhreathnú

Sáraíonn an tacar oibre measta an buiséad cuimhne sna Socruithe. Is modh forbhreathnú go hintinneach
inléite amháin. Méadaigh an buiséad ach amháin nuair a bhíonn go leor cuimhne ar fáil ar an meaisín, nó laghdaigh an
mogalra sula n-osclaítear é le haghaidh eagarthóireachta.

## Níor sábháladh radharc caighdeánach

Brúigh an t-aicearra amhairc Ctrl-modhnaithe, ansin roghnaigh **Sábháil** nó brúigh Iontráil sa deimhniú
dialóg. Nuair a shábhálann tú radharc amháin, nuashonraítear a mhalairt. Tuairiscíonn an líne stádais an t-amharc sábháilte.

## Ní fhreagraíonn aicearraí nascleanúna

Dún aon dialóg módúil ar dtús. Athbhreithnigh nó athshocraigh aicearraí sna Socruithe má rinneadh iad a shaincheapadh. Tá an
Úsáideann aicearraí réamhshocraithe amhairc Ionsáigh, Baile, Leathanach Suas, Scrios, Críochnaigh agus Leathanach Síos.

## Cruthaigh loga diagnóiseach treoshuímh áitiúil

Díchumasaítear logáil dhiagnóiseach de réir réamhshocraithe. Chun ródú méarchláir agus staid ceamara a thaifeadadh go háitiúil:

```powershell
.\MeshMill.exe --diagnostic-log ".\orientation-session.jsonl" "C:\path\mesh.stl"
```

D'fhéadfadh go mbeadh cosán an chomhaid oscailte sa logáil. Athbhreithnigh agus athbhreithnigh é roimh é a roinnt. Níl céimseata mogalra
scríofa chuig an log.

## Tuairiscigh fadhb

Cuir san áireamh an leagan MeshMill, leagan Windows, samhail GPU, comhaireamh triantán mogalra, gníomh cruinn
seicheamh, agus cibé ar úsáideadh an suiteálaí nó an pacáiste iniompartha. Bain úsáid as an sampla athdháilte
mogalra nuair is féidir. Ná ceangail scananna príobháideacha ná logaí diagnóiseacha gan athbhreithniú a dhéanamh orthu ar dtús.
