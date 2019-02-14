#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import tkinter as tk
import tkinter.messagebox as tk_messagebox
import tkinter.scrolledtext as tk_scrolledtext

import abc2midi
import abcparser
import edit_zone_buffer
import snap
import theme


class EditZone():
    def __init__(self, tk_root: tk.Tk, theme: theme.Theme):
        self._theme = theme
        self._scrolled_text = tk_scrolledtext.ScrolledText(
            tk_root, font=theme.get_font(),
            background=theme.bg, foreground=theme.fg,

            # Cursor configuration:
            insertbackground=theme.insertbg,
            #insertofftime=0, # Disable blinking
            #insertwidth=8, # Cursor width

            # Selection configuration:
            selectbackground=theme.selectbg,

            # Enable undo
            undo=1
        )

        self._shift = False
        self._control = False
        self._alt = False

        self._scrolled_text.focus() # Set the focus on the edit zone

        self._scrolled_text.bind('<Key>', self._on_key_press)
        self._scrolled_text.bind('<KeyRelease>', self._on_key_release)

        self._scrolled_text.pack(expand=tk.YES, fill=tk.BOTH)

        self._buffer = edit_zone_buffer.EditZoneBuffer(self._scrolled_text)

        self._check_text_change_since_last_save_cb = None

        self._snap = snap.SingleNoteAbcPlayer()
        try:
            self._snap.setup_synth()
            self._snap.select_instrument('Acoustic Grand Piano')
        except snap.SingleNoteAbcPlayerException as e:
            # Under Windows, after we display a messagebox before the mainloop():
            # 1. the edit zone looses its focus (and it is difficult to get it back).
            # 2. the global keybindings do not work.
            #
            # Workaround : hide the root window before showing the messagebox
            tk_root.withdraw()
            tk_messagebox.showwarning(title='Erreur lors de l\'initialisation du synthétiseur', message=e)
            tk_root.deiconify()

    def get_buffer(self):
        return self._buffer

    def set_check_text_change_since_last_save_cb(self, callback):
        """Set the function that will be called whenever we decide
           it is time to check whether the edit zone text has changed since
           last save.
        """
        self._check_text_change_since_last_save_cb = callback

    def _on_key_press(self, event):
        logging.debug("key pressed: " + event.keysym)
        if event.keysym in ['Shift_R','Shift_L']:
            self._shift = True
        elif event.keysym in ['Control_L','Control_R']:
            self._control = True
        elif event.keysym in ['Alt_L']:
            self._alt = True
        elif not self._control and not self._alt:
            abc_note = abcparser.get_note_to_play(self._buffer, event.char)
            if abc_note is not None:
                self._snap.play_midi_note(abc2midi.get_midi_note(abc_note))

    def _on_key_release(self, event):
        logging.debug("key released: " + event.keysym)
        if event.keysym in ['Shift_R','Shift_L']:
            self._shift = False
        elif event.keysym in ['Control_L','Control_R']:
            self._control = False
        elif event.keysym in ['Alt_L']:
            self._alt = False

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
