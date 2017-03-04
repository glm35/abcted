#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools to convert data from the ABC world to the MIDI world
"""

import musictheory


def get_midi_note(abc_note):
    """"Convert an ABC note to a midi number

    :param abc_note: A text string representing an normalized ABC note
                     eg 'b' or '_C,'

    :return: the MIDI note number of the ABC note
    """

    alteration = 0
    if abc_note[0] == '^':
        alteration = 1
        abc_note = abc_note[1:]
    elif abc_note[0] == '_':
        alteration = -1
        abc_note = abc_note[1:]

    midi_c4_number = 60
    midi_note_number = midi_c4_number
    if abc_note.islower():
        midi_note_number += 12
        abc_note = abc_note.upper()
    midi_note_number += musictheory.c_major_scale_intervals[abc_note] + alteration
    return midi_note_number
