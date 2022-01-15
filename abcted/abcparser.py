#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools that parse the ABC input
"""

import logging as log
from typing import List, Optional

from edit_zone_buffer import EditZoneBuffer
import musictheory


class AbcParserException(Exception):
    pass


def get_note_to_play(edit_buffer: EditZoneBuffer, keysym):
    """Given a keysym following a key press, check whether there is a
     note to play. If so, return the note.

     :param edit_buffer: The buffer containing the text being edited

     :param keysym The key pressed. It has to be a valid ABC note, ie its
                   lower-case value must belong to musictheory.c_major_scale

     :return a String with the note to play in ABC-normalized format, or None
             if there is no note to play. The note is absolute, ie not relative to
             the tune scale. Examples: 'c', "c'", 'C', 'C,,', '^C' (C sharp), '_c' (c flat)
     """

    log.debug('keysym=' + keysym)

    # Check whether we are in comment context
    raw_abc_line = edit_buffer.get_current_line_to_cursor()
    if raw_abc_line.find('%') != -1:
        # There is a '%' before the text cursor => we are in comment context
        return None

    # Check whether we are in an information line
    if len(raw_abc_line) >= 2:
        if raw_abc_line[1] == ':':
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
        log.debug("raw_key at insert: " + raw_key)
        try:
            abc_key = normalize_abc_key(raw_key)
        except AbcParserException:
            return None  # Don't try to play anything if the key is invalid

        # Get the note to play with all the useful attributes (accidentals,
        # octave changes, ...)
        alteration = musictheory.get_note_alteration_in_key(simple_note, abc_key)
        abc_note = alteration + simple_note

    abc_note = abc_note + octave_marker

    log.debug('abc_note=' + abc_note)
    return abc_note


def get_current_raw_key(edit_buffer: EditZoneBuffer):
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


def normalize_abc_key(raw_key: str):
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
        log.warning(msg)
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
        log.warning(msg)
        raise AbcParserException(msg)

    return root + alteration, mode


def get_accidental(raw_abc: str):
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


def get_current_raw_tune(buffer: EditZoneBuffer) -> List[str]:
    """
    Return the current tune around the cursor.

    Args:
        buffer: the EditZoneBuffer to look for the tune

    Returns:
        An array of strings, one per line, starting at the ABC reference
        number (X: header).

    Raises:
        AbcParserException: if the tune cannot be extracted

    """
    raw_tune = []

    # Read lines including and above the current line until
    # the ABC reference number is found.  If no
    # reference number can be found, raise an exception.

    line_no = cur_line_no = buffer.get_line_no_at_cursor()
    while True:
        line = buffer.get_line(line_no)
        raw_tune.insert(0, line)
        if is_reference_number(line):
            break
        else:
            line_no -= 1
            if line_no == 0:  # line numbers start at 1
                msg = 'Reference number (X: header) missing in current tune'
                log.error(msg)
                raise AbcParserException(msg)

    # Read lines below the current line until the next reference number or
    # the end of the buffer (empty line).
    # TODO: change get_line() to have an exception when we pass the end of
    # the buffer.  So that we accept empty lines inside a tune.

    line_no = cur_line_no + 1
    while True:
        line = buffer.get_line(line_no)
        if is_reference_number(line) or line.strip() == '':
            break
        raw_tune.append(line)
        line_no += 1

    return raw_tune


def get_tune_title(raw_tune: List[str]) -> Optional[str]:
    """Get ABC tune title.

    Given an ABC tune as a list of strings, one string per line, return the
    first title of the tune.  Return an empty string if no title can be found.
    """
    for line in raw_tune:
        if line.startswith("T:"):
            return line[2:].strip()
    return ""


def is_reference_number(line: str) -> bool:
    """
    Given a line of ABC text, tell whether it is a reference number
    (X: header) or not.

    Args:
        line: the line of text to process

    Returns:
        True if the line is a X: header else False
    """
    return line.strip().startswith('X:')


def is_comment(line: str) -> bool:
    """
    Given a line of ABC text, tell whether it is a comment (starts with %)
    or not.

    Args:
        line: line of text to check

    Returns:
        True (line is comment) or False (line is not comment)
    """
    return line.strip().startswith('%')


def is_header(line: str) -> bool:
    """
    Given a line of ABC text, tell whether it looks like an ABC header or not.

    Args:
        line: line of text to check

    Returns:
        True (line is header) or False (line is not header)

    """
    abc_headers = ['A:', 'B:', 'C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:',
                   'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:',
                   'T:', 'W:', 'X:', 'Z:']
    for header in abc_headers:
        if line.startswith(header):
            return True
    return False


def parse_default_note_length(line: str):
    """
    Given a line containing a raw default note length, eg '1/8', return
    a tuple eg (1, 8)

    Args:
        line: raw default not length following the
            default note length header 'L:'

    Returns:
        a tuple representing a fraction (numerator, denominator)

    Raises:
        AbcParserException
    """
    try:
        f = [int(s) for s in line.split('/')]
        if len(f) == 2 and f[0] == 1 and f[1] in [4, 8, 16, 32]:
            return tuple(f)
    except ValueError:
        pass
    raise AbcParserException('Invalid default note length: \'' + line + '\'')


def parse_meter(line: str):
    """
    Given a line containing a raw meter, eg '6/8', return
    a tuple eg (6, 8)

    Args:
        line: raw meter following the meter header 'M:'

    Returns:
        a tuple representing a fraction (numerator, denominator)

    Raises:
        AbcParserException
    """
    line = line.strip()
    if line == 'C':
        return 4, 4
    elif line == 'C|':
        return 2, 2
    try:
        f = [int(s) for s in line.split('/')]
        if len(f) == 2:
            return tuple(f)
    except ValueError:
        pass
    raise AbcParserException('Invalid meter: \'' + line + '\'')


def parse_tempo(line: str):
    """
    Given a line containing a raw tempo, eg '120' or '3/8=120', return a tuple
    where the first element is an optional note length tuple and the second
    element is the number of beats per minute for a beat of the note length.
    If a note length is not given, the default note length will be used.

    Args:
        line: raw tempo following the tempo header 'Q:'

    Returns:
        a tuple (note length, bpm) eg (None, 120) for 'Q:120'
            or ((3, 8), 120) for 'Q:3/8=120'

    Raises:
        AbcParserException

    Notes:
        The forms such as 'C=120' and 'C3=120' found in the ABC 1.6 standard
        are not supported.
    """

    # Form 1: ex 'Q:120'
    try:
        bpm = int(line)
        return None, bpm
    except ValueError:
        pass

    # Form 2: ex 'Q:3/8=120'
    f = line.split('=')
    if len(f) == 2:
        try:
            f2 = [int(s) for s in f[0].split('/')]
            return tuple(f2), int(f[1])
        except ValueError:
            pass
    raise AbcParserException('Invalid or unsupported tempo: \'' + line + '\'')
