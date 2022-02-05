Problèmes connus
================

Flag "changed" non testé lors de l'ouverture d'un fichier récent
----------------------------------------------------------------

Si le fichier courant est modifié et qu'on ouvre un fichier récent, abcted ne
demande pas si on souhaite enregistrer les modifications.

Retour musical non souhaité dans les champs informatifs
-------------------------------------------------------

Quand on tape une lettre correspondant à une note dans l'édition du nom d'un
champ informatif de l'entête, ie entre le X: et le K:, elle est jouée.
Typiquement: C quand on veut faire C:

Création d'un nouveau fichier ABC depuis la CLI
-----------------------------------------------

Quand depuis la CLI on lance abcted en passant un nom de fichier
qui n'existe pas, on obtient une erreur. Le comportement standard
des éditeurs de texte dans ce cas est de créer un nouveau fichier, et
il me semble désirable de modifier le comportement d'abcted pour aller
dans ce sens (ex: vim, xed).

Il faudra gérer le cas où le chemin n'existe pas non plus: le créer ou remonter
une erreur?

Chemins avec  des \.\. dans la barre de titre
---------------------------------------------

Quand on ouvre un fichier ABC depuis la CLI en mettant \.\. dans le chemin
vers le fichier, ces caractères apparaissent dans la barre de titre malgré
l'utilisation de la méthode ``pathlib.Path.absolute()``.

Solution possible: utiliser à la place la fonction ``pathlib.Path.resolve()``.
Comme cette méthode vérifie que le chemin existe, elle peut générer une
exception style ``FileNotFound`` qu'il faudra traiter ici.

Les messages d'erreur liés à la gestion des fichiers pourraient être plus explicites
------------------------------------------------------------------------------------

* dans file.open(): donner des messages plus clairs pour les causes les plus
  fréquentes de problème: PermissionError, ..

Durée des notes incorrecte lors de la saisie après un playback
--------------------------------------------------------------

Quand on joue un air avec le player midi et qu'on édite le morceau, la durée des
notes est trop courte (hyp: le synth garde en mémoire la durée de la dernière
note jouée par le player midi)
