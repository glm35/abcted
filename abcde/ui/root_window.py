#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk

import ui.edit_zone
import ui.theme


class RootWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("abcde")
        self._theme = ui.theme.Theme()
        self._edit_zone = ui.edit_zone.EditZone(self, self._theme)

    def maximize(self):
        """Maximize the root window"""
        root_w, root_h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (root_w, root_h))
