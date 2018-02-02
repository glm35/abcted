#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sequencer demo with the "Sporting Nell" tune
"""

# PSL imports
import time

# Third-party imports
from pyfluidsynth3 import fluidevent, fluidsequencer

# abcde imports
import abcde.abc2midi as abc2midi
import abcde.abcparser as abcparser
import abcde.musictheory as musictheory
import abcde.snap as snap


sporting_nell = \
"""
T:Sporting Nell
D:Mick O'Brien: May Morning Dew (1996)
R:reel
M:2/2
K:Dmix
|: ADED A2dc | ABAG EFG2 | ADED A2dc |1 AcGE EDEG :|2 AcGE EDD2 | 
K:Amix
  cdec d2ed | cdef gedB | cdec dfed | cAGE EDD2 |
  cdec dfed | cdef g2gd | eaag efd=c | ABAG EFG2 ||
"""


def demo_play_sporting_nell(bpm=90, instrument='Acoustic Grand Piano'):
    player = snap.SingleNoteAbcPlayer()
    player.setup_synth()
    player.select_instrument(instrument)

    # Setup sequencer over existing player
    sequencer = fluidsequencer.FluidSequencer(player._handle)
    sequencer.beats_per_minute = bpm
    beat_length = sequencer.ticks_per_beat
    print("BPM: {0}".format(sequencer.beats_per_minute))
    print("TPB: {0}".format(sequencer.ticks_per_beat))
    print("TPS: {0}".format(sequencer.ticks_per_second))

    dest = sequencer.add_synth(player._synth)
    ticks = sequencer.ticks + 10

    abc_key = 'Dmix'
    half_bar1 = 'ADED'

    bar1 = 'ADED A2dc'
    bar2 = 'ABAG EFG2'

    for simple_note in half_bar1:
        norm_key = abcparser.normalize_abc_key(abc_key)
        alteration = musictheory.get_note_alteration_in_key(simple_note, norm_key)
        abc_note = alteration + simple_note
        midi_note = abc2midi.get_midi_note(abc_note)

        event = fluidevent.FluidEvent(player._handle)
        event.dest = dest[0]
        event.note(0, midi_note, 127, int(beat_length * 0.25))

        sequencer.send(event, ticks)
        ticks += int(beat_length / 4)

    time.sleep(4)


if __name__ == "__main__":
    demo_play_sporting_nell()
