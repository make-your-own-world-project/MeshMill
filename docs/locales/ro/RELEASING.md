# Lansarea MeshMill

Conducta de lansare stabilă construiește artefacte Windows pe runnerele Windows găzduite de GitHub. Un separat
fluxul de lucru manual creează previzualizări nesemnate Linux x86-64 și macOS Intel/Apple silicon pe nativ
alergători găzduiți de GitHub. Utilizatorii finali nu instalează Python, Node.js sau dependențe.

Înainte de a construi, reîmprospătați și validați cataloagele surselor de localizare:

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## Înainte de prima lansare publică

1. Finalizați și validați traducerile planificate ale aplicației și ale documentației.
2. Consultați notificările GPL și terțe părți.
3. Testați instalarea, lansarea, încărcarea STL, optimizarea, exportul și dezinstalarea pe o soluție curată
   Cont Windows sau mașină virtuală.
4. Rulați CI împotriva `samples/sample-scan.stl`. Inspectați fiecare captură de ecran de documentație și decupați
   bara de activități, fereastră Chrome care nu face parte din MeshMill, notificări, căi private, cont
   detalii și conținut desktop fără legătură înainte de publicare.
5. Configurați autorul Git local al depozitului cu adresa de fără răspuns a contului GitHub înainte de
   primul comite. Confirmați-o cu `git config --local --get user.email`.
6. Configurați secretele de semnare Authenticode opționale:
   - `WINDOWS_CERTIFICATE_BASE64`: Certificat PFX codificat în Base64.
   - `WINDOWS_CERTIFICATE_PASSWORD`: parola PFX.

Fără un certificat de semnare, fișierele generate încă funcționează, dar Windows SmartScreen poate afișa
un avertisment de editor nerecunoscut. Nu descrieți versiunile nesemnate ca fiind semnate sau de încredere.

## Scanare originală și Git LFS

`samples/original-scan.stl` este urmărit prin Git LFS deoarece depășește cei 100 MiB obișnuiți pentru GitHub
limita de fișiere. Înainte de prima comitere, verificați:

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

Filtrul trebuie să fie `lfs`, iar ID-ul obiectului indicator trebuie să se potrivească cu `samples/SHA256SUMS.txt`. Eliberarea
fluxul de lucru verifică conținutul LFS și publică STL original ca un material de lansare separat. CI utilizeaza
eșantionul mai mic normal-Git și nu descarcă obiectul LFS.

## Testați o versiune de versiune fără publicare

Deschideți **Acțiuni**, selectați **Lans**, alegeți **Run workflow** și introduceți o versiune numerică, cum ar fi
`0.1.0`. O rulare manuală încarcă artefacte ale fluxului de lucru pentru testare, dar nu creează un GitHub public
Eliberare.

## Publicați o ediție

Dintr-o filială `main` curată și revizuită:

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

Eticheta începe fluxul de lucru de lansare. Acesta:

1. instalează dependențele de build fixate;
2. generează metadate ale versiunii Windows care se potrivesc;
3. construiește executabilele GUI și CLI autonome;
4. semnează executabilele când sunt configurate secretele de semnare;
5. creează programul de instalare Inno Setup pentru fiecare utilizator;
6. semnează instalatorul când este configurat;
7. creează fișierul de sumă de control ZIP și SHA-256 portabil;
8. încarcă artefacte ale fluxului de lucru;
9. creează versiunea GitHub pentru eticheta împinsă.

Verificați instalatorul și arhiva portabilă pe un sistem curat Windows înainte de a anunța lansarea.
Păstrați sursa corespunzătoare fiecărui binar distribuit disponibil sub aceeași etichetă de lansare.
Confirmați că butonul GitHub indică adresa URL finală a depozitului public înainte de a eticheta primul
eliberare.

## Creați previzualizări Linux și macOS

Deschideți **Acțiuni**, selectați **Compilări de previzualizare platformă** și alegeți **Run workflow**. Introduceți o previzualizare
versiune precum `0.2.0-preview.1`.

Lăsați dezactivat **Publicați o versiune preliminară GitHub publică** pentru prima rulare. Fluxul de lucru creează și testează:

- Linux x86-64 pe Ubuntu 22.04;
- macOS x86-64 pe un rulant Intel;
- macOS arm64 pe un rulant de silicon Apple.

Descărcați artefactele fluxului de lucru și inspectați-le sumele de verificare și jurnalele. Rulați din nou fluxul de lucru cu
publicarea este activată numai după trecerea fiecărei lucrări de construcție. Previzualizările macOS publicate sunt semnate ad-hoc,
nu notariat Apple. Descrieți-le ca versiuni de previzualizare și conectați testerii la
`docs/PLATFORM_TESTING.md` și formularul de emisiune **Testul de previzualizare a platformei**.
