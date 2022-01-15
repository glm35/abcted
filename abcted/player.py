#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# PSL imports
import enum
import logging as log
from threading import Timer, Lock
import time
from typing import Optional
import traceback

# Third-party imports
from pyfluidsynth3 import fluidaudiodriver, fluidhandle, fluidsettings, fluidsynth
from pyfluidsynth3.fluiderror import FluidError
from pyfluidsynth3.fluidplayer import FluidPlayer, PlayerStatus, TempoType


# abcted imports
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


class Synth:
    def __init__(self, libfluidsynth_path: str = None):
        """Create a soundless player. This object cannot produce a sound (yet), but
           it can be used as a stub in soundless setups.
        """
        self._libfluidsynth_path = libfluidsynth_path

        self._instrument = 'Acoustic Grand Piano'
        self._midi_note = None  # MIDI note number
        self._midi_channel = 0  # MIDI channel to play the note
        self._midi_program = midi_programs[self._instrument]
        self._velocity = 1.0    # MIDI note velocity
        self._delay_s = 0.5     # Note duration in seconds

        self._timer = None

        # 'self._lock' protects:
        # - the instance variables used by _on_timeout()
        # - libfluidsynth (in case it is not reentrant, which is unknown to me at the moment)
        self._lock = Lock()

        self._no_sound = True

    def setup_synth(self):
        """Setup the synth so that it can produce sound.

           Raises:
               SingleNoteAbcPlayerException: an error occured during the synth setup.
                   Most common errors: fluidsynth library not found, soundfont not found.
        """
        try:
            if self._libfluidsynth_path is not None:
                log.info("Using libfluidsynth: " + self._libfluidsynth_path)
            self._fluidhandle = fluidhandle.FluidHandle(self._libfluidsynth_path)
            self._fluidsettings = fluidsettings.FluidSettings(self._fluidhandle)
            self._fluidsettings['synth.gain'] = 0.2
            self._fluidsynth = fluidsynth.FluidSynth(self._fluidhandle, self._fluidsettings)
            self._load_soundfont()
            self._fluidsettings['audio.driver'] = 'alsa'
            self._driver = fluidaudiodriver.FluidAudioDriver(self._fluidhandle,
                                                             self._fluidsynth, self._fluidsettings)
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
                self._fluidsynth.load_soundfont(soundfont)
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
        self._fluidsynth.program_change(self._midi_channel, self._midi_program)

    def select_midi_channel(self, midi_channel):
        """Set the MIDI channel used by the SingleNoteAbcPlayer. Here channel numbering starts at 0,
        use 9 for percussions (channel 10)."""
        self._midi_channel = midi_channel
        if self._no_sound:
            return
        self._fluidsynth.program_change(self._midi_channel, self._midi_program)

    def play_midi_note(self, note_number):
        if self._no_sound:
            return
        try:
            self._lock.acquire()
            if self._midi_note is not None:
                self._fluidsynth.noteoff(self._midi_channel, self._midi_note)
                self._timer.cancel()

            self._midi_note = note_number
            self._fluidsynth.noteon(self._midi_channel, self._midi_note, self._velocity)
            self._timer = Timer(self._delay_s, self._on_timeout)
            self._timer.start()
        finally:
            self._lock.release()

    def play_abc_note(self, abc_note):
        self.play_midi_note(abc2midi.get_midi_note(abc_note))

    def _on_timeout(self):
        try:
            self._lock.acquire()
            self._fluidsynth.noteoff(self._midi_channel, self._midi_note)
            self._midi_note = None
        finally:
            self._lock.release()

    def create_midi_player(self):
        return MidiPlayer(self)

    def create_fluid_player(self):
        return FluidPlayer(self._fluidhandle, self._fluidsynth)


class MidiPlayer:
    def __init__(self, synth: Synth):
        self._synth = synth
        self._fluidplayer = None
        self._paused = False  # Whether the player is paused (needed to detect end of playback)
        self._playlist = []

        self.repeat_count = 1

        # By default, use tempo from midi file or default fluidsynth tempo (120 bpm)
        self.tempo_bpm = None
        self.tempo_scale_factor = 1

    def __del__(self):
        if self._fluidplayer is not None:
            del self._fluidplayer

    # Playlist management

    def set_playlist(self, playlist):
        self._playlist = []
        for midi_file in playlist:
            log.debug("add midi file: " + midi_file)
            self._playlist.append(midi_file)

    def get_playlist(self):
        return list(self._playlist)

    # Playback control

    class Status(enum.Enum):
        STOPPED = 0
        PLAYING = 1
        PAUSED = 2

    def get_status(self):
        if self._fluidplayer is None:
            return self.Status.STOPPED
        elif self._paused:
            return self.Status.PAUSED
        else:
            return self.Status.PLAYING

    def play(self):
        """Start playing tunes in the playlist."""
        log.debug("start playing")

        # If playback is finished, need to stop first:
        if self._fluidplayer is not None and self._paused is False \
           and self._fluidplayer.get_status() == PlayerStatus.DONE:
            self.stop()

        if self._fluidplayer is None:
            self._fluidplayer = self._synth.create_fluid_player()
            self._fluidplayer.set_loop(self.repeat_count)
            self._set_tempo(bpm=self.tempo_bpm, scale_factor=self.tempo_scale_factor)

            for midi_file in self._playlist:
                self._fluidplayer.add(midi_file)

        self._fluidplayer.play()
        self._paused = False

    def pause(self):
        """Pause playback."""
        log.debug("pause playing")
        if self._fluidplayer is not None:
            self._fluidplayer.stop()  # fluid_player_stop() actually just pauses playback...
            self._paused = True

    def stop(self):
        """Stop playing."""
        log.debug("stop playing")
        if self._fluidplayer is not None:
            # No way to stop playback and resume at the beginning of the
            # playlist with fluidsynth, so we just delete the player.
            #
            # Before that we call stop(), else the last note will resonate for a while.
            # We need a short delay to let that happen before the player is
            # deleted.

            # Lazy protection against callbacks that might attempt to interact with the Player while
            # it is being stopped:
            death_sentenced_fluidplayer = self._fluidplayer
            self._fluidplayer = None
            self._paused = False

            death_sentenced_fluidplayer.stop()
            time.sleep(0.2)
            del death_sentenced_fluidplayer

    def get_ticks(self):
        if self._fluidplayer is None:
            return None, None
        current_tick = self._fluidplayer.get_current_tick()
        total_ticks = self._fluidplayer.get_total_ticks()
        return current_tick, total_ticks

    def seek(self, ticks: int):
        if self._fluidplayer is None:
            return
        self._fluidplayer.seek(ticks)

    # Loop control

    @property
    def repeat_count(self):
        return self._repeat_count

    @repeat_count.setter
    def repeat_count(self, count):
        if count == 0 or count < -1:
            raise ValueError("repeat count must be > 0 or equal to -1 (infinite)")
        log.debug(f"repeat_count={count}")
        self._repeat_count = count
        if self._fluidplayer is not None:
            self._fluidplayer.set_loop(self.repeat_count)

    # Tempo control

    @property
    def tempo_bpm(self):
        return self._tempo_bpm

    @tempo_bpm.setter
    def tempo_bpm(self, bpm: Optional[int]):
        if bpm is not None and bpm <= 0:
            raise ValueError
        self._tempo_bpm = bpm
        self._tempo_scale_factor = 1
        if self._tempo_bpm is not None:
            log.debug(f"set tempo bpm={bpm}")
            self._set_tempo(bpm=bpm)
        else:
            log.debug("reset tempo (bpm)")
            self._set_tempo(scale_factor=self._tempo_scale_factor)

    @property
    def tempo_scale_factor(self):
        return self._tempo_scale_factor

    @tempo_scale_factor.setter
    def tempo_scale_factor(self, scale_factor: Optional[float]):
        if scale_factor is not None and scale_factor <= 0:
            raise ValueError
        self._tempo_scale_factor = scale_factor
        self._tempo_bpm = None
        log.debug(f"set tempo scale factor={scale_factor}")
        self._set_tempo(scale_factor=self._tempo_scale_factor)

    def _set_tempo(self, bpm: Optional[int] = None, scale_factor: Optional[float] = None):
        if self._fluidplayer is None:
            return

        if bpm is not None:
            log.debug(f'set tempo (bpm): {bpm}')
            self._fluidplayer.set_tempo(TempoType.TEMPO_EXTERNAL_BPM, tempo=bpm)
        elif scale_factor is not None and scale_factor != 1:
            log.debug(f'set relative tempo: x{scale_factor}')
            self._fluidplayer.set_tempo(TempoType.TEMPO_INTERNAL, tempo=scale_factor)
        else:
            log.debug('reset tempo (use MIDI file tempo)')
            self._fluidplayer.set_tempo(TempoType.TEMPO_INTERNAL, tempo=1)

    def get_tempo(self):
        tempo_bpm, midi_tempo = None, None
        if self._fluidplayer is not None:
            tempo_bpm = self._fluidplayer.get_bpm()
            midi_tempo = self._fluidplayer.get_midi_tempo()
        return tempo_bpm, midi_tempo
