Conventions de codage
=====================

Données brutes et données normalisées
-------------------------------------

Le texte supposé au format ABC récupéré dans la zone d'édition est considéré
comme du texte brut. Après analyse par le parser ABC, sa syntaxe est validée
et il prend une forme dite normalisée.

Dans le code:

* les données brutes sont préfixées par ``raw_``. Par exemple: ``raw_note``
  et ``raw_key``.

* les données normalisées sont préfixées par ``abc_``. Par exemple: ``abc_note_``
  et ``abc_key``.
