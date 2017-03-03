#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools that parse the ABC input
"""

def normalize_abc_key(abc_key):
    """
    Given a key in ABC format (eg. 'C' or 'Gmaj' or 'Dmajor' or 'Amixo' or 'F#m'),
    return a normalized tuple where the first element is the scale base note in
    upper case optionally with a sharp/flat alteration and the second element is
    the mode in lower case and with 3 characters.

    :param abc_key: key in ABC format, eg. 'C' or 'Gmaj' or 'Dminor' or 'Amixo' or 'Bb'
    :return: a tuple (tonic, mode), eg ('C', 'maj') or
        ('G', 'maj') or ('D', 'min') or ('A', 'mix') or ('Bb', 'maj')
    """

    # TODO: warn on improperly written keys? where is done syntax validation? in this file anyway...
    # TODO: naming convention: raw_ in the input before parsing/normalization eg raw_abc_key

    tonic = abc_key[0].upper()
    abc_key = abc_key[1:]

    alteration = ''
    if len(abc_key) >= 1 and abc_key[0] in ('b', '#'):
        alteration = abc_key[0]
        abc_key = abc_key[1:]

    mode = None
    if len(abc_key) == 0:
        mode = 'maj'
    elif len(abc_key) == 1 and abc_key[0] == 'm':
        mode = 'min'
    elif len(abc_key) >= 3:
        for prefix in ('maj', 'ion', 'dor', 'phr', 'lyd', 'mix', 'min', 'eol', 'loc'):
            if abc_key.startswith(prefix):
                mode = prefix
                break

    # Assume major if the key is improperly written
    if mode is None:
        mode = 'maj'

    if mode == 'ion':
        mode = 'maj'
    if mode == 'eol':
        mode = 'min'

    return (tonic + alteration, mode)
