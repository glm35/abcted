#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# PSL imports
import logging as log
from threading import Timer, Lock
import traceback

# Third-party imports
from pyfluidsynth3 import fluidaudiodriver, fluidhandle, fluidsettings, fluidsynth
from pyfluidsynth3.fluiderror import FluidError

# abcde imports
import abc2midi


# midi utils

midi_programs = {
    'Acoustic Grand Piano': 0,
    'Accordion': 21,
    'Flute': 73,
    'Fiddle': 110
}

soundfonts = [  # We will use the first sound font that can be found in that list:
    '/usr/share/sounds/sf2/FluidR3_GM.sf2',
    '/usr/share/sounds/sf2/default.sf2'  # Fedora: symlink to '/usr/share/soundfonts/FluidR3_GM.sf2'
]


class SingleNoteAbcPlayerException(Exception):
    pass


class SingleNoteAbcPlayer:
    def __init__(self):
        """Create a soundless player. This object cannot produce a sound (yet), but
           it can be used as a stub in soundless setups.
        """
        self._instrument = 'Acoustic Grand Piano'
        self._midi_note = None  # MIDI note number
        self._midi_channel = 0  # MIDI channel to play the note
        self._midi_program = midi_programs[self._instrument]
        self._velocity = 1.0    # MIDI note velocity
        self._delay_s = 0.5     # Note duration in seconds

        self._timer = None
        self._lock = Lock()
            # 'lock' protects:
            # - the instance variables used by _on_timeout()
            # - libfluidsynth (in case it is not reentrant, which is unknown to me at the moment)

        self._no_sound = True

    def setup_synth(self):
        """Setup the player so that it can produce sound.

           Raises:
               SingleNoteAbcPlayerException: an error occured during the synth setup.
                   Most common errors: fluidsynth library not found, soundfont not found.
        """
        try:
            self._handle = fluidhandle.FluidHandle()
            self._settings = fluidsettings.FluidSettings(self._handle)
            self._settings['synth.gain'] = 0.2
            self._synth = fluidsynth.FluidSynth(self._handle, self._settings)
            self._load_soundfont()
            self._settings['audio.driver'] = 'alsa'
            self._driver = fluidaudiodriver.FluidAudioDriver(self._handle, self._synth, self._settings)
        except (AttributeError, FluidError) as e:
            # rem: under Linux, AttributeError is raised when pyfluidsynth3 is
            # available but libfluidsynth1 is not.
            message = 'Failed to setup fluidsynth: ' + str(e) + '. Audio output will be disabled.'
            log.warning(message)
            log.debug(traceback.format_exc())
            raise SingleNoteAbcPlayerException(message)

        self._no_sound = False  # If we can reach that point without exception, we should have sound
        self.select_instrument(self._instrument)

    def _load_soundfont(self):
        """Look for a soundfont and load it into fluidsynth.

           Raises:
               SingleNoteAbcPlayerException: could not find a soundfont
        """
        soundfont_found = False
        for soundfont in soundfonts:
            try:
                self._synth.load_soundfont(soundfont)
                soundfont_found = True
                log.info('soundfont: loaded \'' + soundfont + '\'')
                break
            except FluidError:
                # rem: loading error logged by fluidsynth
                pass
        if not soundfont_found:
            message = 'No soundfont can be found. Audio output will be disabled.'
            log.warning(message)
            raise SingleNoteAbcPlayerException(message)

    def select_instrument(self, instrument_name):
        self._instrument = instrument_name
        self._midi_program = midi_programs[instrument_name]
        if self._no_sound:
            return
        self._synth.program_change(self._midi_channel, self._midi_program)

    def select_midi_channel(self, midi_channel):
        """Set the MIDI channel used by the SingleNoteAbcPlayer. Here channel numbering starts at 0,
        use 9 for percussions (channel 10)."""
        self._midi_channel = midi_channel
        if self._no_sound:
            return
        self._synth.program_change(self._midi_channel, self._midi_program)

    def play_midi_note(self, note_number):
        if self._no_sound:
            return
        try:
            self._lock.acquire()
            if self._midi_note is not None:
                self._synth.noteoff(self._midi_channel, self._midi_note)
                self._timer.cancel()

            self._midi_note = note_number
            self._synth.noteon(self._midi_channel, self._midi_note, self._velocity)
            self._timer = Timer(self._delay_s, self._on_timeout)
            self._timer.start()
        finally:
            self._lock.release()

    def play_abc_note(self, abc_note):
        self.play_midi_note(abc2midi.get_midi_note(abc_note))

    def _on_timeout(self):
        try:
            self._lock.acquire()
            self._synth.noteoff(self._midi_channel, self._midi_note)
            self._midi_note = None
        finally:
            self._lock.release()
