#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import tkinter.font
import tkinter.scrolledtext

import snap


class Theme():
    def __init__(self, theme = 'TedPy'):
        # The 'TedPy' theme:
        self.bg = '#222222'     # Background color
        self.fg = 'white'       # Foreground color
        self.insertbg = 'white' # Insertion cursor color
        self.selectbg = '#630'  # Select background color

        self.font_family = "courier new"
        self.font_size = 12

    def get_font(self):
        return tkinter.font.Font(family=self.font_family, size=self.font_size)


def maximize_root_window(root):
    """Maximize the root window"""
    root_w, root_h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (root_w, root_h))


class EditZone(tkinter.Frame):
    def __init__(self, frame, theme):
        self.theme = theme
        self.edit_zone = tkinter.scrolledtext.ScrolledText(
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

        self.edit_zone.bind('<Key>', self.on_key_press)
        self.edit_zone.bind('<KeyRelease>', self.on_key_release)

        self.edit_zone.pack(expand=tkinter.YES, fill=tkinter.BOTH)

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
        elif not self.control and not self.alt and \
                        event.keysym.upper() in snap.c_major_scale:
            self.snap.play_abc_note(event.keysym)

    def on_key_release(self, event):
        if event.keysym in ['Shift_R','Shift_L']:
            self.shift = False
        elif event.keysym in ['Control_L','Control_R']:
            self.control = False
        elif event.keysym in ['Alt_L']:
            self.alt = False


root = tkinter.Tk()
root.title("abcde")
#maximize_root_window(root)

theme = Theme()
edit_zone = EditZone(root, theme)

root.mainloop()
