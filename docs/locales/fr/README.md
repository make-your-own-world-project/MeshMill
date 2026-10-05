<p align="center">
  <img src="assets/meshmill-logo.svg" width="620" alt="MeshMill: Dirty geometry? Clean it up!">
</p>

<!-- localization-navigation:start -->
<p align="center">
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/README.md">English</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ar/README.md">العربية</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/bn/README.md">বাংলা</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/de/README.md">Deutsch</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/el/README.md">Ελληνικά</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/es/README.md">Español</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/fa/README.md">فارسی</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/fr/README.md">Français</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ga/README.md">Gaeilge</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/hi/README.md">हिन्दी</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/hu/README.md">Magyar</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/id/README.md">Bahasa Indonesia</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/it/README.md">Italiano</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ja/README.md">日本語</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ko/README.md">한국어</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/nl/README.md">Nederlands</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/pl/README.md">Polski</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/pt/README.md">Português</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ro/README.md">Română</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ru/README.md">Русский</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/sr/README.md">Српски</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/th/README.md">ไทย</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/tr/README.md">Türkçe</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/uk/README.md">Українська</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/ur/README.md">اردو</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/vi/README.md">Tiếng Việt</a> ·
  <a href="https://github.com/make-your-own-world-project/MeshMill/blob/main/docs/locales/zh-CN/README.md">简体中文</a>
</p>
<!-- localization-navigation:end -->

MeshMill est une application de bureau spécialisée conçue pour rendre gérables les géométries de maillage
volumineuses, denses ou complexes. Elle permet une inspection rapide, l'analyse de la densité, la sélection par zone, le découpage, la suppression,
ainsi qu'une réduction contrôlée du maillage, sans nécessiter de compte ni de téléchargement de la géométrie vers un serveur.

Le rendu OpenGL accéléré par GPU conserve la navigation dans les fenêtres, la sélection du matériel, la visualisation de la densité,
et une inspection interactive réactive. La réduction du maillage s'exécute actuellement sur des processeurs natifs distincts, (CPU)
en gardant les longs calculs de géométrie à l’écart de l’interface.

MeshMill prend en charge les maillages issus de scanners 3D, d'exports CAO et de modélisation, de chaînes de reconstruction,
de géométries générées et d'autres sources STL. Elle prépare la géométrie pour des logiciels d'édition en aval,
des outils de fabrication et d'autres flux de travail liés aux maillages. La modélisation généraliste, la sculpture, l'animation,
la gestion des matériaux et la création de scènes sortent de son champ d'application.

## Téléchargement

Choisissez votre système d'exploitation. Chaque package est autonome. Python, Node.js et autres
les dépendances de développement ne sont pas requises.

| Système | Téléchargement recommandé | Statut |
| --- | --- | --- |
| **Windows x64** | **[Téléchargez le programme d'installation de Windows][windows-installer]** | Version prise en charge |
| Windows x64, aucune installation | [Télécharger le ZIP portable][windows-portable] | Version prise en charge |
| Linux x86-64 | [Télécharger l'aperçu Linux][linux-preview] | Aperçu des premiers tests |
| macOS Apple silicium | [Téléchargez l'aperçu du silicium Apple][mac-arm-preview] | Aperçu des premiers tests |
| macOS Intel | [Télécharger l'aperçu Intel Mac][mac-intel-preview] | Aperçu des premiers tests |

**La plupart des utilisateurs de Windows devraient choisir le programme d'installation de Windows.** Utilisez le ZIP portable uniquement lorsque vous le faites
Je ne veux pas que MeshMill soit installé ou je n'ai pas l'autorisation d'installer des applications.

Les packages Linux et macOS sont des versions préliminaires non signées. Ils réussissent les builds natifs automatisés et
des tests de fumée packagés, mais nécessitent toujours des tests sur le matériel réel. Lire le
[Notes d'aperçu Linux et macOS](../../PLATFORM_TESTING.md) avant de les installer.

Windows SmartScreen ou macOS Gatekeeper peuvent avertir des packages non signés.
Un exemple de maillage facultatif est inclus avec la version Windows prise en charge : [STL][sample-mesh].
Les anciennes versions et les sommes de contrôle de téléchargement sont disponibles sur [GitHub Releases][all-releases].

[windows-installer]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-0.1.1-windows-x64-setup.exe
[windows-portable]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-0.1.1-windows-x64-portable.zip
[linux-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-linux-x86_64.tar.gz
[mac-arm-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-arm64.zip
[mac-intel-preview]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.2.0-preview.2/MeshMill-0.2.0-preview.2-macos-x86_64.zip
[sample-mesh]: https://github.com/make-your-own-world-project/MeshMill/releases/download/v0.1.1/MeshMill-sample-scan-original.stl
[all-releases]: https://github.com/make-your-own-world-project/MeshMill/releases

## Démarrage rapide

1. Ouvrez un STL.
2. Examinez-le en mode d'affichage Ombré, Densité, Fil de fer ou Sommets.
3. Choisissez un niveau de qualité, un algorithme et un nombre de triangles cible.
4. Sélectionnez **Optimiser** pour calculer un résultat.
5. Comparez les maillages original et optimisé, puis sélectionnez **Appliquer** pour valider l'opération.
6. Sélectionnez **Enregistrer l'état actuel** ou appuyez sur `Ctrl+S`.

MeshMill ne lance jamais l'optimisation simplement parce qu'un fichier ou un paramètre a été modifié.

## Fonctionnalités

- Entrée au format binaire et ASCII, sortie au format binaire (STL) (STL)
- Réduction préservant la densité, la forme et la topologie (Fast QEM)
- Fenêtre d'affichage OpenGL accélérée par GPU, sélection du matériel et visualisation de la densité
- Travailleurs de géométrie d'arrière-plan natifs pour la réduction du maillage
- Modes d'affichage : ombré, densité, filaire et sommets
- Cibles automatiques basées sur la géométrie plutôt que sur un nombre maximal de triangles fixe
- Sélection de polygones avec possibilité de sélection additive multi-zone
- Recadrage, suppression ou optimisation de la zone sélectionnée uniquement
- Comparaison entre les maillages original, précédent et actuel (avec mise en cache)
- Annulation et rétablissement des modifications géométriques appliquées
- Dérive dimensionnelle, pourcentage de réduction et taille de sortie estimée
- Unités d'affichage : millimètre, centimètre, mètre, pouce et pied
- Métriques relatives au maillage, à la mémoire et à l'activité géométrique (CPU) (GPU)
- Chargement d'une vue d'ensemble limitée lorsque le fichier d'entrée dépasse le budget mémoire configuré (STL)
- Applications avec interface graphique (GUI) et ligne de commande
- Traitement local sans dépendance vis-à-vis d'un compte, de la télémétrie, de téléchargements ou du cloud

## Inspecter la géométrie avant de la réduire

L'affichage ombré offre une vue nette de la surface et de la silhouette. C'est utile pour comparer
préservation de la forme avant d’appliquer une passe d’optimisation.

![Fenêtre ombrée de MeshMill montrant l'échantillon de maillage groupé](../../images/meshmill-shaded.png)

L'affichage Vertices expose la distribution réelle des points. Régions d'analyse denses, zones clairsemées et
des changements brusques d'échantillonnage sont visibles sans changer la géométrie. Le panneau de métriques étendu
suit l'activité du processeur, de la mémoire, du GPU et du traitement de la géométrie tout en travaillant avec le maillage. (CPU)

![Affichage des sommets MeshMill avec des mesures de performances étendues](../../images/meshmill-vertices.png)

L'affichage Wireframe affiche directement la structure triangulaire. Cela aide à identifier la densité inutile,
une triangulation irrégulière et des régions où la simplification peut supprimer une géométrie substantielle.

![Affichage MeshMill Wireframe montrant la variation de la densité des triangles](../../images/meshmill-wireframe.png)

## Analyser la densité du maillage

L’affichage Densité cartographie la densité locale relative dans le modèle. Les régions clairsemées restent fraîches tandis que
les régions de plus en plus denses se déplacent à travers des couleurs plus vives, rendant l'échantillonnage inégal visible d'un seul coup d'œil.

![Affichage de la densité MeshMill montrant la densité relative du maillage](../../images/meshmill-density.png)

La densité reste disponible lors de l'évaluation d'une optimisation provisoire. La boîte à outils rapporte le
algorithme, cible, nombre de triangles et de sommets résultants, pourcentage de réduction, dimensions et
taille de sortie estimée avant l’application de la passe.

![Affichage de la densité MeshMill montrant une optimisation provisoire](../../images/meshmill-density-overview.png)

Maintenez le bouton droit de la souris pour inspecter une région à travers la loupe circulaire. La vue agrandie
reste centré sur le pointeur et révèle la densité locale sans changer la position principale de la caméra.

![Affichage de la densité MeshMill avec la loupe de la fenêtre](../../images/meshmill-density-zoom.png)

## Commandes de visualisation

| Entrée | Action |
| --- | --- |
| Glisser avec le bouton central | Orbite |
| Maj + glisser avec le bouton central | Panoramique |
| Molette de la souris | Zoom vers le pointeur |
| Ctrl + molette de la souris | Rotation horaire ou anti-horaire |
| Touches fléchées | Orbite autour du centre de la vue |
| Ctrl + touches fléchées | Panoramique |
| Ctrl + Maj + Haut/Bas | Zoom |
| Ctrl + Maj + Gauche/Droite | Rouleau |
| `F1` / `F2` / `F3` / `F4` | Ombré / Densité / Filaire / Sommets |
| Maintenir le bouton droit de la souris | Loupe |
| Maj + clic gauche | Ajouter ou supprimer des points de règle |
| Ctrl + glisser vers la gauche | Dessiner un polygone de sélection |
| `Ctrl+C` | Ajouter le polygone à la sélection enregistrée |
| `Ctrl+X` | Recadrer à la sélection |
| `Ctrl+Space` | Optimiser la sélection |
| `Delete` | Supprimer la sélection |
| `Escape` | Effacer la sélection ou la règle active |
| `Ctrl+Z` / `Ctrl+Y` | Annuler/rétablir |
| `Ctrl+S` | Enregistrer l'état actuel du maillage |

Les touches d'affichage standard suivent le bloc de navigation à six touches :

| Clé | Voir | Ctrl + touche |
| --- | --- | --- |
| `Insert` | Gauche | Définir l'orientation actuelle sur Gauche |
| `Home` | Avant | Définir l'orientation actuelle sur Avant |
| `Page Up` | Droite | Définir l'orientation actuelle sur Droite |
| `Delete` | Haut lorsqu'aucune sélection n'existe | Définir l'orientation actuelle sur Haut |
| `End` | Retour | Définir l'orientation actuelle sur Retour |
| `Page Down` | Bas | Définir l'orientation actuelle sur Bas |

L'enregistrement d'une vue met également à jour sa vue opposée. Gauche et droite, avant et arrière, haut et bas
restent jumelés. Dans la boîte de dialogue de confirmation, **Enregistrer** est l'action par défaut, donc Entrée enregistre le
orientation. Front apparaît en haut des vues Top et Bottom.

Les raccourcis peuvent être modifiés ou réinitialisés dans Paramètres.

## Flux de travail de sélection

Maintenez Ctrl et faites glisser vers la gauche pour dessiner un polygone. Faites glisser les coins pour le remodeler, cliquez avec le bouton gauche sur un bord pour ajouter un
ou cliquez avec le bouton droit sur une arête pour en supprimer une. Ajoutez plus de régions avec `Ctrl+C`. Déplacer la caméra cache
le polygone de l'espace écran tout en conservant la géométrie sélectionnée.

L'optimisation avec une sélection active affecte uniquement cette sélection. Le résultat reste provisoire
jusqu'à ce que **Appliquer** soit sélectionné. **Annuler** annule le résultat provisoire et conserve la sélection afin
une autre configuration peut être essayée. Les opérations de recadrage et de suppression deviennent des modifications de maillage normales et annulables.

Le panneau de sélection indique les sommets sélectionnés cumulés, les triangles, la part de maillage, les valeurs estimées.
taille et dimensions. Ses actions recadrent, ajoutent, optimisent, suppriment, reculent ou effacent les éléments conservés.
sélection sans masquer la géométrie environnante.

![MeshMill montrant une sélection régionale conservée et ses statistiques géométriques](../../images/meshmill-crop-selection.png)

## Grandes mailles

Avant d'allouer un binaire STL, MeshMill compare sa mémoire de travail estimée avec la mémoire configurée.
budget mémoire. Un fichier situé au-dessus du budget s'ouvre sous la forme d'un aperçu limité en lecture seule. Les rapports de synthèse
le nombre complet de triangles sources mais désactive l'édition et l'exportation car il s'agit d'un échantillon et non de la totalité
objet. Un traitement out-of-core indexé et dépendant du zoom est prévu dans
[docs/OUT_OF_CORE.md](docs/OUT_OF_CORE.md).

## Ligne de commande

`MeshMillCLI.exe` est inclus dans les deux packages de version :

```powershell
.\MeshMillCLI.exe "C:\path\mesh.stl" --preset balanced
.\MeshMillCLI.exe "C:\path\mesh.stl" --target 150000 --output "C:\path\mesh-reduced.stl"
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm density --target 150000
.\MeshMillCLI.exe "C:\path\mesh.stl" --algorithm topology --overwrite
```

Exécutez `.\MeshMillCLI.exe --help` pour toutes les options. MeshMill refuse d'écraser son fichier d'entrée.

## Exemple de géométrie

Deux versions de l’exemple de développement sont disponibles. L'échantillon est un maillage composite avec
couches intentionnelles de géométrie redondante et de densité variée. Il donne aux personnes sans scanner un
dispositif réaliste pour comparer les algorithmes, inspecter la densité, exercer des opérations régionales,
et développer des fonctionnalités de feuille de route. MeshMill ne nécessite pas de saisie numérisée.

| Fichier | Triangles | Taille | Livraison | Idéal pour |
| --- | ---: | ---: | --- | --- |
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249 999 | 11,9 Mo | Git normal | Évaluation rapide, CI et apprentissage des contrôles | (249,999)
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4 126 315 | 196,8 Mo | Git LFS | Test de la géométrie source dense et des performances des grands maillages | (4,126,315)

Le plus petit échantillon est téléchargé avec chaque clone normal. L'original intact est facultatif et
géré via Git LFS afin de ne pas gonfler l'historique du référentiel ordinaire. Le bureau GitHub comprend
Git LFS. Les utilisateurs de ligne de commande peuvent installer Git LFS et exécuter :

```powershell
git lfs pull --include="samples/original-scan.stl"
```

Les versions marquées publient également le STL original en téléchargement direct pour les personnes qui n'utilisent pas Git.
Voir [`samples/README.md`](../../../samples/README.md) pour la provenance, les dimensions et les sommes de contrôle.

Les contributeurs à l'algorithme devraient également lire le
[guide de test d'algorithme] (docs/ALGORITHM_TESTING.md) avant de comparer ou de modifier la réduction
comportement.

## Unités STL

STL ne code pas une unité. La modification des unités du modèle modifie les étiquettes et les mesures sans mise à l'échelle
les coordonnées enregistrées. Sélectionnez l'unité qui décrit la géométrie source.

## Confidentialité

MeshMill lit et écrit des fichiers locaux. Il ne contient aucun compte, télémétrie, téléchargement, publicité ou
fonctionnalité de traitement en nuage. La mise en œuvre actuelle des métriques GPU utilise les performances locales du Windows.
compteurs. Des fournisseurs de métriques natifs équivalents sont prévus pour Linux et macOS.

Pour le dépannage diagnostique, les développeurs peuvent démarrer l'interface graphique avec
`--diagnostic-log <local-file.jsonl>`. Le journal enregistre localement le routage des entrées et l'état de la caméra et est
désactivé pendant une utilisation normale.

## Développement et sortie

Le texte et la documentation localisés de l'interface utilisateur sont initialement produits avec une traduction automatique externe
services et vérifié automatiquement pour les dommages structurels. La traduction automatique peut encore être
contre nature ou incorrect. Les locuteurs natifs sont encouragés à réviser et à corriger les traductions via
le processus de contribution.

- [Contribuer](CONTRIBUTING.md)
- [Processus de publication](RELEASING.md)
- [Feuille de route](ROADMAP.md)
- [Dépannage](docs/TROUBLESHOOTING.md)
- [Avis de tiers](THIRD_PARTY_NOTICES.md)

## Prise en charge MeshMill

MeshMill est développé et maintenu indépendamment. Lire
[pourquoi soutenir ce travail est important](SUPPORT.md), ou soutenir le développement continu via
[Achetez-moi un café] (https://buymeacoffee.com/tednv).

MeshMill est sous licence GNU General Public License, version 3 ou ultérieure. Voir
[`LICENSE`](../../../LICENSE).
