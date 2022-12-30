#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Provide an abstraction of an ABC tempo, tools to convert the tempo and
sensible default tempo values for trad rhythms.
"""

import logging as log
from typing import Optional


class AbcTempoException(Exception):
    def __init__(self, msg):
        self.msg = msg


class AbcTempo:
    def __init__(self, abc_tempo_str: str):
        self._beat_specs = None  # eg (3, 8) for 3/8, or None
        self._bpm = None  # eg 120
        self._parse_tempo(abc_tempo_str)

    @property
    def bpm(self):
        """Tempo in beats per minute (for musicians)"""
        return self._bpm

    @bpm.setter
    def bpm(self, bpm: int):
        if bpm < 1:
            raise ValueError
        self._bpm = bpm

    @property
    def qpm(self):
        """Tempo in quarter notes per minute (for fluidsynth)"""
        if self._beat_specs is None:
            return self._bpm  # Assume beat specs = 1/4, but not always correct
        else:
            return int(self._bpm * 4 * self._beat_specs[0] / self._beat_specs[1])

    def __str__(self):
        if self._beat_specs is None:
            return str(self._bpm)
        else:
            return f'{self._beat_specs[0]}/{self._beat_specs[1]}={self._bpm}'

    def _parse_tempo(self, abc_tempo_str: str):
        """Parse ABC tempo header value

        Examples of supported ABC tempo header values: '120', '1/2=110", '3/8=120'

        Args:
            abc_tempo_str: raw ABC tempo string (without 'Q:' marker)

        Raises:
            AbcTempoException

        Notes:
            The forms such as 'C=120' and 'C3=120' found in the ABC 1.6 standard
            are not supported.
        """
        # Form 1: ex 'Q:120'
        try:
            self.bpm = int(abc_tempo_str)
            return
        except ValueError:
            pass

        # Form 2: ex 'Q:3/8=120'
        beat_specs, bpm = abc_tempo_str.split('=')
        try:
            self.bpm = int(bpm)
            self._beat_specs = tuple(int(s) for s in beat_specs.split('/'))
            if len(self._beat_specs) == 2:
                return
        except ValueError:
            pass
        raise AbcTempoException(f"Invalid or unsupported tempo: '{abc_tempo_str}'")


def default_abc_tempo(rhythm: Optional[str]):
    """Provide default tempo values for common rhythms"""
    default_tempos = {
        "reel": "1/2=90",
        "jig": "3/8=110",
        "hornpipe": "1/2=70",
        "polka": "1/4=140",
        "slide": "3/8=140",
        "fling": "1/2=80"
    }
    try:
        tempo_str = default_tempos[rhythm]
        log.debug('use default tempo for rhythm="%s": "%s"', rhythm, tempo_str)
    except KeyError:
        # Default to 120 quarter notes per minutes
        # (rem: this is also the default in abc2midi and fluidsynth)
        tempo_str = "1/4=120"
        log.debug('unknown or undefined rhythm="%s", use fallback tempo: "%s"', rhythm, tempo_str)
    return AbcTempo(tempo_str)
