# MeshMill

![Vue ombrée MeshMill](../../images/meshmill-shaded.png)

MeshMill est une application de bureau spécialisée conçue pour rendre gérables les géométries de maillage
volumineuses, denses ou complexes. Elle permet une inspection rapide, l'analyse de la densité, la sélection par zone, le découpage, la suppression,
ainsi qu'une réduction contrôlée du maillage, sans nécessiter de compte ni de téléchargement de la géométrie vers un serveur.

Le rendu OpenGL accéléré par le GPU assure une navigation fluide dans la vue, la sélection matérielle, la visualisation de la densité et l’inspection interactive. La réduction du maillage s’exécute actuellement dans des processus CPU natifs distincts afin que les longs calculs géométriques ne bloquent pas l’interface.

MeshMill prend en charge les maillages issus de scanners 3D, d'exports CAO et de modélisation, de chaînes de reconstruction,
de géométries générées et d'autres sources STL. Elle prépare la géométrie pour des logiciels d'édition en aval,
des outils de fabrication et d'autres flux de travail liés aux maillages. La modélisation généraliste, la sculpture, l'animation,
la gestion des matériaux et la création de scènes sortent de son champ d'application.

## Téléchargement

Téléchargez l'un de ces fichiers depuis la section [Releases de GitHub](../../releases) :

- `MeshMill-<version>-windows-x64-setup.exe` : installateur par utilisateur avec intégration au menu Démarrer et création optionnelle
  de raccourcis sur le bureau.
- `MeshMill-<version>-windows-x64-portable.zip` : application portable. Extrayez l'intégralité de l'archive,
  puis lancez `MeshMill.exe`.

Les deux packages incluent l'environnement d'exécution de l'application. Les utilisateurs finaux n'installent pas les dépendances Python, Node.js ou
La version initiale prend en charge Windows 10 et Windows 11 sur du matériel x64. Des packages Linux et
macOS sont prévus ; les formats de produit et de fichier ne sont pas spécifiques à Windows.

Les builds communautaires non signés peuvent déclencher un avertissement SmartScreen lié à Windows. Les sommes de contrôle des versions sont indiquées
dans `SHA256SUMS.txt`, à côté de chaque version.

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

![Affichage de la densité du maillage](../../images/meshmill-density.png) (MeshMill)

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
| [`sample-scan.stl`](../../../samples/sample-scan.stl) | 249 999 | 11,9 Mo | Git normal | Évaluation rapide, CI et apprentissage des contrôles |
| [`original-scan.stl`](../../../samples/original-scan.stl) | 4 126 315 | 196,8 Mo | Git LFS | Test de la géométrie source dense et des performances des grands maillages |

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
