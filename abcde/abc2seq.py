#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Transform a raw ABC tune into a sequence that can be played by the sequencer
"""

import logging as log
from typing import List

import abcparser


TPB = 240  # tick per beats = constant by convention
DEFAULT_BPM = 120


class Sequence:
    """
    A sequence of notes with relative ticks that can be played by the
    sequencer
    """

    def __init__(self):
        self.anacrusis = None  # not repeated in a sequence loop
        self.flat_tune = None  # the actual sequence
        self.tpb = TPB
        self.bpm = DEFAULT_BPM
        self.tpn = 0  # ticks per note


class AbcParserStateMachine:
    """
    State machine to parse lines in an ABC tune.
    """

    def __init__(self):
        # States of the "line processing" state machine
        self.S_BEGIN = 'BEGIN'
        self.S_HEADER = 'HEADER'
        self.S_TUNE = 'TUNE'
        self.S_END = 'END'

        self._state = self.S_BEGIN

        # ABC tune info
        self.key = None  # eg ('C', 'maj')
        self.default_note_length = None  # eg (1, 8)
        self.meter = None  # eg (6, 8)
        self.tempo = None  # eg (None, 120) or ((1, 8), 120)


    def run(self, line: str):
        line = line.strip()  # Strip leading and trailing spaces

        # Skip comments and empty lines
        if abcparser.is_comment(line) or line == '':
            return

        if self._state == self.S_BEGIN:
            if abcparser.is_reference_number(line):
                self._state = self.S_HEADER
            else:
                log.warning('ABC parser: unexpected line: \'' + line + '\'')

        elif self._state == self.S_HEADER:
            # Find userful information in the header: key (K:), default not length (L:),
            # meter (M:), tempo (Q:).  Forget the other header fields.
            #
            # rem: all these "useful" headers can re-appear and change in the tune

            if line.startswith('K:'):
                self.key = abcparser.normalize_abc_key(line[2:])
                log.debug('ABC parser: key = ' + str(self.key))

            elif line.startswith('L:'):
                self.default_note_length = \
                    abcparser.parse_default_note_length(line[2:])
                log.debug('ABC parser: default note length = '
                          + str(self.default_note_length))

            elif line.startswith('M:'):
                self.meter = abcparser.parse_meter(line[2:])
                log.debug('Abc parser: meter = ' + str(self.meter))

            elif line.startswith('Q:'):
                self.tempo = abcparser.parse_tempo(line[2:])
                log.debug('Abc parser: tempo = ' + str(self.tempo))

            elif abcparser.is_header(line):
                pass

            else:
                log.warning('ABC parser: unexpected line: \'' + line + '\'')
        else:
            log.warning('ABC parser: unexpected line: \'' + line + '\'')


def abc2seq(raw_abc_tune: List[str]) -> Sequence:
    """
    Transform a raw ABC tune into a sequence that can be played by the
    sequencer.

    Args:
        raw_abc_tune: ABC tune starting with the reference number (X: header)
            but unvalidated otherwise.  Each element of the list is a line
            of text.

    Returns:
        A sequence to be played by the sequencer.
    """

    stm1 = AbcParserStateMachine()
    for line in raw_abc_tune:
        stm1.run(line)
