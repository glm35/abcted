#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Translation from C into Python of the "music box" example from the
fluidsynth documentation:
http://fluidsynth.sourceforge.net/api/index.html#Sequencer
"""

# TODO: changement de tempo statique (conf initiale) et dynamique (en cours de jeu)
# TODO: code cleaning

# PSL imports
import argparse
import time

# Third-party imports
from pyfluidsynth3 import fluidaudiodriver, fluidevent, fluidhandle, \
    fluidsequencer, fluidsettings, fluidsynth, utility
from pyfluidsynth3.fluiderror import FluidError

from ctypes import CFUNCTYPE, c_uint, c_void_p
FLUID_EVENT_CALLBACK = CFUNCTYPE(None, c_uint, c_void_p, c_void_p, c_void_p)
# https://docs.python.org/3/library/ctypes.html#callback-functions

ARG = None  # program arguments

TPB = 240  # tick per beats = constant by convention in demo_music_box.py
DEFAULT_BPM = 120

###fluid_synth_t* synth;
###fluid_audio_driver_t* adriver;
###fluid_sequencer_t* sequencer;
###short synthSeqID, mySeqID;
###unsigned int now;
###unsigned int seqduration;

handle = None
synth = None
adriver = None
sequencer = None
synth_seq_id = None
my_seq_id = 0
seq_start = 0
seq_duration = 4 * TPB  # 4 beats in the sequence


###void createsynth()
###{
###    fluid_settings_t* settings;
###    settings = new_fluid_settings();
###    fluid_settings_setstr(settings, "synth.reverb.active", "yes");
###    fluid_settings_setstr(settings, "synth.chorus.active", "no");
###    synth = new_fluid_synth(settings);
###    adriver = new_fluid_audio_driver(settings, synth);
###    sequencer = new_fluid_sequencer2(0);
###
###    // register synth as first destination
###    synthSeqID = fluid_sequencer_register_fluidsynth(sequencer, synth);
###
###    // register myself as second destination
###    mySeqID = fluid_sequencer_register_client(sequencer, "me", seq_callback, NULL);
###
###    // the sequence duration, in ms
###    seqduration = 1000;
###}

def create_synth():
    global handle
    global synth
    global adriver
    global sequencer
    global synth_seq_id
    global my_seq_id
    global seq_duration

    handle = fluidhandle.FluidHandle()

    settings = fluidsettings.FluidSettings(handle)
    settings['synth.gain'] = 0.2
    settings['synth.reverb.active'] = 'yes'
    settings['synth.chorus.active'] = 'no'
    synth = fluidsynth.FluidSynth(handle, settings)
    settings['audio.driver'] = 'alsa'
    adriver = fluidaudiodriver.FluidAudioDriver(handle, synth, settings)

    sequencer = fluidsequencer.FluidSequencer(handle)
    # rem: the demo C code calls 'new_fluid_sequencer2(0)' while
    # the pyfluidsynth3 code calls new_fluid_sequencer()
    sequencer.ticks_per_beat = TPB
    sequencer.beats_per_minute = DEFAULT_BPM

    # register synth as first destination
    (synth_seq_id, name) = sequencer.add_synth(synth)

    # register myself as second destination
    my_seq_id = handle.fluid_sequencer_register_client(
        sequencer.seq, utility.fluidstring('me'), seq_callback, None)


###void deletesynth()
###{
###    delete_fluid_sequencer(sequencer);
###    delete_fluid_audio_driver(adriver);
###    delete_fluid_synth(synth);
###}

def delete_synth():
    global sequencer, adriver, synth

    handle.fluid_sequencer_unregister_client(sequencer.seq, my_seq_id)
        # Needed at least to avoid that seq_callback() gets called after the
        # sequencer is deleted.
    del sequencer
    del adriver
    del synth


###void loadsoundfont()
###{
###    int fluid_res;
###    // put your own path here
###    fluid_res = fluid_synth_sfload(synth, "Inside:VintageDreamsWaves-v2.sf2", 1);
###}

def load_soundfont():
    soundfont = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
    synth.load_soundfont(soundfont)


###void sendnoteon(int chan, short key, unsigned int date)
###{
###    int fluid_res;
###    fluid_event_t *evt = new_fluid_event();
###    fluid_event_set_source(evt, -1);
###    fluid_event_set_dest(evt, synthSeqID);
###    fluid_event_noteon(evt, chan, key, 127);
###    fluid_res = fluid_sequencer_send_at(sequencer, evt, date, 1);
###    delete_fluid_event(evt);
###}

def send_noteon(channel, key, date):
    event = fluidevent.FluidEvent(handle)
    event.source = -1
    event.dest = synth_seq_id
    event.noteon(channel, key, 127)
    sequencer.send(event, int(date), absolute=True)


###void schedule_next_callback()
###{
###    int fluid_res;
###    // I want to be called back before the end of the next sequence
###    unsigned int callbackdate = now + seqduration/2;
###    fluid_event_t *evt = new_fluid_event();
###    fluid_event_set_source(evt, -1);
###    fluid_event_set_dest(evt, mySeqID);
###    fluid_event_timer(evt, NULL);
###    fluid_res = fluid_sequencer_send_at(sequencer, evt, callbackdate, 1);
###    delete_fluid_event(evt);
###}

def schedule_next_callback():
    # I want to be called back before the end of the next sequence
    callback_date = int(seq_start + seq_duration / 2)
    event = fluidevent.FluidEvent(handle)
    event.source = -1
    event.dest = my_seq_id
    event.timer()
    sequencer.send(event, callback_date, absolute=True)


###void schedule_next_sequence() {
###    // Called more or less before each sequence start
###    // the next sequence start date
###    now = now + seqduration;
###
###    // the sequence to play
###
###    // the beat : 2 beats per sequence
###    sendnoteon(0, 60, now + seqduration/2);
###    sendnoteon(0, 60, now + seqduration);
###
###    // melody
###    sendnoteon(1, 45, now + seqduration/10);
###    sendnoteon(1, 50, now + 4*seqduration/10);
###    sendnoteon(1, 55, now + 8*seqduration/10);
###
###    // so that we are called back early enough to schedule the next sequence
###    schedule_next_callback();
###}

def schedule_next_sequence():
    global seq_start

    # Called more or less before each sequence start

    # the sequence to play

    # The strange sequence from the fluidsynth demo:
    # (rem: seq_duration = 1000)
    #
    ## the beat : 2 beats per sequence
    #send_noteon(0, 60, now + seq_duration / 2)
    #send_noteon(0, 60, now + seq_duration)
    #
    ## melody
    #send_noteon(1, 45, now + seq_duration/10)
    #send_noteon(1, 50, now + 4*seq_duration/10)
    #send_noteon(1, 55, now + 8*seq_duration/10)

    # something basic but more recognizable musically

    # the bass line (in ABC format: |: C2 G,2 :|)
    send_noteon(0, 60, seq_start)
    send_noteon(0, 55, seq_start + 2 * TPB)

    # the melody (in ABC format: |: c e g e :|)
    send_noteon(1, 72, seq_start)
    send_noteon(1, 76, seq_start + TPB)
    send_noteon(1, 79, seq_start + 2 * TPB)
    send_noteon(1, 76, seq_start + 3 * TPB)

    # so that we are called back early enough to schedule the next sequence
    schedule_next_callback()

    # the next sequence start date
    seq_start = seq_start + seq_duration


###/* sequencer callback */
###void seq_callback(unsigned int time, fluid_event_t* event, fluid_sequencer_t* seq, void* data) {
###    schedule_next_sequence();
###}

def py_seq_callback(time, event, seq, data):
    schedule_next_sequence()

seq_callback = FLUID_EVENT_CALLBACK(py_seq_callback)


# fluid_event_callback_t = CFUNCTYPE(None, c_uint, c_void_p, c_void_p, c_void_p)
# 1st arg = return type
# other args: params

###int main(void) {
###    createsynth();
###    loadsoundfont();
###
###    // initialize our absolute date
###    now = fluid_sequencer_get_tick(sequencer);
###    schedule_next_sequence();
###
###    sleep(100000);
###    deletesynth();
###    return 0;

def main():
    global seq_start

    create_synth()
    load_soundfont()

    if ARGS.bpm is not None:
        sequencer.beats_per_minute = ARGS.bpm
    else:
        sequencer.beats_per_minute = 90

    print("BPM: {0}".format(sequencer.beats_per_minute))
    if ARGS.debug:
        print("TPB: {0}".format(sequencer.ticks_per_beat))
        print("TPS: {0}".format(sequencer.ticks_per_second))

    # initialize our absolute date
    now = sequencer.ticks
    if ARGS.debug:
        print('<debug> Current tick:', now)
    seq_start = now + 10  # keep a small margin before the first note
    schedule_next_sequence()

    print('Playing...  Hit Ctrl+C to stop')
    try:
        time.sleep(100)
    except KeyboardInterrupt:
        pass
    delete_synth()  # seems needed to avoid segfault at the end


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug',
                        help='display debug messages',
                        action='store_true')
    parser.add_argument('-b', '--bpm', help='set beats per minute', type=int)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main()
