#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# PSL imports
import time

# Third-party imports
from getch import getch

# abcde imports
import abcde.musictheory as musictheory
import abcde.player as snap


def demo_play_interactive(instrument='Acoustic Grand Piano'):
    player = snap.Synth()
    player.setup_synth()
    player.select_instrument(instrument)
    print('Press a key for an ABC note from C to b... (Ctrl+C or q or Q to finish)')
    two_octaves_c_major_scale = musictheory.C_MAJOR_SCALE + list(map(str.lower, musictheory.C_MAJOR_SCALE))
    while True:
        key = getch()
        if key in ['\x03', 'q', 'Q']:  # '\x03' = Ctrl+C
            break
        if key in two_octaves_c_major_scale:
            player.play_abc_note(key)


def demo_play_tick():
    # !!! use 9 for channel 10 (perc)
    # Valeurs de 'note' qui pourraient le faire pour un tick métronome:
    # 37: stick
    # 42: Closed Hi-hat
    # 56: Cowbell
    # ~ 60-62
    # ~ 75-77
    player = snap.Synth()
    player.setup_synth()
    player.select_midi_channel(9)
    for note in range(35, 82):
        print("playing note {} on channel 10 (perc)".format(note))
        player.play_midi_note(note)
        time.sleep(0.5)

if __name__ == "__main__":
    # Choose your demo:

    demo_play_interactive()
    # demo_play_interactive('Accordion')
    # demo_play_tick()
