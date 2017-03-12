#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
import tkinter.scrolledtext

import ui.edit_zone
import ui.theme


def maximize_root_window(root):
    """Maximize the root window"""
    root_w, root_h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (root_w, root_h))


def start_ui():
    root = tkinter.Tk()
    root.title("abcde")
    #maximize_root_window(root)

    theme = ui.theme.Theme()
    edit_zone = ui.edit_zone.EditZone(root, theme)

    root.mainloop()
