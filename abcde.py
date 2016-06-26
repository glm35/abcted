#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import tkinter.font
import tkinter.scrolledtext


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


root = tkinter.Tk()
root.title("abcde")
#maximize_root_window(root)

theme = Theme()
edit_zone = tkinter.scrolledtext.ScrolledText(root, font=theme.get_font(),
                                              background=theme.bg, foreground=theme.fg,

                                              # Cursor configuration:
                                              insertbackground=theme.insertbg,
                                              #insertofftime=0, # Disable blinking
                                              #insertwidth=8, # Cursor width

                                              # Selection configuration:
                                              selectbackground=theme.selectbg)
edit_zone.pack(expand=tkinter.YES, fill=tkinter.BOTH)

root.mainloop()
