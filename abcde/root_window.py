#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
import pathlib
import tkinter as tk
import tkinter.messagebox as tk_messagebox

import edit_zone
import file
import recent_files
import theme


class RootWindow():
    def __init__(self, filename=None):
        self.tk_root = tk.Tk()

        self._theme = theme.Theme()

        self._edit_zone = edit_zone.EditZone(self.tk_root, self._theme)

        self._file = file.File(self, self._edit_zone.get_buffer())
        self._file.set_root_window_title()
        self._edit_zone.set_check_text_change_since_last_save_cb(self._file.check_text_change_since_last_save)
        if filename:
            self._file.open(str(pathlib.Path(filename).absolute()))  # Make sure filename is absolute

        menu_bar = tk.Menu(self.tk_root)

        self._file_menu = tk.Menu(menu_bar, tearoff=0)
        self._file_menu.add_command(label='Nouveau', underline=0, accelerator='Ctrl + N', command=self._file.on_file_new)
        self._file_menu.add_command(label='Ouvrir...', underline=0, accelerator='Ctrl + O', command=self._file.on_file_open)
        self._file_menu.add_separator()
        self._favrecent_index_first = 3  # The first favorite file is at index 3
        self._favrecent_nb = 0
        self._build_fav_recent_menu_entries()
        recent_files.register_update_recent_files_cb(self._update_fav_recent_menu_entries)
        self._file_menu.add_separator()
        self._file_menu.add_command(label='Enregistrer', underline=0, accelerator='Ctrl + S', command=self._file.on_file_save)
        self._file_menu.add_command(label='Enregistrer sous...', underline=3, command=self._file.on_file_save_as)
        self._file_menu.add_separator()
        self._file_menu.add_command(label='Quitter', underline=0, accelerator='Alt + F4', command=self.exit)
        menu_bar.add_cascade(label='Fichier', underline=0, menu=self._file_menu)

        self.tk_root.config(menu=menu_bar)

        self.tk_root.bind('<Control-N>', self._file.on_file_new)
        self.tk_root.bind('<Control-n>', self._file.on_file_new)
        self.tk_root.bind('<Control-O>', self._file.on_file_open)
        self.tk_root.bind('<Control-o>', self._file.on_file_open)
        self.tk_root.bind('<Control-S>', self._file.on_file_save)
        self.tk_root.bind('<Control-s>', self._file.on_file_save)
        self.tk_root.bind('Alt-Keypress-F4', self.exit)

        self.tk_root.protocol('WM_DELETE_WINDOW', self.exit)

    def _build_fav_recent_menu_entries(self):
        for fav in recent_files.read_favorite_files():
            self._file_menu.insert_command(
                index=self._favrecent_index_first + self._favrecent_nb,
                label=file.prettify_filename(fav),
                command=lambda local_fav=fav: self._file.open(local_fav))
            self._favrecent_nb += 1
            # https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result
        self._file_menu.insert_separator(
            index=self._favrecent_index_first + self._favrecent_nb)
        self._favrecent_nb += 1
        for recent in recent_files.read_recent_files():
            self._file_menu.insert_command(
                index=self._favrecent_index_first + self._favrecent_nb,
                label=file.prettify_filename(recent),
                command=lambda local_recent=recent: self._file.open(local_recent))
            self._favrecent_nb += 1

    def _update_fav_recent_menu_entries(self):
        # Remove the favorite and recent menu entries
        while self._favrecent_nb > 0:
            self._file_menu.delete(self._favrecent_index_first)
            self._favrecent_nb -= 1
        # Re-create them
        self._build_fav_recent_menu_entries()

    def maximize(self):
        """Maximize the root window"""
        root_w, root_h = self.tk_root.winfo_screenwidth(), self.tk_root.winfo_screenheight()
        self.tk_root.geometry("%dx%d+0+0" % (root_w, root_h))

    def exit(self, event=None):
        log.debug('RootWindow.exit()')

        if self._file.ask_save_changes() == 'cancel':
            log.debug('RootWindow.exit(): ask save changes cancelled/failed, aborting')
            return 'break'
        else:
            self.tk_root.destroy()

    def set_title(self, filename, modified_flag):
        """Set the title of the root window

        The title shows the name of the file being edited, and a star '*'
        if the file has been modified in the editor since its last save on disk.

        Args:
            filename (str): string representation of the filename
            modified_flag (bool): whether the file has been modified

        Returns:
            None
        """

        modified_flag_str = '* ' if modified_flag else ''
        self.tk_root.title(modified_flag_str + filename)
