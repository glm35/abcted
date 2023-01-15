====================
Jouer un morceau ABC
====================

abcted permet de jouer un morceau ABC afin de contrôler la saisie, de se
remettre en tête une mélodie ou de permettre la pratique instrumentale avec un
playback.

Un aide-mémoire des raccourcis clavier permettant de contrôle le playback est
donné ici: :ref:`playback-shortcuts`.


Play, pause, stop
=================

+------------------------+-------------------------------------------+
| Raccourcis             | Commande                                  |
+========================+===========================================+
| Ctrl+j (ou Ctrl+J)     | Ouvrir la boîte de playback du morceau    |
|                        | courant (le morceau dans lequel est le    |
|                        | curseur)                                  |
+------------------------+-------------------------------------------+
| SPC                    | Démarre le playback ou bascule l'état du  |
|                        | playback entre play et pause              |
+------------------------+-------------------------------------------+
| ESC                    |Si le playback est en cours (play ou       |
|                        |pause), arrête le playback.  Sinon, ferme  |
|                        |la fenêtre de playback.                    |
+------------------------+-------------------------------------------+


Jouer en boucle
===============

On peut choisir de boucler indéfiniment le playback, ou bien définir le nombre
de répétitions.

+------------------------+-------------------------------------------+
| Raccourcis             | Commande                                  |
+========================+===========================================+
| l                      |Bascule entre les différents modes de      |
|                        |bouclage (pas de bouclage, bouclage infini,|
|                        |définir le nombre de répétitions)          |
+------------------------+-------------------------------------------+


Tempo
=====

Un morceau est joué au tempo donné par le champ informatif "tempo" (Q).

Si ce champ n'est pas défini, un tempo par défaut est utilisé.  Il dépend du
type de morceau défini par le champ informatif "rythme" (R) et correspond au
:ref:`pre-defined-tempo` "medium".

Remarque: si ni le champ "tempo" ni le champ "rythme" ne sont définis, ou si le
champ "rythme" contient une valeur non reconnue, on utilise une pulsation par
défaut de 120 noires à la minutes (tempo "medium" de la ligne "autre" du tableau
des valeurs prédéfinies).



Modifier le tempo
-----------------

On peut modifier le tempo en saisissant une nouvelle valeur ou en
augmentant/diminuant la valeur courante avec les touches ``+`` et ``-``.  Le
tempo peut prendre une valeur entre 1 et 999 battements par minute (bpm).

+------------------------+-------------------------------------------+
| Raccourcis             | Commande                                  |
+========================+===========================================+
| b                      |Focalise sur le widget de saisie du tempo  |
|                        |en bpm                                     |
+------------------------+-------------------------------------------+
| +, -                   |Accélère ou ralenti le tempo de 2 bpm      |
+------------------------+-------------------------------------------+
| =                      |Restaure le tempo à sa valeur d'origine    |
+------------------------+-------------------------------------------+


.. _pre-defined-tempo:

Tempo prédéfini
---------------

abcted propose des tempos prédéfinis pour quelques rythmes de morceau et permet
de les appliquer rapidement:

============= ============= ============= =============
Rythme        Tempo lent    Tempo medium  Tempo rapide
============= ============= ============= =============
Reel          60            90            116
Jig           90            110           130
Hornpipe      50            70            82
Slide         100           140           150
Polka         110           140           156
Valse         108           146           165
Mazurka       120           150           160
Fling         60            80            106
autre         100           120           140
============= ============= ============= =============

Le tempo lent permet de s'échauffer ou de travailler à vitesse réduite.

Le tempo rapide correspond à un tempo de ceili.

Pour appliquer un tempo prédéfini, appuyer sur l'un des trois boutons ad-hoc ou
utiliser un raccourci clavier:

+------------------------+-------------------------------------------+
| Raccourcis             | Commande                                  |
+========================+===========================================+
| s                      |Applique le tempo lent prédéfini (slow)    |
+------------------------+-------------------------------------------+
| m                      |Applique le tempo intermédiaire prédéfini  |
|                        |(medium, modéré)                           |
+------------------------+-------------------------------------------+
| f                      |Applique le tempo rapide prédéfini         |
|                        |(fast, tempo de ceili)                     |
+------------------------+-------------------------------------------+
