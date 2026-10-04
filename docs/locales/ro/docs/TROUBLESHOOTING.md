# Depanare

## Windows blochează descărcarea

Compilările comunității nesemnate pot declanșa Microsoft Defender SmartScreen. Comparați cele descărcate
hash-ul SHA-256 al fișierului cu `SHA256SUMS.txt` din aceeași versiune GitHub. Versiunile semnate identifică
editorul lor în proprietățile fișierului Windows.

## Construcția portabilă nu pornește

Extrageți codul ZIP complet înainte de a rula `MeshMill.exe`. Directorul `_internal` trebuie să rămână următorul
la ambele executabile. Nu rulați executabilul din interiorul vizualizatorului ZIP.

## Un STL mare se deschide ca o prezentare generală

Setul de lucru estimat depășește bugetul de memorie din Setări. Modul de prezentare generală este intenționat
numai pentru citire. Măriți bugetul numai atunci când aparatul are suficientă memorie disponibilă sau reduceți
plasă înainte de a-l deschide pentru editare.

## O vizualizare standard nu a fost salvată

Apăsați comanda rapidă pentru vizualizarea modificată prin Ctrl, apoi alegeți **Salvare** sau apăsați Enter în confirmare
dialog. Salvarea unei vizualizări actualizează și opusul ei. Linia de stare raportează vizualizarea salvată.

## Comenzile rapide de navigare nu răspund

Închideți mai întâi orice dialog modal. Examinați sau resetați comenzile rapide din Setări, dacă au fost personalizate. The
Comenzile rapide de vizualizare implicite folosesc Inserare, Acasă, Pagina sus, Ștergere, Sfârșit și Pagina în jos.

## Creați un jurnal de diagnostic de orientare locală

Înregistrarea de diagnosticare este dezactivată în mod implicit. Pentru a înregistra local rutarea tastaturii și starea camerei:

```powershell
.\MeshMill.exe --diagnostic-log ".\orientation-session.jsonl" "C:\path\mesh.stl"
```

Jurnalul poate conține calea fișierului deschis. Examinați-l și redactați-l înainte de distribuire. Geometria plasei nu este
scris în jurnal.

## Raportați o problemă

Includeți versiunea MeshMill, versiunea Windows, modelul GPU, numărul triunghiului de plasă, acțiunea exactă
secvența și dacă a fost folosit programul de instalare sau pachetul portabil. Utilizați eșantionul redistribuibil
plasă atunci când este posibil. Nu atașați scanări private sau jurnale de diagnosticare fără a le examina mai întâi.
