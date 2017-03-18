#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import tkinter.scrolledtext

import abcparser
import abc2midi
import snap
import ui.edit_buffer


class EditZone(tkinter.Frame):
    def __init__(self, frame, theme):
        self.theme = theme
        self._edit_zone = tkinter.scrolledtext.ScrolledText(
            frame, font=theme.get_font(),
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

        self._edit_zone.pack(expand=tkinter.YES, fill=tkinter.BOTH)

        self.edit_buffer = ui.edit_buffer.EditBuffer(self._edit_zone)

        self.snap = snap.SingleNoteAbcPlayer()
        self.snap.midi_channel = 1
        self.snap.select_instrument('Acoustic Grand Piano')

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
