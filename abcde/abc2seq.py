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
        self.npm = 0  # notes per minute
        self.tpn = 0  # ticks per note


class AbcSequencerException(Exception):
    pass


def compute_notes_per_minute(default_note_length, meter, tempo) -> int:
    """
    Compute the number of notes per minutes.  This will be used to configure
    the tempo of the sequencer.

    Args:
        default_note_length: tuple of int, eg (1, 8) for 'L:1/8'.  This
            parameter is optional and can be None
        meter: tuple of int, eg (6, 8) for 'M:6/8'
        tempo: tuple (absolute note length, tempo), eg (None, 120) for 'Q:120'
            or ((3, 8), 120) for 'Q:3/8=120'

    Returns:
        The number of notes per minutes (int)

    Raises:
        AbcSequencerException if meter or tempo is not set
    """
    if meter is None or tempo is None:
        raise AbcSequencerException('Cannot compute notes per minutes: '
                                    'missing meter or tempo')

    # If the default note length is not set, deduce it from the meter:
    if default_note_length is None:
        default_note_length = (1, meter[1])

    # If the tempo note length is not explicitly set, use default note length
    if tempo[0] is None:
        tempo = (default_note_length, tempo[1])

    npm = tempo[1] * tempo[0][0] * default_note_length[1] / tempo[0][1]
    return int(npm)


def compute_ticks_per_note(notes_per_minute: int) -> int:
    """
    Compute the number of ticks per default length note at the current
    tempo.  We try to maximise the resolution, but we have to stay below
    the max ticks per second that fluidsynth supports.

    Args:
        notes_per_minute: number of notes of the default length per minute

    Returns:
        number of ticks per default length note

    """
    max_ticks_per_second = 1000
    tpn_candidates = [60, 120, 240, 480]
    for tpn in reversed(tpn_candidates):
        if tpn * notes_per_minute / 60 <= max_ticks_per_second:
            return tpn
    return tpn_candidates[0]


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

        #
        self.seq = Sequence()

    def _update_notes_per_minute(self):
        self.seq.npm = compute_notes_per_minute(
            self.default_note_length, self.meter, self.tempo)
        self.seq.tpn = compute_ticks_per_note(self.seq.npm)
        log.debug('ABC parser: notes_per_minute = ' + str(self.seq.npm))
        log.debug('ABC parser: ticks_per_note = ' + str(self.seq.tpn))

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
                self._state = self.S_TUNE
                self._update_notes_per_minute()

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

        elif self._state == self.S_TUNE:
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
