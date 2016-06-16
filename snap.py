#! /usr/bin/python3

from pyfluidsynth3 import fluidaudiodriver, fluidhandle, fluidsettings, fluidsynth
import time
from getch import getch
from threading import Timer, Lock


# midi utils

midi_programs = {
    'Acoustic Grand Piano': 0,
    'Accordion': 21,
    'Flute': 73,
    'Fiddle': 110
}


# abc2midi utils

c_major_scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
major_scale_intervals = [0, 2, 4, 5, 7, 9, 11]
c_major_scale_intervals = dict(zip(c_major_scale, major_scale_intervals))


def abc2midi_note(abc_note_string):
    """"Convert an ABC note to a midi number"""
    midi_c4_number = 60
    midi_note_number = midi_c4_number
    if abc_note_string.islower():
        midi_note_number += 12
        abc_note_string = abc_note_string.upper()
    midi_note_number += c_major_scale_intervals[abc_note_string]
    return midi_note_number


class SingleNoteAbcPlayer:
    def __init__(self):
        self.midi_note = None  # MIDI note number
        self.midi_channel = 0  # MIDI channel to play the note
        self.midi_program = midi_programs['Acoustic Grand Piano']
        self.velocity = 1.0    # MIDI note velocity
        self.delay_s = 0.5     # Note duration in seconds

        self.timer = None
        self.lock = Lock()
            # 'lock' protects:
            # - the instance variables used by on_timeout()
            # - libfluidsynth (in case it is not reentrant, which is unkown to me at the moment)

        self.setup_synth()

    def setup_synth(self):
        self.handle = fluidhandle.FluidHandle()
        self.settings = fluidsettings.FluidSettings(self.handle)
        self.settings['synth.gain'] = 0.2
        self.synth = fluidsynth.FluidSynth(self.handle, self.settings)
        self.synth.load_soundfont('/usr/share/sounds/sf2/FluidR3_GM.sf2')

        self.settings['audio.driver'] = 'alsa'
        self.driver = fluidaudiodriver.FluidAudioDriver(self.handle, self.synth, self.settings)

    def select_instrument(self, instrument_name):
        self.midi_program = midi_programs[instrument_name]
        self.synth.program_change(self.midi_channel, self.midi_program)

    def play_midi_note(self, note_number):
        try:
            self.lock.acquire()
            if self.midi_note is not None:
                self.synth.noteoff(self.midi_channel, self.midi_note)
                self.timer.cancel()

            self.midi_note = note_number
            self.synth.noteon(self.midi_channel, self.midi_note, self.velocity)
            self.timer = Timer(self.delay_s, self.on_timeout)
            self.timer.start()
        finally:
            self.lock.release()

    def play_abc_note(self, abc_note):
        self.play_midi_note(abc2midi_note(abc_note))

    def on_timeout(self):
        try:
            self.lock.acquire()
            self.synth.noteoff(self.midi_channel, self.midi_note)
            self.midi_note = None
        finally:
            self.lock.release()


def demo_play_interactive(instrument ='Acoustic Grand Piano'):
    synth = SingleNoteAbcPlayer()
    synth.select_instrument(instrument)
    print('Press a key for an ABC note from C to b... (Ctrl+C or q or Q to finish)')
    two_octaves_c_major_scale = c_major_scale + list(map(str.lower, c_major_scale))
    while True:
        key = getch()
        if key in ['\x03', 'q', 'Q']: # '\x03' = Ctrl+C
            break
        if key in two_octaves_c_major_scale:
            synth.play_abc_note(key)


def demo_play_tick():
    # !!! use 9 for channel 10 (perc)
    # Valeurs de 'note' qui pourraient le faire pour un tick métronome:
    # 37: stick
    # 42: Closed Hi-hat
    # 56: Cowbell
    # ~ 60-62
    # ~ 75-77
    synth = SingleNoteAbcPlayer()
    synth.midi_channel = 9
    for note in range(35, 82):
        print("playing note {} on channel 10 (perc)".format(note))
        synth.play_midi_note(note)
        time.sleep(0.5)


# Choose your demo:

demo_play_interactive()
#demo_play_interactive('Accordion')
#demo_play_tick()
