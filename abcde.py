#! /usr/bin/python3

from pyfluidsynth3 import fluidaudiodriver, fluidhandle, fluidsettings, fluidsynth
import time
from getch import getch
from threading import Timer, Lock

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

def demo_play_single_note():
    synth.noteon(0, 79, 1.0)
    time.sleep(1)
    synth.noteoff(0, 79)

def demo_play_scale():
    for note in c_major_scale + list(map(str.lower, c_major_scale)):
        midi_note_number = abc2midi_note_number(note)
        synth.noteon(0, midi_note_number, 1.0)
        time.sleep(0.5)
        synth.noteoff(0, midi_note_number)

def demo_play_interactive():
    print('Press a key for an ABC note from C to b... (Ctrl+C to finish)')
    two_octaves_c_major_scale = c_major_scale + list(map(str.lower, c_major_scale))
    while True:
        key = getch()
        if key is '\x03': # Ctrl+C
            break
        if key in two_octaves_c_major_scale:
            midi_note_number = abc2midi_note_number(key)
            synth.noteon(0, midi_note_number, 1.0)
            time.sleep(0.5)
            synth.noteoff(0, midi_note_number)
    # Limite de cette approche:
    #       il faut attendre la fin d'une note pour pouvoir en jouer une autre
    #       effet secondaire quand ça arrive: la note est affichée dans le terminal et pas traitée par getch()


# Version 2 de demo_play_interactive(): utilisation de timers
# Q: est-ce que libfluidsynth est réentrant? et pyfluidsynth3?

current_midi_note_number = None
current_midi_channel = 0
current_timer = None

# 'lock' protects both:
# (1) the above global variables
#  and (2) libfluidsynth (in case it is not reentrant, which is unkown to me at the moment)
lock = Lock()


def on_timeout():
    global current_midi_note_number, current_midi_channel, lock

    try:
        lock.acquire()
        synth.noteoff(current_midi_channel, current_midi_note_number)
        current_midi_note_number = None
    finally:
        lock.release()


def play_note(channel, note_number, velocity, delay_s):
    global current_midi_note_number, current_midi_channel, current_timer, lock

    try:
        lock.acquire()
        if current_midi_note_number is not None:
            synth.noteoff(current_midi_channel, current_midi_note_number)
            current_timer.cancel()

        current_midi_channel = channel
        current_midi_note_number = note_number
        synth.noteon(current_midi_channel, current_midi_note_number, velocity)
        current_timer = Timer(delay_s, on_timeout)
        current_timer.start()
    finally:
        lock.release()


def demo_play_interactive_timer():
    print('Press a key for an ABC note from C to b... (Ctrl+C or q or Q to finish)')
    two_octaves_c_major_scale = c_major_scale + list(map(str.lower, c_major_scale))
    while True:
        key = getch()
        if key in ['\x03', 'q', 'Q']: # '\x03' = Ctrl+C
            break
        if key in two_octaves_c_major_scale:
            midi_note_number = abc2midi_note_number(key)
            play_note(0, midi_note_number, 1.0, 0.5)


def demo_play_tick():
    # !!! use 9 for channel 10 (perc)
    # Valeurs de 'note' qui pourraient le faire pour un tick métronome:
    # 37: stick
    # 42: Closed Hi-hat
    # 56: Cowbell
    # ~ 60-62
    # ~ 75-77
    for note in range(35, 82):
        print("playing note {} on channel 10 (perc)".format(note))
        play_note(9, note, 1.0, 0.5)
        time.sleep(0.5)

demo_play_tick()
exit()


#bank_no = 25
#res = synth.bank_select(0, bank_no)
#print("bank select: " + str(res))

midi_programs = {
    'Acoustic Grand Piano': 0,
    'Accordion': 21,
    'Flute': 73,
    'Fiddle': 110
}

program_no = midi_programs['Fiddle']
#program_no = midi_programs['Flute']
res = synth.program_change(0, program_no)
print("program change: channel={}, program={} -- res={}".format(0, program_no, res))


demo_play_interactive_timer()
