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


def default_abc_tempo(rhythm: Optional[str], speed: str = "medium"):
    """Provide default tempo values for common rhythms

    Args:
        rhythm: tune rhythm/type ("reel", "jig", "hornpipe", ...)
        speed: "slow", "medium" or "fast"
    """
    predefined_tempos = {
        "reel": {
            "slow": "1/2=60",
            "medium": "1/2=90",
            "fast": "1/2=116",
        },
        "jig": {
            "slow": "3/8=90",
            "medium": "3/8=110",
            "fast": "3/8=130",
        },
        "hornpipe": {
            "slow": "1/2=50",
            "medium": "1/2=70",
            "fast": "1/2=82",
        },
        "polka": {
            "slow": "1/4=110",
            "medium": "1/4=140",
            "fast": "1/4=156",
        },
        "slide": {
            "slow": "3/8=100",
            "medium": "3/8=140",
            "fast": "3/8=150",
        },
        "fling": {
            "slow": "1/2=60",
            "medium": "1/2=80",
            "fast": "1/2=106",
        },
        "waltz": {
            "slow": "1/4=108",
            "medium": "1/4=146",
            "fast": "1/4=165",
        },
        "mazurka": {
            "slow": "1/4=120",
            "medium": "1/4=150",
            "fast": "1/4=160",
        },
    }

    fallback_tempos = {
        # Fallback tempo values for unknown/undefined rhythms
        # (120 quarter notes per minutes is also the default in abc2midi and fluidsynth)
        "slow": "1/4=100",
        "medium": "1/4=120",
        "fast": "1/4=140"
    }

    try:
        tempo_str = predefined_tempos[rhythm][speed]
        log.debug('use default tempo for %s %s: "%s"', speed, rhythm, tempo_str)
    except KeyError:
        tempo_str = fallback_tempos[speed]
        if rhythm is None or rhythm == "":
            reason = "undefined rhythm"
        else:
            reason = f'unknown rhythm "{rhythm}"'
        log.debug('%s: use fallback %s tempo: "%s"', reason, speed, tempo_str)
    return AbcTempo(tempo_str)
