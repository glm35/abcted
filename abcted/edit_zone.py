#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
import tkinter as tk
import tkinter.scrolledtext as tk_scrolledtext

import abc2midi
import abcparser
import edit_zone_buffer
from player import Synth, SingleNoteAbcPlayerException
import theme


class EditZone():
    def __init__(self, tk_root: tk.Tk, theme: theme.Theme, synth: Synth):
        self._theme = theme
        self._synth = synth

        self._scrolled_text = tk_scrolledtext.ScrolledText(
            tk_root, font=theme.get_font(),
            background=theme.bg, foreground=theme.fg,

            # Cursor configuration:
            # insertforeground=theme.insertfg, # does not exist
            insertbackground=theme.insertbg,
            #insertofftime=0, # Disable blinking
            #insertwidth=8, # Cursor width

            # Selection configuration:
            selectforeground=theme.selectfg,
            selectbackground=theme.selectbg,

            # Enable undo
            undo=1
        )

        self._scrolled_text.focus()  # Set focus on text area

        self._scrolled_text.bind('<Key>', self._on_key_press)
        self._scrolled_text.bind('<KeyRelease>', self._on_key_release)

        self._scrolled_text.grid(row=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self._buffer = edit_zone_buffer.EditZoneBuffer(self._scrolled_text)

        self._check_text_change_since_last_save_cb = None

    def get_buffer(self):
        return self._buffer

    def focus(self):
        self._scrolled_text.focus()

    def set_check_text_change_since_last_save_cb(self, callback):
        """Set the function that will be called whenever we decide
           it is time to check whether the edit zone text has changed since
           last save.
        """
        self._check_text_change_since_last_save_cb = callback

    def _on_key_press(self, event):
        """
        When an ABC note is input, play that note in order to get a musical
        feedback.

        Args:
            event: KeyPress event

        Returns:
            None
        """
        log.debug('key pressed: ' + event.keysym)
        log.debug('modifier keys: 0x%04x', event.state)
        ctrl_alt_modifiers = 0x0004 | 0x0008 | 0x0080
        if event.state & ctrl_alt_modifiers == 0:
            # Key press without Ctrl/Left Alt/Right Alt modifiers
            # (rem: when a single Ctrl/Alt modifier key is pressed,
            # event.state does not include that key; but we do not care)
            abc_note = abcparser.get_note_to_play(self._buffer, event.char)
            if abc_note is not None:
                self._synth.play_midi_note(abc2midi.get_midi_note(abc_note))

    def _on_key_release(self, event):
        if self._check_text_change_since_last_save_cb:
            self._check_text_change_since_last_save_cb()

    def on_edit_cut(self, event=None):
        self._scrolled_text.event_generate("<<Cut>>")
        return "break"

    def on_edit_copy(self, event=None):
        self._scrolled_text.event_generate("<<Copy>>")
        return "break"

    def on_edit_paste(self, event=None):
        self._scrolled_text.event_generate("<<Paste>>")
        return "break"

    def on_edit_undo(self, event=None):
        self._scrolled_text.event_generate("<<Undo>>")
        return "break"

    def on_edit_redo(self, event=None):
        self._scrolled_text.event_generate("<<Redo>>")
        return "break"

    def on_edit_select_all(self, event=None):
        self._scrolled_text.tag_add('sel', '1.0', 'end')
        return "break"
