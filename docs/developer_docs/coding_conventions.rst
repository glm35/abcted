Style et conventions de codage
==============================

Style de codage
---------------

docstrings
~~~~~~~~~~

* la documentation Python (dosctrings) est écrite dans le style Google. Exemple ici:
  http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html


Conventions de codage
---------------------

Données brutes et données normalisées
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le texte supposé au format ABC récupéré dans la zone d'édition est considéré
comme du texte brut. Après analyse par le parser ABC, sa syntaxe est validée
et il prend une forme dite normalisée.

Dans le code:

* les données brutes sont préfixées par ``raw_``. Par exemple: ``raw_note``
  et ``raw_key``.

* les données normalisées sont préfixées par ``abc_``. Par exemple: ``abc_note_``
  et ``abc_key``.

Nommage des variables stockant des noms de fichiers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On s'appuie sur la terminologie normalisée à l'ISO pour C++17
(https://en.cppreference.com/w/cpp/filesystem/path#Decomposition):

* path: nom de répertoire + nom de fichier

* filename: uniquement le nom de fichier

Cf. discussion sur stackoverflow:
https://stackoverflow.com/questions/2235173/file-name-path-name-base-name-naming-standard-for-pieces-of-a-path

Dans le code abcted, tous les noms de fichiers sont absolus et normalisés.
Les noms de variables stockant des chemins venant de l'extérieur du programme
avant normalisation sont préfixés par ``raw_``.

Variables globales et constantes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Les constantes sont en majuscules: eg CONFIG_FILE_NAME.

* Les variables globales non constantes sont en minuscules: eg args

Nom de fichier vs chemin vers un fichier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Les noms de fichiers ou répertoires sous forme de chaîne de caractères
  terminent par name: eg config_file_name, config_dir_name.

* Les chemins de fichiers ou répertoires (pathlib.Path) terminent par path,
  eg: config_file_path, config_dir_path.

Nommage des gestionnaires d'évènements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Quand une fonction est appellée suite à un évènement et qu'elle prend en
paramètre un évènement, on préfixe son nom avec ``_on``.  Par exemple:
``PlayerDeck._on_toggle_play_pause()``.  Quand la fonction est une commande
appelée directement, par exemple depuis un menu, on ne préfixe pas.  Par
exemple: ``PlayerDeck._play()``.
