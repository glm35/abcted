#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox as tk_messagebox
import tkinter.scrolledtext as tk_scrolledtext

import abcparser
import abc2midi
import snap
import ui.edit_buffer


class EditZone(tk.Frame):  # TODO: pourquoi a-t-on besoin d'une Frame?
                           #  Pour une future barre de défilement horizontale?
    def __init__(self, root_window, theme):
        self.theme = theme
        # TODO: Renommer _edit_zone: ambigu car même nom que la classe qui l'héberge
        self._edit_zone = tk_scrolledtext.ScrolledText(
            root_window, font=theme.get_font(),
            background=theme.bg, foreground=theme.fg,

            # Cursor configuration:
            insertbackground=theme.insertbg,
            #insertofftime=0, # Disable blinking
            #insertwidth=8, # Cursor width

            # Selection configuration:
            selectbackground=theme.selectbg)

        self.shift = False
        self.control = False
        self.alt = False

        self._edit_zone.focus() # Set the focus on the edit zone

        self._edit_zone.bind('<Key>', self.on_key_press)
        self._edit_zone.bind('<KeyRelease>', self.on_key_release)

        self._edit_zone.pack(expand=tk.YES, fill=tk.BOTH)

        self.edit_buffer = ui.edit_buffer.EditBuffer(self._edit_zone)
        self.check_text_change_since_last_save_cb = None

        self.snap = snap.SingleNoteAbcPlayer()
        try:
            self.snap.setup_synth()
            self.snap.select_instrument('Acoustic Grand Piano')
        except snap.SingleNoteAbcPlayerException as e:
            # Under Windows, after we display a messagebox before the mainloop():
            # 1. the edit zone looses its focus (and it is difficult to get it back).
            # 2. the global keybindings do not work.
            #
            # Workaround : hide the root window before showing the messagebox
            root_window.withdraw()
            tk_messagebox.showwarning(title='Failed to setup synth', message=e)
            root_window.deiconify()

    def set_check_text_change_since_last_save_cb(self, callback):
        self.check_text_change_since_last_save_cb = callback

    def on_key_press(self, event):
        #print("key pressed: " + event.keysym)
        if event.keysym in ['Shift_R','Shift_L']:
            self.shift = True
        elif event.keysym in ['Control_L','Control_R']:
            self.control = True
        elif event.keysym in ['Alt_L']:
            self.alt = True
        elif not self.control and not self.alt:
            abc_note = abcparser.get_note_to_play(self.edit_buffer, event.char)
            if abc_note is not None:
                self.snap.play_midi_note(abc2midi.get_midi_note(abc_note))

    def on_key_release(self, event):
        if event.keysym in ['Shift_R','Shift_L']:
            self.shift = False
        elif event.keysym in ['Control_L','Control_R']:
            self.control = False
        elif event.keysym in ['Alt_L']:
            self.alt = False

        if self.check_text_change_since_last_save_cb:
            self.check_text_change_since_last_save_cb()
