#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
import pathlib
import tkinter as tk
import tkinter.messagebox as tk_messagebox

import file
import ui.edit_zone
import ui.theme


class RootWindow(tk.Tk):
    def __init__(self, filename=None):
        super().__init__()

        self._theme = ui.theme.Theme()
        self._edit_zone = ui.edit_zone.EditZone(self, self._theme)
        self._file = file.File(self, self._edit_zone._edit_zone)  # TODO: revoir les accesseurs
        self._file.set_root_title()
        self._edit_zone.set_check_text_change_since_last_save_cb(self._file.check_text_change_since_last_save)
        if filename:
            self._file.open(str(pathlib.Path(filename).absolute()))  # Make sure filename is absolute
            # TODO: use pathlib.Path.resolve() to remove possible '..'
            # This will check that the path exists, so 'FileNotFound' errors will have to be handled here...
            # unless we move this to _file.open()

            # TODO: si le fichier n'existe pas, créer un nouveau fichier avec ce nom
            #       plutôt que générer une erreur. C'est le comportement par défaut
            #       des éditeurs de texte (vim, xed)

        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='New', underline=0, accelerator='Ctrl + N', command=self._file.on_file_new)
        file_menu.add_command(label='Open...', underline=0, accelerator='Ctrl + O', command=self._file.on_file_open)
        file_menu.add_command(label='Save', underline=0, accelerator='Ctrl + S', command=self._file.on_file_save)
        file_menu.add_command(label='Save as...', underline=3, command=self._file.on_file_save_as)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', underline=0, accelerator='Alt + F4', command=self.exit)
        menu_bar.add_cascade(label='File', underline=0, menu=file_menu)

        self.config(menu=menu_bar)

        self.bind('<Control-N>', self._file.on_file_new)
        self.bind('<Control-n>', self._file.on_file_new)
        self.bind('<Control-O>', self._file.on_file_open)
        self.bind('<Control-o>', self._file.on_file_open)
        self.bind('<Control-S>', self._file.on_file_save)
        self.bind('<Control-s>', self._file.on_file_save)
        self.bind('Alt-Keypress-F4', self.exit)

        self.protocol('WM_DELETE_WINDOW', self.exit)

    def maximize(self):
        """Maximize the root window"""
        root_w, root_h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (root_w, root_h))

    def exit(self, event=None):
        log.debug('RootWindow.exit()')

        if self._file.ask_save_changes() == 'cancel':
            log.debug('RootWindow.exit(): ask save changes cancelled/failed, aborting')
            return 'break'
        elif tk_messagebox.askokcancel('Quit?', 'Really quit?'):
            self.destroy()
