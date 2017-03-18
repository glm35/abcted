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

    # We handle octave jumps with the assumption that abc_note is correct:
    # we don't check that we have a lower case letter before ',' or an upper case
    # letter before "'".
    octave_jump = 0
    tentative_octave_marker = abc_note[-1]
    if tentative_octave_marker == ',':
        octave_jump = -12
    elif tentative_octave_marker == "'":
        octave_jump = 12
    if octave_jump != 0:
        abc_note = abc_note[:-1]

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
    midi_note_number += octave_jump + alteration + musictheory.C_MAJOR_SCALE_INTERVALS[abc_note]
    return midi_note_number
