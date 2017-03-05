#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools to convert data from the ABC world to the MIDI world
"""

import musictheory


def get_midi_note(abc_note):
    """"Convert an ABC note to a midi number

    :param abc_note: A normalized ABC note eg 'b', '_E,', '__e', '^c', '^^c'

    :return: the MIDI note number of the ABC note
    """

    alteration = 0
    if abc_note[0] == '^':
        if abc_note[1] == '^':
            alteration = 2
            abc_note = abc_note[2:]
        else:
            alteration = 1
            abc_note = abc_note[1:]
    elif abc_note[0] == '_':
        if abc_note[1] == '_':
            alteration = -2
            abc_note = abc_note[2:]
        else:
            alteration = -1
            abc_note = abc_note[1:]

    midi_c4_number = 60
    midi_note_number = midi_c4_number
    if abc_note.islower():
        midi_note_number += 12
        abc_note = abc_note.upper()
    midi_note_number += musictheory.C_MAJOR_SCALE_INTERVALS[abc_note] + alteration
    return midi_note_number
