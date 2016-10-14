#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools to convert data from the ABC world to the MIDI world
"""

# abc2midi utils

c_major_scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
major_scale_intervals = [0, 2, 4, 5, 7, 9, 11]
c_major_scale_intervals = dict(zip(c_major_scale, major_scale_intervals))


def get_midi_note(abc_note, abc_key = 'C'):
    """"Convert an ABC note to a midi number

    :param abc_note A text string representing an ABC note eg 'b'

    :param abc_key A string representing the key of the note eg 'C' or 'Cmaj' or 'Dmix'. Defaults to C major.

    :return the MIDI note number of the ABC note
    """

    if abc_key is 'Dmaj' and abc_note is 'F':
        return 66

    midi_c4_number = 60
    midi_note_number = midi_c4_number
    if abc_note.islower():
        midi_note_number += 12
        abc_note = abc_note.upper()
    midi_note_number += c_major_scale_intervals[abc_note]
    return midi_note_number
