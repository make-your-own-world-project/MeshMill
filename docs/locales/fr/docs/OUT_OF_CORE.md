# Architecture maillée hors noyau

La protection actuelle contre les fichiers volumineux du MeshMill estime la mémoire de travail avant d'allouer une mémoire de travail complète.
maille. Les fichiers qui dépassent le budget configuré peuvent s'ouvrir sous forme d'aperçus de navigation limités. Un
L'aperçu est une géométrie échantillonnée, est visiblement identifié comme tel et ne peut pas être modifié ou exporté en tant que tel.
même si c'était la source complète.

Les véritables détails dépendant du zoom nécessitent un index spatial persistant. La conception ci-dessous définit que
prochaine phase de mise en œuvre.

## Format d'index

Chaque maillage source reçoit un répertoire `.meshmill-index` versionné contenant :

- `manifest.json`, avec la taille de la source, l'heure de modification, les hachages du contenu échantillonné, les limites,
  nombre de triangles, version d'index, précision des coordonnées et descriptions de niveaux ;
- tuiles spatiales adressées par niveau octree et code Morton ;
- un maillage d'affichage grossier pour chaque tuile parent occupée ;
- enregistrements triangulaires en pleine résolution dans des tuiles feuilles ; et
- la propriété des limites et les métadonnées de chevauchement utilisées lors des opérations et de l’assemblage régionaux.

La création d'index lit la source séquentiellement dans des blocs délimités. Il écrit des exécutions de tuiles temporaires et
publie atomiquement le manifeste une fois que chaque fichier requis a réussi la validation. Une interruption ou
un index obsolète est détecté à partir de son manifeste et peut être repris ou reconstruit sans ouvrir le fichier complet
maillage en mémoire.

## Diffusion en continu dans la fenêtre

La fenêtre sélectionne les tuiles en utilisant le tronc de la caméra et l'erreur d'espace d'écran. Les tuiles parents grossières sont
montré en premier. Les tuiles enfants visibles les remplacent à mesure que la caméra se rapproche, tandis que hors écran et
les carreaux à faible impact restent grossiers. RAM et VRAM ont des budgets indépendants et sont les moins récemment utilisés
caches. La publication de détails ne libère jamais la représentation grossière de l'objet entier.

Le planificateur enregistre ces états de tuile : en file d'attente, lecture, traitement, téléchargement, résident, échec,
et annulé. La fenêtre d'affichage peut colorer les cubes par état et remplir chaque cube proportionnellement à sa taille.
progrès. L'annulation supprime les résultats partiels et laisse la dernière représentation complète active.

## Traitement et capacité

Une unité de travail locale est une tuile plus le chevauchement déterministe requis par son fonctionnement. Concurrence
est limité au RAM actuellement disponible, au pourcentage de mémoire configuré, au nombre de processeurs logiques et
taille mesurée de l’unité de travail. Le téléchargement et l'affichage de GPU disposent d'un budget VRAM distinct. Parallèle signalé
La capacité est une estimation jusqu'à ce que les carreaux représentatifs aient été mesurés.

Les opérations conservent un propriétaire pour chaque élément de limite. L'assemblage valide les limites partagées,
supprime les doublons, vérifie les décomptes et les limites et enregistre les paramètres exacts utilisés. Le même travail
le format de l'unité et du résultat peut ensuite être planifié sur des nœuds de synthèse distribués.

## Règles de sécurité

- Un échantillon global est étiqueté comme une vue d’ensemble et non comme un détail de fenêtre d’affichage en pleine résolution.
- Un aperçu ne peut pas écraser ou exporter le maillage source complet.
- Les demandes complètes qui dépassent le budget actuel nécessitent un choix explicite.
- La génération d'index, le traitement des tuiles et l'assemblage restent annulables et préservent l'ancien
  état complet.
- Les valeurs de capacité sont des estimations et indiquent si elles décrivent le moteur actuel ou prévu.
  exécution de tuiles parallèles.
