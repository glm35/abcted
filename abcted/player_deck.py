#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# PSL imports
import logging as log
import os
from threading import Timer
import tkinter as tk
from typing import Optional, Union

# abcted imports
import abc2midi
import abcparser
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
        self._timer = None  # 1s cyclic timer to update the get tempo label

    def __del__(self):
        if self._timer is not None:
            self._timer.cancel()  # TODO: also when hiding player deck
        del self._midi_player
        if self._midi_filename is not None:
            os.remove(self._midi_filename)  # TODO: fix segfault on exit
            self._midi_filename = None

    def on_open_deck(self, event=None):
        """Create the player frame if it does not exist yet, else update tune and focus
        """
        if self._player_frame is None:
            self._create_player_frame()
        self._play_button.focus()
        self._player_frame.grid(row=2, sticky=tk.E + tk.W)

        raw_tune = abcparser.get_current_raw_tune(self._edit_zone.get_buffer())
        log.debug("raw_tune: " + str(raw_tune))
        self._tune_title_label.config(text=abcparser.get_tune_title(raw_tune))
        # TODO: handle AbcParserException: notify user
        self._midi_filename = abc2midi.abc2midi(raw_tune)
        self._midi_player.set_playlist([self._midi_filename])
        # TODO: clean midi file when switching tune + stop playback if needed

    def _on_close_deck(self, event=None):
        self._midi_player.stop()
        self._player_frame.grid_forget()
        self._edit_zone.focus()

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
            w.bind('<Key-l>', self._on_toggle_loop)  # TODO
            w.bind('<Key-b>', self._on_focus_tempo_bpm_entry)
            w.bind('<Key-s>', self._on_focus_tempo_scale_factor_entry)
            w.bind('<Key-plus>', self._on_speed_up)  # TODO: speed up tempo +10%
            w.bind('<KP_Add>', self._on_speed_up)
            w.bind('<Key-minus>', self._on_slow_down)  # TODO: slow down tempo -10%
            w.bind('<KP_Subtract>', self._on_slow_down)
            w.bind('<Key-equal>', self._on_reset_tempo)

    def _create_playback_control_frame(self):
        frame = tk.Frame(self._player_frame)

        button_frame = tk.Frame(frame)
        self._stop_button = tk.Button(button_frame, text='Stop', command=self._midi_player.stop)
        self._stop_button.pack(side=tk.LEFT)
        self._pause_button = tk.Button(button_frame, text='Pause', command=self._midi_player.pause)
        self._pause_button.pack(side=tk.LEFT)
        self._play_button = tk.Button(button_frame, text='Play', command=self._play)
        self._play_button.pack(side=tk.LEFT)
        self._tune_title_label = tk.Label(button_frame, text="")
        self._tune_title_label.pack(side=tk.LEFT, fill=tk.X)
        self._close_button = tk.Button(button_frame, text='Close', command=self._on_close_deck)
        self._close_button.pack(side=tk.RIGHT)
        self._widgets += [self._stop_button, self._pause_button, self._play_button,
                          self._close_button]
        button_frame.pack(fill=tk.X)

        self._playback_position = tk.Label(frame, text="Playback position:")
        self._playback_position.pack(side=tk.LEFT, fill=tk.X)

        frame.pack(fill=tk.X)

    def _play(self):
        self._midi_player.play()
        if self._timer is None:
            self._timer = Timer(interval=1, function=self._timeout)
            self._timer.start()
        self._update_get_tempo_label()

    def _on_toggle_play_pause(self, event=None):
        player_status = self._midi_player.get_status()
        if player_status == player.MidiPlayer.Status.STOPPED or \
           player_status == player.MidiPlayer.Status.PAUSED:
            self._play()
        else:
            self._midi_player.pause()
        return 'break'

    def _on_stop_playback_or_close_deck(self, event=None):
        player_status = self._midi_player.get_status()
        if player_status == player.MidiPlayer.Status.PLAYING or \
           player_status == player.MidiPlayer.Status.PAUSED:
            self._midi_player.stop()
        else:
            self._on_close_deck()
        return 'break'

    def _update_playback_position(self):
        current, total = self._midi_player.get_ticks()
        self._playback_position.config(text=f"Playback position (ticks): {current}/{total}")

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
        pass

    def _on_repeat_entry_return_keypress(self, event=None):
        self._loop_value.set(self.REPEAT)
        self._loop_control()

    def _create_tempo_frame(self):
        self._tempo_frame = tk.Frame(self._player_frame)

        tk.Label(self._tempo_frame, text="Set tempo:").grid(row=1, columnspan=3, sticky=tk.W)

        tk.Label(self._tempo_frame, text="bpm:",
                 justify=tk.RIGHT).grid(row=2, column=0, sticky=tk.E)
        self._tempo_bpm_entry = tk.Entry(self._tempo_frame, width=5)
        self._tempo_bpm_entry.grid(row=2, column=1, sticky=tk.W)
        self._tempo_bpm_entry.bind("<Return>", self._on_set_tempo_bpm)
        self._tempo_bpm_entry.bind("<KP_Enter>", self._on_set_tempo_bpm)
        self._tempo_bpm_button = tk.Button(self._tempo_frame, text="Set tempo (bpm)",
                                           command=self._on_set_tempo_bpm)
        self._tempo_bpm_button.grid(row=2, column=2, sticky=tk.W)

        tk.Label(self._tempo_frame, text="Scale factor:").grid(row=4, sticky=tk.E)
        self._scale_factor_entry = tk.Entry(self._tempo_frame, width=8)
        self._scale_factor_entry.grid(row=4, column=1, sticky=tk.W)
        self._scale_factor_entry.bind("<Return>", self._on_set_tempo_scale_factor)
        self._scale_factor_entry.bind("<KP_Enter>", self._on_set_tempo_scale_factor)
        self._scale_tempo_button = tk.Button(self._tempo_frame, text="Speed up/slow down",
                                             command=self._on_set_tempo_scale_factor)
        self._scale_tempo_button.grid(row=4, column=2, sticky=tk.W)

        self._reset_tempo_button = tk.Button(self._tempo_frame,
                                             text="Reset tempo (use tempo from midi file)",
                                             command=self._on_reset_tempo)
        self._reset_tempo_button.grid(row=5, column=0, columnspan=3, sticky=tk.W+tk.E)

        self._get_tempo_label = tk.Label(self._tempo_frame, text="Get tempo:")
        self._get_tempo_label.grid(row=6, columnspan=3, sticky=tk.W)

        self._widgets += [self._tempo_bpm_button, self._tempo_bpm_button, self._scale_factor_entry,
                          self._scale_tempo_button, self._reset_tempo_button]

        self._tempo_frame.pack(side=tk.TOP, fill=tk.X)

    def _on_focus_tempo_bpm_entry(self, event=None):
        self._tempo_bpm_entry.focus()

    def _on_set_tempo_bpm(self, event=None):
        self._midi_player.tempo_bpm = int(self._tempo_bpm_entry.get())
        self._scale_factor_entry.delete(0, len(self._scale_factor_entry.get()))
        self._update_get_tempo_label()

    def _on_focus_tempo_scale_factor_entry(self, event=None):
        self._scale_factor_entry.focus()

    def _on_set_tempo_scale_factor(self, event=None):
        self._midi_player.tempo_scale_factor = float(self._scale_factor_entry.get())
        self._tempo_bpm_entry.delete(0, len(self._tempo_bpm_entry.get()))
        self._update_get_tempo_label()

    def _on_speed_up(self, event=None):
        pass

    def _on_slow_down(self, event=None):
        pass

    def _on_reset_tempo(self, event=None):
        self._tempo_bpm_entry.delete(0, len(self._tempo_bpm_entry.get()))
        self._scale_factor_entry.delete(0, len(self._scale_factor_entry.get()))
        self._midi_player.tempo_scale_factor = 1
        self._update_get_tempo_label()

    def _update_get_tempo_label(self):
        tempo_bpm, midi_tempo = self._midi_player.get_tempo()
        self._get_tempo_label.config(text=f"Get tempo: bpm={tempo_bpm}, MIDI tempo={midi_tempo}")

    def _timeout(self):
        self._update_playback_position()
        self._update_get_tempo_label()
        self._timer = Timer(interval=1, function=self._timeout)
        self._timer.start()
