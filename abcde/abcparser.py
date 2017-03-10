#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools that parse the ABC input
"""

import musictheory


class AbcParserException(Exception):
    pass


def normalize_abc_key(raw_key):
    """
    Given a key in ABC format as found in the ABC input (eg. 'C' or 'Gmaj' or 'Dmajor' or 'Amixo' or 'F#m'),
    return a normalized tuple (root, mode) where the first element is the scale base note in
    upper case optionally with a sharp/flat alteration and the second element is
    the normalized mode in lower case and with 3 characters.

    :param raw_key: raw text data following the 'K:' prefix in a key
                    information field. Examples of expected (valid) input:
                    'C' or 'Gmaj' or 'Dminor' or 'Amixo' or 'Bb'

    :return a tuple (root, mode) where root is a valid root and mode a
            normalized mode, eg ('C', 'maj') or ('G', 'maj') or ('D', 'min')
            or ('A', 'mix') or ('Bb', 'maj')

    :exception AbcParserException: the format of raw_text is invalid and cannot be parsed
    """

    # Parse the key root

    root = raw_key[0].upper()
    raw_key = raw_key[1:]

    alteration = ''
    if len(raw_key) >= 1 and raw_key[0] in ('b', '#'):
        alteration = raw_key[0]
        raw_key = raw_key[1:]

    if root + alteration + "maj" not in musictheory.MAJOR_SCALES.keys():
        msg = root + alteration + " is not a valid key name"
        print("warning: " + msg)  # TODO: use a logger
        raise AbcParserException(msg)

    # Parse the key mode

    mode = None
    if len(raw_key) == 0:
        mode = 'maj'
    elif len(raw_key) == 1 and raw_key[0] == 'm':
        mode = 'min'
    elif len(raw_key) >= 3:
        for prefix in ('maj', 'ion', 'dor', 'phr', 'lyd', 'mix', 'min', 'eol', 'loc'):
            if raw_key.startswith(prefix):
                mode = prefix
                break
    # TODO: raise exception if the mode cannot be understood

    # Assume major if the key is improperly written
    if mode is None:
        mode = 'maj'

    if mode == 'ion':
        mode = 'maj'
    if mode == 'eol':
        mode = 'min'

    return root + alteration, mode


def get_accidental(cur_line_to_insert):
    """
    Find whether there is an accidental at the end of the current line before
    the insert point.

    :param cur_line_to_insert: the current line of text from start to insert point

    :return A string representing the accidental: '' (none), '=' (natural), '^' (sharp),
        '^^' (double sharp), '_' (flat), '__' (double flat)
    """

    accidental = ''

    try:
        c = cur_line_to_insert[-1]
        if c == '=':
            accidental = c
        elif c == '^' or c == '_':
            accidental = c
            try:
                d = cur_line_to_insert[-2]
                if d == c:
                    accidental = d + accidental
            except IndexError:
                pass
    except IndexError:
        pass

    return accidental
