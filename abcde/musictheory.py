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


def get_note_alteration_in_key(abc_note, abc_key):
    """Given a note without ABC alteration (no '_', '^' or '=') and a
    normalized key, tell whether the note is natural, sharp or flat in the key.

    :param abc_note: A text string representing an ABC note eg 'b'
    :param abc_key: A tuple representing a normalized ABC key, eg ('D', 'mix')
                    or ('Bb', 'min'). Defaults to ('C', 'maj').

    :return: '' (natural), '_' (flat), '^' (sharp)
    """

    (root, mode) = abc_key
    if mode != 'maj':
        return ''

    scale = MAJOR_SCALES[root + mode]
    for note in scale:
        if note[0].lower() == abc_note.lower():
            if len(note) == 1:
                return ''
            if note[1] == '#':
                return '^'
            elif note[1] == 'b':
                return '_'
    return ''
