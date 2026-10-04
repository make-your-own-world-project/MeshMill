# Tests d'algorithmes et contribution

Les algorithmes MeshMill devraient rendre les géométries difficiles gérables tout en gardant leurs effets visibles,
mesurable et réversible avant qu’un résultat ne soit appliqué.

## Luminaires de référence

Utilisez les deux versions groupées de la géométrie de l'échantillon composite :

- `samples/sample-scan.stl` est le plus petit appareil Git normal pour le développement de routine, automatisé
  vérifications et apprentissage des contrôles.
- `samples/original-scan.stl` est le luminaire complet Git LFS pour le comportement des fichiers volumineux, les couches redondantes,
  densité inégale, chevauchement et travail de performance.

Les régions redondantes et denses sont des caractéristiques de test intentionnelles. Un test peut les cibler, mais
Il ne faut pas supposer que toutes les surfaces qui se chevauchent sont jetables. Ajoutez des mailles synthétiques compactes lorsqu'un
le changement nécessite une limite, une courbure, une topologie, une densité ou un invariant de chevauchement connus.

## Liste de contrôle de comparaison

Pour un changement d’algorithme ou de paramètre, enregistrez :

- Version MeshMill ou validation ;
- dispositif d'entrée et somme de contrôle ;
- algorithme, préréglage de qualité, cible et paramètres avancés ;
- nombre de triangles et de sommets originaux et résultants ;
- pourcentage de réduction, dimensions et dérive dimensionnelle ;
- temps écoulé et mémoire maximale lorsque les performances sont pertinentes ;
- des captures d'écran des mêmes vues et modes d'affichage enregistrés ;
- changements visibles de limite, de trou, d'auto-intersection, de chevauchement ou de distorsion ;
- si le résultat provient d'une opération de maillage entier ou de sélection uniquement.

Comparez avec le comportement actuel de la même cible, pas seulement avec un autre préréglage avec un
nombre de sorties différent. Inspectez les affichages ombrés, de densité, filaires et de sommets, le cas échéant.

## Conseils d'acceptation

Un changement d'optimisation doit éviter les changements de dimensions inattendus, les inversions de surface évidentes,
fissures entre les régions traitées, perte de frontières significatives et régressions de grande qualité à un moment donné.
nombre de sorties similaire. Les changements axés sur la densité devraient démontrer que la concentration supprimée a fait
ne portent pas de courbure ou de topologie utile.

Les résultats de performances doivent identifier le processeur, la capacité de mémoire, le matériel graphique, le fonctionnement
système, la taille d’entrée et si les données étaient déjà mises en cache. Validation structurelle et captures d'écran
prennent en charge la révision mais ne remplacent pas l’inspection par des contributeurs familiers avec la géométrie source.

## Tests de régression

Préférez les tests déterministes avec des tolérances explicites. Gardez les nouveaux appareils suffisamment petits pour un Git normal,
documentez leur origine et leur licence, et utilisez la géométrie synthétique lorsque les données sources réelles ne sont pas nécessaires.
Les tests doivent couvrir l'annulation et la restauration de l'état lorsqu'une opération peut modifier la géométrie.
