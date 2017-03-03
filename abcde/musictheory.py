#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools and constants with the knowledge of the musical theory
"""

MAJOR_SCALES = {
    'Cmaj' : ['C', 'D', 'E', 'F', 'G', 'A', 'B'],

    'Gmaj' : ['G', 'A', 'B', 'c', 'd', 'e', 'f#'],
    'Dmaj' : ['D', 'E', 'F#', 'G', 'A', 'B', 'c#'],
    'Amaj' : ['A', 'B', 'c#', 'd', 'e', 'f#', 'g#'],
    'Emaj' : ['E', 'F#', 'G#', 'A', 'B', 'c#', 'd#'],
    'Bmaj' : ['B', 'c#', 'd#', 'e', 'f#', 'g#', 'a#'],
    'F#maj' : ['F#', 'G#', 'A#', 'B', 'c#', 'd#', 'e#'],
    'C#maj' : ['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#'],

    'Fmaj' : ['F', 'G', 'A', 'Bb', 'c', 'd', 'e', 'f'],
    'Bbmaj' : ['Bb', 'c', 'd', 'eb', 'f', 'g', 'a'],
    'Ebmaj' : ['Eb', 'F', 'G', 'Ab', 'Bb', 'c', 'd'],
    'Abmaj' : ['Ab', 'Bb', 'c', 'db', 'eb', 'f', 'g'],
    'Dbmaj' : ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'c'],
    'Gbmaj' : ['Gb', 'Ab', 'Bb', 'cb', 'db', 'eb', 'f'],
    'Cbmaj' : ['Cb', 'Db', 'Eb', 'Fb', 'Gb', 'Ab', 'Bb']
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


c_major_scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
major_scale_intervals = [0, 2, 4, 5, 7, 9, 11]
c_major_scale_intervals = dict(zip(c_major_scale, major_scale_intervals))


def get_mode_alteration(abc_note, abc_key):
    """Given a note without ABC alteration (no '_', '^' or '=') and a
    normalized mode, return 0 if the note is unaltered, -1 if the note must be
    flattened or +1 if the note must be sharpened.

    :param abc_note: A text string representing an ABC note eg 'b'
    :param abc_key: A normalized string representing the key of the note
        eg 'Cmaj' or 'Dmix'.

    :return: 0 (natural), -1 (flat), +1 (sharp)
    """

    # TODO: input: abc_key = a normalized ABC key: (tonic, mode) tuple

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
