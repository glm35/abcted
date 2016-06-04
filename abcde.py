#! /usr/bin/python3

from pyfluidsynth3 import fluidaudiodriver, fluidhandle, fluidsettings, fluidsynth
import time

handle = fluidhandle.FluidHandle()
settings = fluidsettings.FluidSettings( handle )
synth = fluidsynth.FluidSynth( handle, settings )
synth.load_soundfont('/usr/share/sounds/sf2/FluidR3_GM.sf2')

settings['audio.driver'] = 'alsa'
driver = fluidaudiodriver.FluidAudioDriver( handle, synth, settings )

synth.noteon( 0, 79, 1.0 )
time.sleep( 1 )
synth.noteoff( 0, 79 )