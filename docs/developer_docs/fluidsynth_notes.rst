=======================================
Notes sur l'utilisation de pyfluidsynt3
=======================================

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
