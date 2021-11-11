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


C_MAJOR_SCALE = MAJOR_SCALES['Cmaj']
MAJOR_SCALE_INTERVALS = [0, 2, 4, 5, 7, 9, 11]
C_MAJOR_SCALE_INTERVALS = dict(zip(C_MAJOR_SCALE, MAJOR_SCALE_INTERVALS))


def get_note_alteration_in_key(simple_note, abc_key):
    """Given a note without ABC alteration (no '_', '^' or '=') and a
    normalized key, tell whether the note is natural, sharp or flat in the key.

    :param simple_note: A text string representing a note without alteration eg 'b'
    :param abc_key: A tuple representing a normalized ABC key, eg ('D', 'mix')
                    or ('Bb', 'min').

    :return: '' (natural), '_' (flat), '__' (double flat), '^' (sharp), '^^' (double sharp)
    """

    (root, mode) = abc_key

    # Find the alteration of the note in the major scale that has the same
    # root as abc_key. Also find the place (index) of the note in the major
    # scale, this will be useful for the next step

    alteration = 0
    scale = MAJOR_SCALES[root + 'maj']
    for (index, note) in enumerate(scale):
        if note[0].lower() == simple_note.lower():
            if len(note) == 1:
                alteration = 0
            elif note[1] == '#':
                alteration = 1
            elif note[1] == 'b':
                alteration = -1
            break

    # Add the alteration of the note in the mode of abc_key to the major scale
    # alteration

    alteration += MODE_ALTERATIONS[mode][index]

    if alteration == 1:
        return '^'
    elif alteration == 2:
        return '^^'
    elif alteration == -1:
        return '_'
    elif alteration == -2:
        return '__'
    else:
        return ''
