=======================================
Notes sur l'utilisation de pyfluidsynt3
=======================================

Références
==========

http://fluidsynth.sourceforge.net/api/index.html#Sequencer

Stopper une séquence
====================

Une technique qui semble fonctionner: détruire le séquenceur.  La dernière
note jouer raisonne assez longtemps, on peut l'arrêter avant::

    sequencer = fluidsequencer.FluidSequencer(player._handle)
    ...
    for ...
        sequencer.send(...)

    player._synth.noteoff(player._midi_channel, midi_note)
    del sequencer


Qu'est-ce qui se passe quand on envoie un évènement dans le passé?
==================================================================

L'évènement s'applique immédiatement.


time, timestamps, date et ticks
===============================

time, timestamps, date et ticks: c'est kiff-kiff.

Quand on programme un évènement à venir dans un séquenceur, la date de
l'évènement s'exprime en **ticks**.  C'est le cas avec la fonction
fluid_sequencer_send_at() de fluidsynth (paramètre ``time``), c'est aussi
le cas avec la fonction FluidSequencer.send() de pyfluidsynth3 (paramètre
``timestamp``).  C'est encore le cas avec la fonction ``sendnoteon()`` de
l'exemple donné dans http://fluidsynth.sourceforge.net/api/index.html#Sequencer
(paramètre ``date``).


Relation entre ticks et tempo
=============================

Par défaut, l'échelle de temps des ticks est la suivante: 1000 ticks/s, soit
durée(tick) = 1ms.  C'est le paramètre "ticks per second", ou tps.

Par ailleurs

* bpm = beat per minute, c'est le tempo du métronome.

* tpb = ticks per beat, c'est la conséquence du tps et du bpm.

On a::

  beat_len = 60 / bpm

et::

  tpb = tps * beat_len

soit::

  tpb = 60 * tps / bpm


Exemple: pour un tempo de 120 battements par minute (120 bpm) et l'échelle
de temps par défaut (tps = 1000 ticks par seconde), un battement dure
500 ticks.


Interaction bas-niveau avec fluidsynth
======================================

Un objet FluidHandle permet d'appeler toutes les fonctions de la librairie
C fluidsynth: cf fluidhandle.py

Pour enregistrer à l'aide de la fonction fluid_sequencer_register_client()
une fonction Python comme callback qui sera appelé par
la librairie C fluidsynth: voir
https://docs.python.org/3/library/ctypes.html#callback-functions
(exemple dans tests/demo_music_box.py)
