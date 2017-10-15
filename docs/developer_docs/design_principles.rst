Principes de conceptions d'abcde
================================

Principe de conception
----------------------

En français
~~~~~~~~~~~

La langue maternelle d'abcde est le français:

* l'interface utilisateur est en français;

* la documentation pour les utilisateurs et les développeurs est en français.

Le code et les commentaires dans le code sont écrits en anglais.

A terme, si le logiciel a atteint un niveau de maturité suffisamment
important pour envisger une publication/diffusion internationale, il
sera internationalisé, avec dans un premier temps une traduction de l'IHM
et de la documentation en anglais.

Développement incrémental
~~~~~~~~~~~~~~~~~~~~~~~~~

L'objectif est d'avoir un logiciel utilisable, pas parfait: les fonctions les plus
utiles sont développées en priorité, et on finalise dans un second temps.

Maintenabilité
~~~~~~~~~~~~~~

Je n'ai pas beaucoup de temps disponible pour développer abcde. La maintenabilité et
la lisibilité du code sur le long terme sont donc très importantes. Cela guide certains
choix de conception et de principes de développement:

* garder une base de code propre et bien documentée

* utiliser uniquement la librairie standard Python, sauf quand il n'est pas possible
  de faire autrement

Portabilité
~~~~~~~~~~~

Le développement se fait sous Linux. La possibilité de faire tourner le logiciel sous
Windows est prise en compte dans les choix techniques.

Développement décentralisé
~~~~~~~~~~~~~~~~~~~~~~~~~~

Afin de pouvoir développer depuis plusieurs postes de travail et avec ou sans accès
réseau, tout le développement est décentralisé. Dans un premier temps, cela se
traduit par "tout sous git": le code, les docs, et les bugs.

S'amuser
~~~~~~~~

Le développement d'abcde est un loisir, il doit conserver une dimension ludique.

Choix techniques
----------------

* Python3, dans la version disponible sur les distributions Ubuntu LTS et Linux Mint.
  A chaque nouvelle version LTS, on s'autorise à utiliser les nouvelles fonctions
  disponibles dans le langage Python et sa librairie standard: compromis entre le fait
  de s'amuser et d'avoir un logiciel portable.
