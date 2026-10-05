# Sortie de MeshMill

Le pipeline de versions stables crée des artefacts Windows sur les exécuteurs Windows hébergés par GitHub. Un séparé
le flux de travail manuel crée des aperçus non signés Linux x86-64 et macOS Intel/Apple Silicon sur natif
Coureurs hébergés sur GitHub. Les utilisateurs finaux n'installent pas Python, Node.js ou les dépendances.

Avant de créer, actualisez et validez les catalogues sources de localisation :

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
python tools/release_privacy_check.py
```

## Avant la première sortie publique

1. Terminer et valider les traductions prévues de l'application et de la documentation.
2. Consultez la GPL et les avis de tiers.
3. Testez l'installation, le lancement, le chargement, l'optimisation, l'exportation et la désinstallation de STL sur un ordinateur propre.
   Compte Windows ou machine virtuelle.
4. Exécutez CI sur `samples/sample-scan.stl`. Inspectez chaque capture d'écran de la documentation et recadrez-la
   la barre des tâches, la fenêtre chrome qui ne fait pas partie de MeshMill, les notifications, les chemins privés, le compte
   les détails et le contenu du bureau sans rapport avant la publication.
5. Configurez l'auteur Git local du référentiel avec l'adresse de non-réponse GitHub du compte avant le
   premier commit. Confirmez-le avec `git config --local --get user.email`.
6. Configurez les secrets de signature Authenticode facultatifs :
   - `WINDOWS_CERTIFICATE_BASE64` : certificat PFX codé en base64.
   - `WINDOWS_CERTIFICATE_PASSWORD` : mot de passe PFX.

Sans certificat de signature, les fichiers générés fonctionnent toujours, mais Windows SmartScreen peut afficher
un avertissement d'éditeur non reconnu. Ne décrivez pas les builds non signées comme signées ou fiables.

## Numérisation originale et Git LFS

`samples/original-scan.stl` est suivi via Git LFS car il dépasse les 100 Mio normaux de GitHub.
limite de fichier. Avant le premier commit, vérifiez :

```powershell
git check-attr filter -- samples/original-scan.stl
git lfs pointer --file samples/original-scan.stl
```

Le filtre doit être `lfs` et l'ID de l'objet pointeur doit correspondre à `samples/SHA256SUMS.txt`. La libération
Le workflow extrait le contenu LFS et publie le STL d'origine en tant qu'actif de version distinct. Utilisations CI
le plus petit échantillon Git normal et ne télécharge pas l'objet LFS.

## Tester une version de version sans publier

Ouvrez **Actions**, sélectionnez **Release**, choisissez **Exécuter le workflow** et saisissez une version numérique telle que
`0.1.0`. Une exécution manuelle télécharge les artefacts de flux de travail à des fins de test, mais ne crée pas de GitHub public.
Libération.

## Publier une version

À partir d'une branche `main` propre et révisée :

```powershell
git tag -a v0.1.0 -m "MeshMill 0.1.0"
git push origin v0.1.0
```

La balise démarre le workflow de publication. Il :

1. installe les dépendances de build épinglées ;
2. génère des métadonnées de version Windows correspondantes ;
3. construit les exécutables GUI et CLI autonomes ;
4. signe les exécutables lorsque les secrets de signature sont configurés ;
5. construit le programme d'installation d'Inno Setup par utilisateur ;
6. signe le programme d'installation une fois configuré ;
7. crée le fichier de somme de contrôle ZIP et SHA-256 portable ;
8. télécharge des artefacts de flux de travail ;
9. crée la version GitHub pour la balise poussée.

Vérifiez le programme d'installation et l'archive portable sur un système Windows propre avant d'annoncer la sortie.
Conservez la source correspondant à chaque binaire distribué disponible sous la même balise de version.
Confirmez que le bouton GitHub pointe vers l'URL du référentiel public final avant de baliser le premier.
libération.

## Créer des aperçus Linux et macOS

Ouvrez **Actions**, sélectionnez **Builds d'aperçu de plateforme** et choisissez **Exécuter le workflow**. Entrez un aperçu
version telle que « 0.2.0-preview.1 ».

Laissez **Publier une version préliminaire publique de GitHub** désactivée pour la première exécution. Le workflow construit et teste :

- Linux x86-64 sur Ubuntu 22.04 ;
- macOS x86-64 sur un processeur Intel ;
- macOS arm64 sur un coureur de silicium Apple.

Téléchargez les artefacts de flux de travail et inspectez leurs sommes de contrôle et leurs journaux. Exécutez à nouveau le workflow avec
la publication est activée uniquement après la réussite de chaque tâche de build. Les aperçus macOS publiés sont signés ad hoc,
pas certifié par Apple. Décrivez-les en tant que versions préliminaires et associez les testeurs à
`docs/PLATFORM_TESTING.md` et le formulaire de problème **Test d'aperçu de la plateforme**.
