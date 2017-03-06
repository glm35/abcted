Faire passer les tests automatiques
===================================

Objectifs
---------

* les tests doivent passer sur le code dans ``abcde/`` pas dans un code installé
  quelque part sur le système de fichier

* pouvoir exécuter les tests avec ``make test`` qui fait
  ``python -m unittest discover`` depuis la racine

* pouvoir exécuter les tests depuis pycharm


Passer les tests en CLI
-----------------------

Pour pouvoir dérouler les tests en CLI, il faut ajouter la racine des sources
à la variable d'environnement ``PYTHONPATH``::

  $ export PYTHONPATH=$PYTHONPATH:/path/to/abcde/abcde

Pour automatiser la configuration du ``PYTHONPATH`` lors de l'appel à  ``make test``
je ne vois pas d'autre moyen que de passer par un script intermédiaire: je ne
vois pas comment on peut exporter ``PYTHONPATH`` depuis le Makefile. D'où
``runtests.py``.


Passer les tests avec PyCharm
-----------------------------

Pour pouvoir dérouler les tests avec PyCharm, il faut faire la même chose.

Méthode 1 (générique): il suffit de marquer le répertoire ``abcde/abcde`` comme
contenant des sources (*clic droit -> Mark Directory As... -> Source Root*).
Comme dans la section Environments, la case à cocher
*Add source roots to PYTHONPATH* est cochée par défaut, cette config simple
s'applique à tous les cas.

Méthode 2 (à refaire pour chaque configuration): 

* éditer la configuration

* dans la section Environment variables: créer la variable PYTHONPATH avec le
  chemin qui va bien

(testé avec PyCharm Community Edition 2016.3.2)
