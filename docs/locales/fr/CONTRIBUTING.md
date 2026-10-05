# Contribuer

Les contributions sont les bienvenues via des tickets et des pull request.

## Portée du projet

MeshMill permet de gérer les fichiers de maillage surdimensionnés, denses ou difficiles pour l'édition en aval et
flux de production. Les contributions devraient améliorer l'inspection de la géométrie, la densité du maillage et des points
gestion, optimisation, sélection, recadrage, nettoyage, validation, échange STL, performance,
ou la coordination de ces opérations.

Le projet n'inclut pas la modélisation, la sculpture, la peinture, l'animation, le rendu,
composition de scènes, matériaux, gréements ou autres systèmes de création de contenu. Des propositions qui introduisent
ces fonctionnalités sortent de la portée du projet.

Les nouvelles fonctionnalités doivent garder l'application concentrée et préserver les flux de travail directs qui deviennent source
la géométrie en maillages gérables et évitez de transformer les contrôles de support en une édition générale
environnement.

## Localisation

Le texte source de l'interface utilisateur en anglais est stocké dans `locales/en-US.json`. Les métadonnées locales sont stockées dans
`locales/manifest.json`. Les catalogues d'interface utilisateur traduits utilisent les mêmes clés stables et le même nom de fichier
`<locale>.json`. La documentation traduite utilise le nom de fichier racine correspondant sous
`docs/locales/<locale>/`.

Les traductions sont initialement réalisées avec des services de traduction automatique externes et reçoivent
validation structurelle automatisée. Ce procédé ne peut garantir un naturel, une précision technique ou
langage contextuellement correct. Les locuteurs natifs sont encouragés à réviser et à corriger l'interface utilisateur traduite.
texte et documentation. Les corrections de traduction doivent conserver les clés du catalogue, les espaces réservés,
commandes, liens, mesures, noms de produits et structure Markdown.

Après avoir modifié les étiquettes, les info-bulles, les boîtes de dialogue ou tout autre texte visible par l'utilisateur, exécutez :

```powershell
python tools/localization/extract_ui_catalog.py
python tools/localization/validate_locales.py
```

Examinez ensemble les modifications apportées à la source et les clés régénérées.

## Modifications de la géométrie et de l'algorithme

Utilisez la géométrie de l'échantillon groupé lors de la modification de l'optimisation, de l'analyse de densité, de la sélection, du recadrage,
gestion des fichiers volumineux ou comportement de comparaison des fenêtres d'affichage. Il contient intentionnellement des couches redondantes
et une densité inégale, donc un résultat utile devrait améliorer la maniabilité sans cacher la distorsion,
en supprimant les limites significatives ou en supprimant silencieusement la géométrie qu'un autre algorithme préserve.

Enregistrez l'entrée, l'algorithme, les paramètres, le nombre de triangles, les dimensions, la dérive dimensionnelle, le temps écoulé,
et des captures d'écran pertinentes pour les comparaisons. Testez à la fois le plus petit appareil normal-Git et, lorsque le
le changement concerne la géométrie grande ou en couches, le luminaire original Git LFS. Ne réglez pas un algorithme
à ce seul luminaire. Ajoutez de petits cas synthétiques pour l'invariant ou la régression spécifique en cours
testé.

Voir [Test d'algorithme et contribution](docs/ALGORITHM_TESTING.md) pour la liste de contrôle de comparaison.

## Configuration du développement

1. Installez Python 3.12 64 bits sur Windows.
2. Créez et activez un environnement virtuel.
3. Installez `requirements-dev.txt`.
4. Exécutez `python meshmill.py` pour l’interface graphique ou `python meshmill.py --help` pour l’utilisation de la CLI.
5. Exécutez `python -m py_compile meshmill.py` avant de soumettre une modification.

Conservez les maillages privés, les exécutables générés, les captures d'écran contenant des informations privées et les
créer des répertoires à partir de commits. La géométrie de test redistribuable appartient sous `samples/` avec son
source, licence, dimensions et méthode de génération documentées. Les nouveaux fichiers sources doivent utiliser le
Identifiant SPDX `GPL-3.0-or-later`.

Recadrez chaque capture d'écran de la documentation selon le contenu de l'application MeshMill. N'incluez pas le
barre des tâches, chrome de fenêtre sans rapport, notifications, détails du compte, chemins privés ou arrière-plan
contenu du bureau.
