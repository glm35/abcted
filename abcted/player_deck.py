#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# PSL imports
from copy import copy
import logging as log
import os
import tkinter as tk
import tkinter.ttk as ttk
from typing import Optional, Union

# abcted imports
import abc2midi
import abcparser
from abctempo import AbcTempo, default_abc_tempo
from edit_zone import EditZone
import player


class PlayerDeck:
    def __init__(self,
                 container_frame: Union[tk.Tk, tk.Frame],
                 edit_zone: EditZone,
                 synth: player.Synth):
        self._container_frame = container_frame
        self._edit_zone = edit_zone
        self._player_frame: Optional[tk.Frame] = None
        self._widgets = []  # play deck widgets that can have focus

        self._midi_player = synth.create_midi_player()
        self._midi_filename = None

        self._abc_tune = None
        self._abc_tempo: AbcTempo = None  # Keep track of the current tempo

        self._timer_id = None

    # ------------------------------------------------------------------------
    # Create/show player deck
    # ------------------------------------------------------------------------

    def on_open_deck(self, event=None):
        """Create the player frame if needed, show it and play current tune"""
        self._show_player_deck()

        # In case the user requests to open the deck while the deck is already
        # opened, take it as a "I want to play a new tune" or "I want to play
        # an updated version of the current tune": stop the current playback (no
        # effect if the playback is already stopped) and remove the midi file of
        # the old tune.
        self._stop()

        try:
            self._setup_tune()
        except abcparser.AbcParserException as e:
            log.error('ABC parser error: %s', e.msg)
            # TODO: notify user
            self._hide_player_deck()
            return

        self._play()

    def _show_player_deck(self):
        """Show player deck and focus on the play button"""
        if self._player_frame is None:
            self._create_player_frame()
        self._play_button.focus()
        self._player_frame.grid(row=2, sticky=tk.E + tk.W)

    def _create_player_frame(self):
        self._player_frame = tk.Frame(self._container_frame)
        self._create_playback_control_frame()
        self._create_loop_control_frame()
        self._create_tempo_frame()
        self._bind_player_deck_keys()

    def _bind_player_deck_keys(self):
        # Bind player deck keyboard shortcuts to all the widgets in the player
        # deck that can have focus.
        for w in self._widgets:
            w.bind('<Escape>', self._on_stop_playback_or_close_deck)
            w.bind('<Key-space>', self._on_toggle_play_pause)
            w.bind('<Key-l>', self._on_toggle_loop)
            w.bind('<Key-b>', self._on_focus_tempo_entry)
            w.bind('<Key-plus>', self._on_speed_up)
            w.bind('<KP_Add>', self._on_speed_up)
            w.bind('<Key-minus>', self._on_slow_down)
            w.bind('<KP_Subtract>', self._on_slow_down)
            w.bind('<Key-equal>', self._on_reset_tempo)
            w.bind('<Key-s>', self._on_set_slow_tempo)
            w.bind('<Key-m>', self._on_set_medium_tempo)
            w.bind('<Key-f>', self._on_set_fast_tempo)
        # TODO: bind enter key to all the buttons

    # ------------------------------------------------------------------------
    # Hide/close/destroy player deck
    # ------------------------------------------------------------------------

    def _hide_player_deck(self):
        self._player_frame.grid_forget()

    def _on_close_deck(self, event=None):
        """Stop playback, hide player deck and focus the edit zone"""
        self._stop()
        self._cleanup_tune()
        self._hide_player_deck()
        self._edit_zone.focus()

    def exit(self):
        """Stop playback and cleanup (for use on program exit)"""
        self._stop()
        self._cleanup_tune()
        del self._midi_player

    # ------------------------------------------------------------------------
    # Manage the tune to play
    # ------------------------------------------------------------------------

    def _setup_tune(self):
        """Create a MIDI file from the current ABC tune and pass it to the MIDI player"""

        # Cleanup if there is already a tune in the player deck
        self._cleanup_tune()

        # Get the current ABC tune, ie the tune at the cursor position in the edit zone
        raw_tune = abcparser.get_current_raw_tune(self._edit_zone.get_buffer())
        log.debug("raw_tune: " + str(raw_tune))

        # Parse the ABC tune, display its title on the player deck and its tempo
        # in the tempo entry
        self._abc_tune = abcparser.AbcParser(raw_tune)

        self._tune_title_label.config(text=self._abc_tune.title)

        self._reset_tempo()

        # Create a MIDI file from the ABC tune and give its name to the player
        self._midi_filename = abc2midi.abc2midi(raw_tune)
        self._midi_player.set_playlist([self._midi_filename])

    def _cleanup_tune(self):
        if self._midi_filename is not None:
            log.debug(f"remove MIDI file: {self._midi_filename}")
            os.remove(self._midi_filename)
            self._midi_filename = None
        self._abc_tune = None
        self._abc_tempo = None

    # ------------------------------------------------------------------------
    # Playback control: play, stop, pause
    # ------------------------------------------------------------------------

    def _create_playback_control_frame(self):
        frame = tk.Frame(self._player_frame)

        button_frame = tk.Frame(frame)
        self._stop_button = ttk.Button(button_frame, text='Stop', command=self._stop)
        self._stop_button.pack(side=tk.LEFT)
        self._pause_button = ttk.Button(button_frame, text='Pause', command=self._pause)
        self._pause_button.pack(side=tk.LEFT)
        self._play_button = ttk.Button(button_frame, text='Play', command=self._play)
        self._play_button.pack(side=tk.LEFT)
        self._tune_title_label = tk.Label(button_frame, text="")
        self._tune_title_label.pack(side=tk.LEFT, fill=tk.X)
        self._close_button = ttk.Button(button_frame, text='Close', command=self._on_close_deck)
        self._close_button.pack(side=tk.RIGHT)
        self._widgets += [self._stop_button, self._pause_button, self._play_button,
                          self._close_button]
        button_frame.pack(fill=tk.X)

        self._playback_position = tk.Label(frame, text="Playback position:")
        self._playback_position.pack(side=tk.LEFT, fill=tk.X)

        frame.pack(fill=tk.X)

        # TODO:
        # - when focus is on the edit zone and when click on the buttons: focus on the buttons?
        # - action the other buttons when called from keyboard shortcuts (same as mouse button)

    def _play(self):
        """Start playback"""
        self._stop_button.state(['!pressed'])
        self._pause_button.state(['!pressed'])
        self._play_button.state(['pressed'])

        self._midi_player.play()
        self._start_timer()

    def _pause(self):
        """Pause playback"""
        self._stop_button.state(['!pressed'])
        self._pause_button.state(['pressed'])
        self._play_button.state(['!pressed'])

        self._stop_timer()
        self._midi_player.pause()
        self._update_playback_position()

    def _stop(self):
        """Stop playback"""
        if self._player_frame is None:
            # The player frame has not been created so playback never started:
            # no need to stop, and bad things would happend if we tried to update
            # the player frame UI
            return

        self._stop_button.state(['pressed'])
        self._pause_button.state(['!pressed'])
        self._play_button.state(['!pressed'])

        self._stop_timer()
        self._midi_player.stop()

        self._update_playback_position()

    def _on_toggle_play_pause(self, event=None):
        player_status = self._midi_player.get_status()
        if player_status == player.MidiPlayer.Status.STOPPED or \
           player_status == player.MidiPlayer.Status.PAUSED:
            self._play()
        else:
            self._pause()
        return 'break'

    def _on_stop_playback_or_close_deck(self, event=None):
        player_status = self._midi_player.get_status()
        if player_status == player.MidiPlayer.Status.PLAYING or \
           player_status == player.MidiPlayer.Status.PAUSED:
            self._stop()
        else:
            self._on_close_deck()
        return 'break'

    def _update_playback_position(self):
        current, total = self._midi_player.get_ticks()
        self._playback_position.config(text=f"Playback position (ticks): {current}/{total}")

    # ------------------------------------------------------------------------
    # Playback loop/repeat control
    # ------------------------------------------------------------------------

    (NO_LOOP, LOOP_FOREVER, REPEAT) = (1, 2, 3)

    def _create_loop_control_frame(self):
        self._loop_control_frame = tk.Frame(self._player_frame)

        self._loop_value = tk.IntVar()
        self._loop_value.set(self.NO_LOOP)
        for txt, val in [("No Loop", self.NO_LOOP),
                         ("Loop Forever", self.LOOP_FOREVER),
                         ("Repeat", self.REPEAT)]:
            radio_button = tk.Radiobutton(self._loop_control_frame,
                                          text=txt, variable=self._loop_value, value=val,
                                          command=self._loop_control)
            self._widgets.append(radio_button)
            radio_button.pack(side=tk.LEFT)

        self._repeat_entry = tk.Entry(self._loop_control_frame, width=3)
        self._repeat_entry.insert(0, "3")  # repeat 3 times by default
        self._repeat_entry.bind("<Return>", self._on_repeat_entry_return_keypress)
        self._repeat_entry.bind("<KP_Enter>", self._on_repeat_entry_return_keypress)
        self._widgets.append(self._repeat_entry)
        self._repeat_entry.pack(side=tk.LEFT)
        tk.Label(self._loop_control_frame, text="times").pack(side=tk.LEFT)

        self._loop_control_frame.pack(side=tk.TOP, fill=tk.X)

    def _loop_control(self):
        loop_control_mode = self._loop_value.get()
        if loop_control_mode == self.NO_LOOP:
            self._midi_player.repeat_count = 1
        elif loop_control_mode == self.LOOP_FOREVER:
            self._midi_player.repeat_count = -1
        elif loop_control_mode == self.REPEAT:
            try:
                self._midi_player.repeat_count = int(self._repeat_entry.get())
            except ValueError:
                pass

    def _on_toggle_loop(self, event=None):
        loop_control_mode = self._loop_value.get() + 1
        if loop_control_mode > self.REPEAT:
            loop_control_mode = self.NO_LOOP
        self._loop_value.set(loop_control_mode)

        self._loop_control()

    def _on_repeat_entry_return_keypress(self, event=None):
        self._loop_value.set(self.REPEAT)
        self._loop_control()

    # ------------------------------------------------------------------------
    # Playback tempo control
    # ------------------------------------------------------------------------

    def _create_tempo_frame(self):
        self._tempo_frame = tk.Frame(self._player_frame)

        tk.Label(self._tempo_frame, text="Tempo:").grid(row=1, column=1, sticky=tk.W)

        self._tempo_entry = tk.Entry(self._tempo_frame, width=4)
        self._tempo_entry.bind("<Return>", self._on_set_tempo)
        self._tempo_entry.bind("<KP_Enter>", self._on_set_tempo)
        self._tempo_entry.grid(row=1, column=2, sticky=tk.W)

        tk.Label(self._tempo_frame, text="bpm",
                 justify=tk.RIGHT).grid(row=1, column=3, sticky=tk.W)

        self._tempo_button = tk.Button(self._tempo_frame, text="Set tempo",
                                       command=self._on_set_tempo)
        self._tempo_button.grid(row=1, column=4, sticky=tk.W)

        self._reset_tempo_button = tk.Button(self._tempo_frame, text="Reset tempo",
                                             command=self._on_reset_tempo)
        self._reset_tempo_button.grid(row=1, column=5, sticky=tk.W)

        tk.Label(self._tempo_frame, text="Set predefined tempo:").grid(row=1, column=6, sticky=tk.W)

        self._slow_tempo_button = ttk.Button(self._tempo_frame, text="Slow",
                                            command=self._on_set_slow_tempo)
        self._slow_tempo_button.grid(row=1, column=7, sticky=tk.W)

        self._medium_tempo_button = ttk.Button(self._tempo_frame, text="Medium",
                                            command=self._on_set_medium_tempo)
        self._medium_tempo_button.grid(row=1, column=8, sticky=tk.W)

        self._fast_tempo_button = ttk.Button(self._tempo_frame, text="Fast",
                                            command=self._on_set_fast_tempo)
        self._fast_tempo_button.grid(row=1, column=9, sticky=tk.W)

        self._widgets += [self._tempo_entry, self._tempo_button, self._reset_tempo_button,
                          self._slow_tempo_button, self._medium_tempo_button, self._fast_tempo_button]

        self._tempo_frame.pack(side=tk.TOP, fill=tk.X)

    def _on_focus_tempo_entry(self, event=None):
        self._tempo_entry.focus()

    def _on_set_tempo(self, event=None):
        try:
            bpm = int(self._tempo_entry.get())
        except ValueError:
            # Keep current tempo in case of invalid input
            bpm = self._abc_tempo.bpm
        self._set_tempo(bpm)
        self._press_tempo_button(None)

    def _on_speed_up(self, event=None):
        self._set_tempo(self._abc_tempo.bpm + 2)
        self._press_tempo_button(None)

    def _on_slow_down(self, event=None):
        self._set_tempo(self._abc_tempo.bpm - 2)
        self._press_tempo_button(None)

    def _set_tempo(self, bpm: int):
        if bpm < 1:
            bpm = 1
        elif bpm > 999:
            bpm = 999  # Arbitrary limit
        self._abc_tempo.bpm = bpm

        self._midi_player.tempo = self._abc_tempo.qpm

        self._tempo_entry.delete(0, tk.END)
        self._tempo_entry.insert(0, str(self._abc_tempo.bpm))

    def _reset_tempo(self):
        self._abc_tempo = copy(self._abc_tune.tempo)
        if self._abc_tempo is not None:
            self._set_tempo(self._abc_tempo.bpm)
            self._press_tempo_button(None)
        else:
            # The tempo is not specified in the ABC tune (or we failed to parse
            # it): set a default value depending on the tune rhythm.
            self._on_set_medium_tempo()

    def _on_reset_tempo(self, event=None):
        self._reset_tempo()

    def _on_set_slow_tempo(self, event=None):
        self._abc_tempo = default_abc_tempo(self._abc_tune.rhythm, "slow")
        self._set_tempo(self._abc_tempo.bpm)
        self._press_tempo_button("slow")

    def _on_set_medium_tempo(self, event=None):
        self._abc_tempo = default_abc_tempo(self._abc_tune.rhythm, "medium")
        self._set_tempo(self._abc_tempo.bpm)
        self._press_tempo_button("medium")

    def _on_set_fast_tempo(self, event=None):
        self._abc_tempo = default_abc_tempo(self._abc_tune.rhythm, "fast")
        self._set_tempo(self._abc_tempo.bpm)
        self._press_tempo_button("fast")

    def _press_tempo_button(self, speed: Optional[str]):
        speed_to_button = {
            "slow": self._slow_tempo_button,
            "medium": self._medium_tempo_button,
            "fast": self._fast_tempo_button,
        }
        for button in speed_to_button.values():
            button.state(['!pressed'])
        if speed is not None:
            speed_to_button[speed].state(['pressed'])


    # ------------------------------------------------------------------------
    # GUI periodic update every second
    #
    # We use tkinter universal widget method "after()" so that the callback gets
    # called in the context of the main thread: no risk of race conditions.
    # ------------------------------------------------------------------------

    def _start_timer(self):
        """Start the timer if it is not already running"""
        if self._timer_id is None:
            self._timer_id = self._player_frame.after(1000, self._timeout)

    def _stop_timer(self):
        """Stop the timer if it is running"""
        if self._timer_id is not None:
            self._player_frame.after_cancel(self._timer_id)
            self._timer_id = None

    def _timeout(self):
        """Update UI and restart timer unless it has been stopped"""
        self._update_playback_position()
        if self._timer_id is not None:
            self._timer_id = self._player_frame.after(1000, self._timeout)
