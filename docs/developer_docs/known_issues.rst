Problèmes connus
================

Retour musical
--------------

Retour musical non souhaité dans les champs informatifs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Quand on tape une lettre correspondant à une note dans l'édition du nom d'un
champ informatif de l'entête, ie entre le X: et le K:, elle est jouée.
Typiquement: C quand on veut faire C:

Retour musical désactivé quand on change d'application avec Alt+TAB
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Quand on bascule de abcde vers une autre application avec Alt+TAB et qu'on revient
dans abcde, il n'y a plus de feedback musical lors de l'édition.

La raison: l'évènement keypress sur Alt_L est pris en compte par abcde, mais pas
l'évènement keyrelease qui a lieu dans l'autre application. Quand abcde croit qu'une
touche control ou alt est appuyée, la fonction play_midi_note() n'est pas appelée.

Workaround: de retour dans abcde, appuyer puis relâcher Alt_L

Piste de correction: quand le focus revient sur l'application, vérifier l'état des touches
control et alt.
