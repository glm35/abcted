#! /usr/bin/python3

from pyfluidsynth3 import fluidaudiodriver, fluidhandle, fluidsettings, fluidsynth
import time

handle = fluidhandle.FluidHandle()
settings = fluidsettings.FluidSettings(handle)
settings['synth.gain'] = 0.2
synth = fluidsynth.FluidSynth(handle, settings)
synth.load_soundfont('/usr/share/sounds/sf2/FluidR3_GM.sf2')

settings['audio.driver'] = 'alsa'
driver = fluidaudiodriver.FluidAudioDriver(handle, synth, settings)

c_major_scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
major_scale_intervals = [0, 2, 4, 5, 7, 9, 11]
c_major_scale_intervals = dict(zip(c_major_scale, major_scale_intervals))

def abc2midi_note_number(abc_note_string):
    """"Convert an ABC note to a midi number"""
    midi_c4_number = 60
    midi_note_number = midi_c4_number
    if abc_note_string.islower():
        midi_note_number += 12
        abc_note_string = abc_note_string.upper()
    midi_note_number += c_major_scale_intervals[abc_note_string]
    return midi_note_number

#synth.noteon(0, 79, 1.0)
#time.sleep(1)
#synth.noteoff(0, 79)

for note in c_major_scale + list(map(str.lower, c_major_scale)):
    midi_note_number = abc2midi_note_number(note)
    synth.noteon(0, midi_note_number, 1.0)
    time.sleep(0.5)
    synth.noteoff(0, midi_note_number)
