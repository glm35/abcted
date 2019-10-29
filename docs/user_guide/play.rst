====================
Jouer un morceau ABC
====================

``Ctrl + j`` ou le menu "Jouer => Play" permet de jouer le morceau courant
ou la sélection courante.

Quand un playback est en cours, ``ESC`` ou le menu "Jouer => Stop" permet
d'arrêter le playback.

L'option accessible par le menu "Jouer => Jouer en boucle" permet d'activer
ou de désactiver le fait de jouer en boucle le morceau ou la sélection
courante.  Option désactivée par défaut.

L'option accessible par le menu "Jouer => Donner le tempo" permet d'activer
ou de désactiver le fait de donner le tempo au démarrage du playback.
Option désactivée par défaut.

Le tempo du playback est le tempo indiqué dans champ informatif
ABC "Q:".  Si ce tempo n'est pas défini, abcde utilise par défaut une valeur
qui dépend du type de morceau (champ informatif ABC "R:").  Table des valeurs
par défaut:

============= ================
Type d'air    Tempo par défaut
============= ================
Reel          TBD
Jig           TBD
Hornpipe      TBD
Slide         TBD
Polka         TBD
Valse         TBD
Mazurka       TBD
============= ================

Si ni le champ "Q:" ni le champ "R:" ne sont définis, ou si le champ "R:"
contient une valeur non reconnue par abcde, le tempo du playback est 90.

Le menu "Jouer => Définir le tempo..." ouvre une boîte de dialogue permettant
de définir le tempo à une valeur désirée dans la plage 30-240.  Cette boîte
contient un bouton "Réinitialiser" qui permet de revenir à la valeur déterminée
automatiquement par abcde.

Le menu "Jouer => Augmenter le tempo", ou le raccourci ``Ctrl + PLUS`` permet
d'augmenter le tempo par pas de 2 unités.  Le menu "Jouer => Réduire le tempo",
ou le raccourci ``Ctrl + MOINS`` permet de réduire le tempo par pas de 2 unités.

Un tempo modifié manuellement reste en mémoire jusqu'à ce qu'on joue un autre
morceau ou jusqu'à l'arrêt d'abcde.
