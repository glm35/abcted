#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools to convert data from the ABC world to the MIDI world
"""

import abcparser
import musictheory

def get_midi_note(abc_note, abc_key = 'C'):
    """"Convert an ABC note to a midi number

    :param abc_note: A text string representing an ABC note eg 'b'
    :param abc_key: A string representing the key of the note eg 'C' or 'Cmaj' or 'Dmix'. Defaults to C major.

    :return: the MIDI note number of the ABC note
    """

    # TODO: input = (tonic, mode) typle

    (tonic, mode) = abcparser.normalize_abc_key(abc_key)

    alteration = musictheory.get_mode_alteration(abc_note, tonic + mode)

    midi_c4_number = 60
    midi_note_number = midi_c4_number
    if abc_note.islower():
        midi_note_number += 12
        abc_note = abc_note.upper()
    midi_note_number += musictheory.c_major_scale_intervals[abc_note] + alteration
    return midi_note_number
