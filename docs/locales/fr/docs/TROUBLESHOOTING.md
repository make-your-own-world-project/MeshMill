# Dépannage

## Windows bloque le téléchargement

Les builds de communauté non signés peuvent déclencher Microsoft Defender SmartScreen. Comparez le téléchargé
le hachage SHA-256 du fichier avec `SHA256SUMS.txt` de la même version GitHub. Les versions signées identifient
leur éditeur dans les propriétés du fichier Windows.

## La version portable ne démarre pas

Extrayez le ZIP complet avant d’exécuter `MeshMill.exe`. Le répertoire `_internal` doit rester ensuite
aux deux exécutables. N'exécutez pas l'exécutable depuis la visionneuse ZIP.

## Un grand STL s'ouvre sous forme d'aperçu

L'ensemble de travail estimé dépasse le budget de mémoire dans Paramètres. Le mode Aperçu est intentionnellement
en lecture seule. Augmentez le budget uniquement lorsque la machine dispose de suffisamment de mémoire disponible, ou réduisez le
maillage avant de l’ouvrir pour l’éditer.

## Une vue standard n'a pas été enregistrée

Appuyez sur le raccourci de la vue modifiée par Ctrl, puis choisissez **Enregistrer** ou appuyez sur Entrée dans la confirmation.
dialogue. L'enregistrement d'une vue met également à jour son opposé. La ligne d'état rapporte la vue enregistrée.

## Les raccourcis de navigation ne répondent pas

Fermez d’abord toute boîte de dialogue modale. Vérifiez ou réinitialisez les raccourcis dans Paramètres s’ils ont été personnalisés. Le
les raccourcis d'affichage par défaut utilisent Insérer, Accueil, Page précédente, Supprimer, Fin et Page suivante.

## Créer un journal de diagnostic d'orientation locale

La journalisation des diagnostics est désactivée par défaut. Pour enregistrer localement le routage du clavier et l’état de la caméra :

```powershell
.\MeshMill.exe --diagnostic-log ".\orientation-session.jsonl" "C:\path\mesh.stl"
```

Le journal peut contenir le chemin du fichier ouvert. Révisez-le et rédigez-le avant de le partager. La géométrie du maillage n'est pas
écrit dans le journal.

## Signaler un problème

Inclut la version MeshMill, la version Windows, le modèle GPU, le nombre de triangles de maillage, l'action exacte
séquence et si le programme d'installation ou le package portable a été utilisé. Utiliser l'échantillon redistribuable
maille lorsque cela est possible. Ne joignez pas d’analyses privées ou de journaux de diagnostic sans les examiner au préalable.
