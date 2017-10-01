#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools that parse the ABC input
"""

import logging
import musictheory


class AbcParserException(Exception):
    pass


def get_note_to_play(edit_buffer, keysym):
    """Given a keysym following a key press, check whether there is a
     note to play. If so, return the note.

     :param edit_buffer: The buffer containing the text being edited

     :param keysym The key pressed. It has to be a valid ABC note, ie its
                   lower-case value must belong to musictheory.c_major_scale

     :return a String with the note to play in ABC-normalized format, or None
             if there is no note to play. The note is absolute, ie not relative to
             the tune scale. Examples: 'c', "c'", 'C', 'C,,', '^C' (C sharp), '_c' (c flat)
     """

    logging.debug('get_note_to_play(): keysym=' + keysym)

    # Check whether we are in comment context
    raw_abc_line = edit_buffer.get_current_line_to_cursor()
    if raw_abc_line.find('%') != -1:
        # There is a '%' before the text cursor => we are in comment context
        return None

    # Check whether we are in an information line
    if len(raw_abc_line) >= 2:
        if raw_abc_line[1] is ':':
            if 'A' <= raw_abc_line[0] <= 'Z':
                return None

    # Handle octave markers
    octave_marker = ''
    if keysym == "'" or keysym == ',':
        try:
            tentative_note = raw_abc_line[-1]
        except IndexError:
            return None
        if tentative_note.upper() in musictheory.C_MAJOR_SCALE:
            raw_abc_line = raw_abc_line[:-1]
            simple_note = tentative_note
            octave_marker = keysym
            if ((simple_note.islower() and octave_marker == ',')
                or (simple_note.isupper() and octave_marker == "'")):
                return None
        else:
            return None
    elif keysym.upper() in musictheory.C_MAJOR_SCALE:
        simple_note = keysym
    else:
        return None

    # Find whether there is an accidental before the note
    accidental = get_accidental(raw_abc_line)
    if accidental != '':
        if accidental == '=':  # natural
            abc_note = simple_note
        else:  # (double) sharp, (double) flat
            abc_note = accidental + simple_note
    else:
        # Find the tune key at the insertion point
        raw_key = get_current_raw_key(edit_buffer)
        logging.debug("get_note_to_play(): raw_key at insert: " + raw_key)
        try:
            abc_key = normalize_abc_key(raw_key)
        except AbcParserException:
            return None  # Don't try to play anything if the key is invalid

        # Get the note to play with all the useful attributes (accidentals,
        # octave changes, ...)
        alteration = musictheory.get_note_alteration_in_key(simple_note, abc_key)
        abc_note = alteration + simple_note

    abc_note = abc_note + octave_marker

    logging.debug('get_note_to_play(): abc_note=' + abc_note)
    return abc_note


def get_current_raw_key(edit_buffer):
    """Get the contents of the key info field for the current tune.

    :return: a string with whatever can be found in the key info field. It
             should be something like 'C' or 'Eb minor' or 'A mix', but it
             is not controlled and not guaranteed to be valid here.
    """

    # Assume 'C major' if no key is specified
    key = 'C'

    # For each line going upward until until the line starts with 'X:'
    # (beginning of the tune found) or until there are no more lines,
    # look for the key:

    line_no = edit_buffer.get_line_no_at_cursor()
    while line_no > 0:
        line = edit_buffer.get_line(line_no)
        if line.startswith('K:'):
            key = line[2:]
            break
        if line.startswith('X:'):
            # We reached the beginning of the tune
            break
        line_no -= 1

    return key


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

    raw_key = raw_key.strip()  # Remove leading and trailing spaces

    # Parse the key root

    root = raw_key[0].upper()
    raw_key = raw_key[1:]

    alteration = ''
    if len(raw_key) >= 1 and raw_key[0] in ('b', '#'):
        alteration = raw_key[0]
        raw_key = raw_key[1:]

    if root + alteration + 'maj' not in musictheory.MAJOR_SCALES.keys():
        msg = root + alteration + raw_key + ' is not a valid key name'
        logging.warning(msg)
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
        if mode == 'ion':
            mode = 'maj'
        if mode == 'eol':
            mode = 'min'

    # Raise exception if the mode cannot be understood
    if mode is None:
        msg = root + alteration + raw_key + ' is not a valid key name'
        logging.warning(msg)
        raise AbcParserException(msg)

    return root + alteration, mode


def get_accidental(raw_abc):
    """
    Find whether there is an accidental at the end of the given string

    :param raw_abc: A piece of supposedly ABC text

    :return A string representing the accidental: '' (none), '=' (natural), '^' (sharp),
        '^^' (double sharp), '_' (flat), '__' (double flat)
    """

    accidental = ''

    try:
        c = raw_abc[-1]
        if c == '=':
            accidental = c
        elif c == '^' or c == '_':
            accidental = c
            try:
                d = raw_abc[-2]
                if d == c:
                    accidental = d + accidental
            except IndexError:
                pass
    except IndexError:
        pass

    return accidental
