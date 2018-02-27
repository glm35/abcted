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
                pass
            #elif abcparser.is_header(line):
            #    pass
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
