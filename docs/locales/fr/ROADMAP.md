# Feuille de route MeshMill

## Prise en charge de la plateforme

Windows est la plate-forme packagée initiale. L'architecture de l'application et les formats de maillage sont
multiplateforme et les versions futures devraient ajouter les packages natifs Linux et macOS. Travail de plateforme
comprend l'empaquetage, l'intégration d'applications, les mesures matérielles, le comportement du système de fichiers et l'automatisation
publier des tests tout en préservant le même projet et les mêmes flux de travail STL sur chaque système pris en charge.

- Validez le package de préversion Linux x86-64 sur les distributions, les environnements de bureau, l'affichage
  serveurs et pilotes GPU avant de le promouvoir en stable.
- Validez les packages de prévisualisation macOS Apple Silicon et x86-64 sur du matériel réel, puis ajoutez Developer
  Signature d'identité et légalisation avant de les promouvoir en stable.
- Ajoutez des fournisseurs de métriques CPU, de mémoire et GPU natifs de plate-forme derrière une interface partagée.
- Conservez les paramètres enregistrés, les mappages de clavier, le comportement de la ligne de commande et les données du projet portables.

Cette feuille de route enregistre les travaux planifiés. Il ne décrit pas les fonctionnalités de la version actuelle.

## Portée

MeshMill gère la géométrie, la densité de maillage, la densité de points, l'optimisation, le nettoyage, la validation et STL
échange afin que les fichiers de maillage volumineux ou lourds restent utiles dans les flux de travail d'édition en aval.

Modélisation générale, sculpture, peinture, animation, rendu, composition de scènes, matériaux,
le truquage et d’autres systèmes de création de contenu sont en dehors de cette feuille de route. La synthèse distribuée s'applique
aux opérations de gestion de maillage de MeshMill et n'étend pas le produit à un éditeur général.

## Géométrie de référence

Le maillage composite groupé est le support de développement commun pour les algorithmes et la feuille de route actuels.
travail. Ses couches intentionnellement redondantes et sa densité inégale permettent des comparaisons reproductibles de
qualité de réduction, analyse de densité, gestion des chevauchements, opérations régionales, traitement hors noyau,
et synthèse future. Les implémentations de la feuille de route devraient rendre compte des résultats par rapport à cet appareil et aux petits
des maillages de régression spécialement conçus, plutôt que d'optimiser le comportement pour un seul modèle.

## Espaces de travail Multi-STL et synthèse statistique

Un espace de travail doit accepter plusieurs entrées STL en tant qu’objets source distincts et visibles indépendamment.
MeshMill doit aligner ces sources, mesurer leur accord géométrique et en synthétiser une utilisable
maillage sans conserver les surfaces internes en double ou la géométrie de chevauchement répétée.

Comportement prévu :

- ajoutez, supprimez, masquez, isolez, réorganisez et inspectez plusieurs sources STL dans un seul espace de travail ;
- conserver l'identité de la source, les unités, les transformations, les limites, la résolution et l'historique des opérations ;
- fournir un enregistrement automatique avec des contrôles d'alignement manuels et une qualité d'ajustement mesurable ;
- partitionner les sources en régions spatiales avant la comparaison afin que les entrées importantes restent limitées ;
- analyser l'occupation, la distance à la surface la plus proche, l'accord normal, la densité locale, la variance et
  nombre d'observations dans des régions qui se chevauchent ;
- classer les surfaces correspondantes, les surfaces en conflit, le bruit de numérisation, les espaces et la géométrie unique ;
- consolider les surfaces statistiquement concordantes en une surface représentative avec des enregistrements
  confiance au lieu d’empiler des triangles en double ;
- supprimer la géométrie fermée, coïncidente et partagée qui n'apporte aucun détail de forme extérieure ;
- conserver la géométrie source qui ne se chevauche pas et exposer les régions ambiguës pour un examen visuel ;
- autoriser une pondération par source et par région lorsqu'une analyse est plus propre ou plus détaillée ;
- valider l'étanchéité, les frontières, les normales, les dimensions et la topologie après synthèse ;
- enregistrer la provenance de la source et les paramètres de synthèse afin que le maillage combiné soit reproductible ;
- prévisualisez le nombre de triangles attendu, les limites, le chevauchement supprimé et la distribution de confiance avant
  valider le résultat synthétisé.

Ce flux de travail doit utiliser le même index spatial hors noyau et le même modèle d'unité de travail prévu pour les grandes
mailles. La comparaison statistique et la consolidation des chevauchements devraient également être distribuées au niveau local.
ou des nœuds MeshMill distants.

## Synthèse distribuée

Un cluster MeshMill doit coordonner plusieurs nœuds fonctionnant en parallèle sur plusieurs
postes de travail. Un nœud peut inspecter, sélectionner, réduire, valider, réparer ou combiner une région attribuée ou
unité de travail. Les contributions restent versionnées indépendamment jusqu'à ce qu'elles soient examinées et incorporées
dans une version objet partagé.

Le système doit prendre en charge :

- contributions simultanées de plusieurs opérateurs et nœuds automatisés ;
- entrées, paramètres, dépendances et sorties déterministes de l'unité de travail ;
- planification tenant compte des capacités basée sur CPU, GPU, la mémoire, les algorithmes et la charge actuelle ;
- partitionnement tenant compte des dépendances des maillages, des régions, des passes de validation et des étapes de synthèse ;
- files d'attente durables avec pause, reprise, annulation, nouvelle tentative, réaffectation et reprise après échec ;
- artefacts adressés par le contenu et contrôles d'intégrité entre les nœuds ;
- synthèse reproductible à partir d'un ensemble enregistré de versions de contributions acceptées ;
- des postes de travail hors ligne ou connectés par intermittence qui peuvent se synchroniser ultérieurement ;
- opération locale d'abord avec un contrôle explicite sur les nœuds participants et les données de projet partagées.

## Collaboration versionnée

Chaque contribution doit enregistrer sa version de l'objet parent, la région ou l'unité de travail sélectionnée, l'opération,
paramètres, identité du nœud, horodatages, dépendances, résultats de validation et somme de contrôle de sortie.

Comportement de collaboration prévu :

- les projets contiennent des objets, des branches, des points de contrôle, des contributions et des versions synthétisées ;
- les contributeurs peuvent travailler à partir de la même version parent sans s'écraser mutuellement ;
- les contributions qui ne se chevauchent pas peuvent fusionner automatiquement après validation ;
- une géométrie superposée ou des dépendances incompatibles créent un conflit explicite ;
- les conflits fournissent une comparaison visuelle, un choix au niveau de la région, un rebasement, une réexécution et une résolution manuelle ;
- les états de révision incluent en attente, accepté, rejeté, remplacé, en conflit et incorporé ;
- le manifeste de synthèse final identifie chaque contribution et dépendance incorporée.

## Interface utilisateur de coordination

L'application de bureau doit gérer le travail distribué sans nécessiter de ligne de commande distincte
ou workflow d'administration du serveur. Les vues planifiées incluent :

- **Projets :** objets, branches, versions, contributeurs et statut de synthèse.
- **Cluster :** postes de travail et nœuds connectés, capacités, état de santé, charge et affectation actuelle.
- **File d'attente :** unités de travail en attente, actives, en pause, bloquées, en échec et terminées.
- **Contributions :** auteur, nœud, version parent, région concernée, paramètres, vérifications et état de révision.
- **Comparez :** vues 3D synchronisées, différences géométriques, métriques et inspection des limites.
- **Conflits :** régions qui se chevauchent, conflits de dépendances, choix de résolution et résultats de validation.
- **Synthèse :** graphique de dépendance, progression globale, versions de contribution sélectionnées et résultat final.
- **Historique :** graphique de branche, points de contrôle, fusions, versions synthétisées et manifestes de reproductibilité.

La fenêtre d'affichage doit afficher la propriété, les régions attribuées, le travail terminé, les modifications en attente, les conflits,
et les différences de version sans altérer le maillage sous-jacent.

## Coordination et transports

La première phase de conception doit définir les limites du protocole avant de sélectionner un transport. Le protocole
doit séparer les métadonnées de coordination des artefacts de grand maillage, prendre en charge le transfert avec reprise et
restent utilisables sur un réseau local sans compte externe ni service hébergé.

Concepts de coordination requis :

- élection d'un coordinateur ou d'un coordinateur explicitement sélectionné ;
- découverte de nœuds et inscription manuelle de nœuds ;
- sessions authentifiées et autorisation à l'échelle du projet ;
- baux et battements de cœur pour la propriété des travaux ;
- soumission du travail idempotent et acceptation des résultats ;
- négociation de version entre différentes versions de MeshMill ;
- événements structurés pour la progression, les journaux, la validation, les échecs et les tentatives ;
- récupération après une interruption du coordinateur, du poste de travail, du réseau ou du nœud.

## Phases de livraison

### Phase 0 : traitement de grands maillages hors cœur

L'index, le streaming, le cache, l'unité de travail et le contrat de sécurité sont documentés dans
[`docs/OUT_OF_CORE.md`](docs/OUT_OF_CORE.md).

- Estimez le nombre de triangles et la mémoire de travail avant d’allouer le maillage complet.
- Ouvrez des fichiers binaires STL surdimensionnés sous forme d'aperçus de navigation limités et uniformément échantillonnés.
- Partitionnez la géométrie pleine résolution en cubes spatiaux avec des limites de chevauchement déterministes.
- Lisez, analysez et optimisez simultanément les cubes indépendants dans les limites de CPU et de mémoire.
- Benchmark des implémentations de calcul GPU pour les étapes de réduction telles que l'évaluation des erreurs, le candidat
  notation, requêtes spatiales et traitement indépendant des unités de travail. Décharger une étape uniquement lorsqu'elle
  fournit une vitesse de bout en bout mesurable ou un avantage en mémoire sans réduire le déterminisme, le maillage
  qualité, garanties de topologie ou compatibilité avec les systèmes dépourvus de GPU adapté.
- Diffusez des niveaux de fenêtre grossiers à fins au lieu de nécessiter le maillage complet en mémoire.
- Dessinez l'état du cube directement dans la fenêtre : en file d'attente, en lecture, en traitement, terminé et échoué.
- Affichez la progression par cube en remplissant chaque cube et conservez une vue globale de l'objet de haut niveau.
- Assemblez les cubes traités avec validation des limites, suppression des doublons et paramètres reproductibles.
- Étendez le planificateur de cube local aux unités de travail de synthèse distribuées dans les phases ultérieures.

### Phase 1 : fondation locale versionnée

- Définissez les formats d’objet, d’opération, de contribution, de branche et de manifeste.
- Ajoutez des espaces de travail multi-STL avec visibilité, transformations, métadonnées et provenance par source.
- Ajoutez des mesures de qualité d’enregistrement et une classification de chevauchement spatial.
- Synthétisez des surfaces statistiquement concordantes tout en supprimant les géométries en double et fermées.
- Ajoutez un examen visuel des conflits, des lacunes, de la confiance et de la géométrie propres à une seule source.
- Conservez l’historique local au fil des sessions d’application.
- Ajoutez des comparaisons visuelles de maillage et de région.
- Rendre les opérations déterministes et reproductibles de manière indépendante.

### Phase 2 : nœuds locaux coordonnés

- Exécutez des nœuds de travail sur un poste de travail.
- Ajoutez la mise en file d'attente, les rapports sur les capacités, l'affectation des tâches et l'annulation.
- Affichez l'état du nœud et de l'unité de travail dans l'interface utilisateur MeshMill.
- Validez localement le partitionnement et l’assemblage des résultats.

### Phase 3 : synthèse multi-postes

- Ajoutez une découverte et une inscription LAN authentifiées.
- Transférez les entrées et les résultats de travail axés sur le contenu avec prise en charge des CV.
- Coordonnez le travail simultané sur plusieurs postes de travail.
- Récupérez les affectations après une panne de nœud ou de réseau.

### Phase 4 : versionnage collaboratif

- Ajoutez des contributeurs, des branches, des états de révision et des autorisations.
- Fusionnez les contributions qui ne se chevauchent pas.
- Détectez et résolvez les conflits de chevauchement ou de dépendance.
- Synthétisez les contributions sélectionnées dans une version objet reproductible.

### Phase 5 : durcissement de la production

- Ajoutez des tests de compatibilité de protocole et une gestion des versions mixtes.
- Ajoutez des tests d’audit, d’intégrité, de corruption, d’interruption et de récupération.
- Comparez les performances de planification, de partitionnement, de transfert, de fusion et de synthèse.
- Déploiement, sauvegarde, migration et récupération de documents après incident.
