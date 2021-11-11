===================
Gestion de fichiers
===================

Fichiers récents et fichiers favoris
====================================

Fichiers récents
~~~~~~~~~~~~~~~~

abcted garde en mémoire les 10 fichiers les plus récemment utilisés et les
présente dans le menu Fichier:

  * un fichier est ajouté automatiquement à la liste et placé en première
    position dès qu'il est créé ou ouvert;

  * le plus ancien fichier récent est retiré automatiquement de la liste quand
    la liste est pleine;

  * un fichier récent est retiré automatiquement de la liste si on essaie de
    l'ouvrir et s'il n'existe plus à l'emplacement attendu.

.. note:: la liste des fichiers récents est conservée dans le fichier texte
   codé en UTF-8 ``~/.config/abcted/recent_files.txt``.  Ce fichier peut être
   édité manuellement quand abcted est fermé.

Fichiers favoris
~~~~~~~~~~~~~~~~

abcted permet de marquer des fichiers récents comme favoris à l'aide du menu
Fichier => Ajouter aux favoris.  Un fichier favori apparaît dans le menu
des fichiers récents précédé d'une étoile.  Un fichier favori n'est jamais
supprimé automatiquement de la liste des fichiers récents.  On peut supprimer
un fichier de la liste des favoris à l'aide du menu
Fichier => Retirer des favoris.

.. note:: la liste des fichiers favoris est conservée dans le fichier texte
   codé en UTF-8 ``~/.config/abcted/favorite_files.txt``.  Ce fichier peut être
   édité manuellement quand abcted est fermé.
