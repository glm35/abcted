#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manage ABC files: open, save, detect on-disk change, ...
"""

import logging as log
import tkinter as tk
import tkinter.filedialog as tk_filedialog
import os


class File():
    def __init__(self, root, edit_zone):
        self._root = root
        self.buffer = edit_zone  # Text buffer to be saved in file (TODO encapsulate)
        self.filename = None

        self._last_saved_text = '\n'  # That's the contents of the empty edit zone
        self._modified_flag = False  # Whether buffer has been modified since last save

    def _update_last_saved_text(self, text):
        self._last_saved_text = text
        self._modified_flag = False

    def check_text_change_since_last_save(self, update_ui=True):
        """Check whether the text in the edit zone has changed since the last time
           the buffer was saved. If so, update the ui.
        """
        old_modified_flag = self._modified_flag
        text = self.buffer.get(1.0, tk.END)

        print('<text>' + text + '</text>')
        print('<last-saved-text>' + self._last_saved_text + '</last-saved-text>')

        if text != self._last_saved_text:
            self._modified_flag = True
        else:
            self._modified_flag = False
        if update_ui and old_modified_flag != self._modified_flag:
            self.set_root_title()
        return self._modified_flag

    def new(self, event=None):
        log.debug('File(): new()')
        return 'break'

    def set_root_title(self):
        """Set the title of the root window from the filename"""
        title = ''
        if self._modified_flag:
            title += '* '
        if self.filename is None:
            title += 'New ABC File.abc'
        else:
            # If possible, build a dir name relative to the user's home directory
            dirname = os.path.dirname(self.filename)
            home = os.path.expanduser('~')
            if dirname.startswith(home):
                dirname = '~' + dirname[len(home):]
            title += '{} ({})'.format(os.path.basename(self.filename), dirname)
        self._root.title(title)

    def open(self, event=None):
        log.debug('File(): open()')
        filename = tk_filedialog.askopenfilename(
            defaultextension='.abc',
            filetypes = [('ABC Files', '*.abc'), ('All Files', '*.*')])
        if filename:
            # TODO: si le fichier courant est modifié: proposer de le sauver
            log.debug('Opening: ' + filename)
            with open(filename, 'r') as file:
                self.filename = filename
                self.set_root_title()
                self.buffer.delete(1.0, tk.END)
                text = file.read()
                self.buffer.insert(1.0, text)
                # TODO: comprendre pourquoi insert() ajoute une ligne vide
                #       qui vient mettre le bazar dans la détection des modifications
                self._update_last_saved_text(text)
            # TODO: handle IO errors
        return 'break'

    def _write_to_file(self, filename=None):
        """Return True in case of success else False"""
        if filename is None:
            filename = self.filename
        return_status = True
        try:
            text = self.buffer.get(1.0, tk.END)
            with open(filename, 'w') as file:
                file.write(text)
                self._update_last_saved_text(text)
        except IOError:
            # TODO: handle IO errors
            return_status = False
        return return_status

    def save(self, event=None):
        log.debug("File(): save()")
        if self.filename is None:
            self.save_as()
        else:
            self._write_to_file()
            self.set_root_title()
        return 'break'

    def save_as(self, event=None):
        log.debug("File(): save_as()")
        # TODO: si le fichier courant est modifié: proposer de le sauver
        filename = tk_filedialog.asksaveasfilename(
            defaultextension='.abc',
            filetypes=[('ABC Files', '*.abc'), ('All Files', '*.*')])
        if filename:
            log.debug('Saving as: ' + filename)
            ret = self._write_to_file(filename)
            if ret == True:
                self.filename = filename
                self.set_root_title()
        return 'break'
