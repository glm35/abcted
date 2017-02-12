#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools to convert data from the ABC world to the MIDI world
"""

# abc2midi utils

c_major_scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
major_scale_intervals = [0, 2, 4, 5, 7, 9, 11]
c_major_scale_intervals = dict(zip(c_major_scale, major_scale_intervals))

MAJOR_SCALES = {
    'Cmaj' : ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    'Gmaj' : ['G', 'A', 'B', 'c', 'd', 'e', 'f#'],
    'Dmaj' : ['D', 'E', 'F#', 'G', 'A', 'B', 'c#']
}

MODE_ALTERATIONS = {
    'maj': [0, 0, 0, 0, 0, 0, 0],
    'dor': [0, 0, -1, 0, 0, 0, -1], # b3, b7
    'phr': [0, -1, -1, 0, 0, -1, -1], # b2, b3, b6, b7
    'lyd': [0, 0, 0, 1, 0, 0, 0], # #4
    'mix': [0, 0, 0, 0, 0, 0, -1], # b7
    'min': [0, 0, -1, 0, 0, -1, -1], # b3, b6, b7
    'loc': [0, -1, -1, 0, -1, -1, -1], # b2, b3, b5, b6, b7
}


def get_midi_note(abc_note, abc_key = 'C'):
    """"Convert an ABC note to a midi number

    :param abc_note: A text string representing an ABC note eg 'b'
    :param abc_key: A string representing the key of the note eg 'C' or 'Cmaj' or 'Dmix'. Defaults to C major.

    :return: the MIDI note number of the ABC note
    """

    (base_note, mode) = normalize_abc_key(abc_key)

    alteration = get_mode_alteration(abc_note, base_note + mode)

    midi_c4_number = 60
    midi_note_number = midi_c4_number
    if abc_note.islower():
        midi_note_number += 12
        abc_note = abc_note.upper()
    midi_note_number += c_major_scale_intervals[abc_note] + alteration
    return midi_note_number


def get_mode_alteration(abc_note, abc_key):
    """Given a note without ABC alteration (no '_', '^' or '=') and a
    normalized mode, return 0 if the note is unaltered, -1 if the note must be
    flattened or +1 if the note must be sharpened.

    :param abc_note: A text string representing an ABC note eg 'b'
    :param abc_key: A normalized string representing the key of the note
        eg 'Cmaj' or 'Dmix'.

    :return: 0 (natural), -1 (flat), +1 (sharp)
    """

    scale = MAJOR_SCALES[abc_key]
    for note in scale:
        if note[0].lower() == abc_note.lower():
            if len(note) == 1:
                return 0
            if note[1] == '#':
                return 1
            elif note[1] == 'b':
                return -1
    return 0


def normalize_abc_key(abc_key):
    """
    Given a key in ABC format (eg. 'C' or 'Gmaj' or 'Dmajor' or 'Amixo' or 'Bm'),
    return a normalized tuple where the first element is the scale base note in
    upper case and the second element is the mode in lower case and with 3
    characters.

    :param abc_key: key in ABC format, eg. 'C' or 'Gmaj' or 'Dmajor' or 'Amixo' or 'Bm'
    :return: a tuple (base_note, mode), eg ('C', 'maj') or
        ('G', 'maj') or ('D', 'maj') or ('A', 'mix') or ('B', 'min')
    """

    base_note = abc_key[0].upper()

    mode = None
    if len(abc_key) == 1:
        mode = 'maj'
    elif len(abc_key) == 2 and abc_key[1] == 'm':
        mode = 'min'
    elif len(abc_key) >= 4:
        for prefix in ['maj', 'ion', 'dor', 'phr', 'lyd', 'mix', 'min', 'eol', 'loc']:
            if abc_key[1:].startswith(prefix):
                mode = prefix
                break

    # Assume major if the key is improperly written
    if mode is None:
        mode = 'maj'

    if mode == 'ion':
        mode = 'maj'
    if mode == 'eol':
        mode = 'min'

    return (base_note, mode)
