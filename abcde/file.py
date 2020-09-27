#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manage ABC files: new, open, save, save as, add to/remove from favorites ...
"""

import logging as log
import tkinter as tk
import tkinter.filedialog as tk_filedialog
import tkinter.messagebox as tk_messagebox

from edit_zone_buffer import EditZoneBuffer
from file_utils import prettify_path, normalize_path
import recent_files


class File():
    def __init__(self, root_window, buffer: EditZoneBuffer):
        self._root_window = root_window
        self._buffer = buffer  # Text buffer to be saved in file (this is a EditZoneBuffer object)
        self._path = None  # Path of the file (absolute directory name + filename)

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
        text = self._buffer.get()

        if text != self._last_saved_text:
            self._modified_flag = True
        else:
            self._modified_flag = False
        if update_ui and old_modified_flag != self._modified_flag:
            self.set_root_window_title()
        return self._modified_flag

    def on_file_new(self, event=None):
        """'File => New' menu callback"""
        log.debug('File.on_file_new()')
        if self.ask_save_changes() == 'cancel':
            log.debug('File.on_file_new(): ask save changes cancelled/failed, leaving')
        else:
            self._path = None
            self._buffer.replace('\n')
            self._update_last_saved_text('\n')
            self.set_root_window_title()
        return 'break'

    def set_root_window_title(self):
        """Set the title of the root window from the file path."""
        if self._path is None:
            pretty_path = 'Nouveau fichier.abc'
        else:
            pretty_path = prettify_path(self._path)
        self._root_window.set_title(pretty_path, self._modified_flag)

    def ask_save_changes(self):
        """Propose to save the current text if it has changed.

        If the current text has changed and has never been saved, or if
        it has changed since last save, propose the user to save the text.

        If the user chooses to save the text, ask for a filename if there
        is no file path yet, then save the text.

        Returns:
            str: 'ok' or 'cancel'

            Returns 'ok' if the user chose to save the file or to discard
            the changes

            Returns 'cancel' if the user chose to cancel the
            current operation (open, new, ...)
        """
        if not self._modified_flag:
            return 'ok'

        ret = tk_messagebox.askyesnocancel(title='Modifications non enregistrées',
            message='Le texte ABC a été modifié et les changement n\'ont pas été enregistrés.'
                    ' Voulez-vous enregistrer les modifications?')
        if ret is None:  # cancel
            return 'cancel'
        elif ret == False:  # no
            return 'ok'
        else:  # yes (ret == True)
            if self._save() == True:
                return 'ok'
            else:  # Save failed or was cancelled by user
                return 'cancel'

    def open(self, raw_path):
        """Open a file given its path.

        In case the file cannot be opened, an error message box is displayed and that's it.

        Params:
            raw_path(str): file path + filename, not necessarily normalized
        """
        log.debug('File.open(): opening: ' + raw_path)
        path = normalize_path(raw_path)
        text = None
        try:
            with open(path, 'r') as file:
                try:
                    text = file.read()
                except UnicodeDecodeError as e:
                    log.debug('File.open(): caught exception UnicodeDecodeError: ' + str(e))
                    tk_messagebox.showerror('Erreur lors de l\'ouverture du fichier',
                                            'Impossible d\'ouvrir ' + path
                                            + ': il n\'est pas encodé en UTF-8.'
                                            + ' Veuillez corriger l\'encodage et réessayer.')
        except FileNotFoundError as e:
            log.debug('File.open(): caught exception ' + type(e).__name__ + ' : '+ str(e))
            tk_messagebox.showerror('Erreur lors de l\'ouverture du fichier',
                                    'Impossible d\'ouvrir ' + path + ': '
                                    + str(e))
            recent_files.remove_recent_file(path)
        except Exception as e:  # Catch-all handler for other file exceptions
            log.debug('File.open(): caught exception ' + type(e).__name__ + ' : '+ str(e))
            tk_messagebox.showerror('Erreur lors de l\'ouverture du fichier',
                                    'Impossible d\'ouvrir ' + path + ': ' + str(e))

        if text is None:
            log.debug('File.open(): read failed, leaving')
        else:
            self._path = path
            self._buffer.replace(text)
            self._update_last_saved_text(text)
            self.set_root_window_title()
            recent_files.promote_recent_file(path)

    def on_file_open(self, event=None, path=None):
        """'File => Open...' menu callback

        Args:
            event: event that caused the callback

            path: normalized path of the path of the file to open.  This is
              optional: if no path is provided, a box to select the file
              is presented to the user.

        """
        log.debug('File.on_file_open(): entering')

        if self.ask_save_changes() == 'cancel':
            log.debug('File.on_file_open(): ask save changes cancelled/failed, leaving')
            return 'break'

        raw_path = path
        if raw_path is None:
            raw_path = tk_filedialog.askopenfilename(  # raw_path is a 'str' object
                defaultextension='.abc',
                filetypes = [('Fichiers ABC', '*.abc'), ('Tous les fichiers', '*.*')],
                initialdir='.')  # Under Windows, the current dir is not the initial dir
            if not raw_path:
                log.debug('File.on_file_open(): no file selected, leaving')
                return 'break'

        self.open(raw_path)
        return 'break'

    #
    # Add/remove favorite file
    #

    def get_menu_state(self, menu_name):
        menu_state = tk.ACTIVE

        if menu_name == 'add_to_favorites':
            # Menu entry enabled if:
            # (1) there is an opened file with a name
            # and (2) it is not already listed in the favorites
            if self._path is None:
                menu_state = tk.DISABLED
            elif self._path in recent_files.favorite_files_list:
                menu_state = tk.DISABLED

        elif menu_name == 'remove_from_favorites':
            # Menu entry enabled if:
            # (1) there is an opened file with a name
            # and (2) it is already listed in the favorites
            if self._path is None:
                menu_state = tk.DISABLED
            elif self._path not in recent_files.favorite_files_list:
                menu_state = tk.DISABLED

        return menu_state

    def on_file_add_to_favorites(self, event=None):
        """'File => Add to favorites' menu callback"""
        log.debug('File.on_file_add_to_favorites(): entering')
        recent_files.add_to_favorites(self._path)
        return 'break'

    def on_file_remove_from_favorites(self, event=None):
        """'File => Remove from favorites' menu callback"""
        log.debug('File.on_file_remove_from_favorites(): entering')
        recent_files.remove_from_favorites(self._path)
        return 'break'

    #
    # Save file
    #

    def _write_to_file(self, path):
        """Write buffer contents to file.

        Args:
            path: normalized directory + filename of the file

        Returns:
            True if the write succeeds else False
        """
        return_status = True
        try:
            text = self._buffer.get()
            with open(path, 'w') as file:
                file.write(text)
            self._path = path
            self._update_last_saved_text(text)
            self.set_root_window_title()
            recent_files.promote_recent_file(path)
        except IOError as e:
            log.debug('File._write_to_file(): caught exception ' + type(e).__name__ + ' : '+ str(e))
            tk_messagebox.showerror('Erreur lors de l\'enregistrement du fichier',
                                    'Impossible d\'enregistrer ' + path + ': '
                                    + str(e))
            return_status = False
        return return_status

    def _save(self):
        """Save text to file.

        If no path (filename) has been chosen yet, ask the user for one.

        Returns:
            bool: True if the text was saved, False if it was not whatever the reason
                (error, no filename specified, ...)
        """
        if self._path is None:
            return self._save_as()
        else:
            return self._write_to_file(self._path)

    def on_file_save(self, event=None):
        """'File => Save' menu callback"""
        self._save()
        return 'break'

    def _save_as(self):
        """Select path (filename) then save text.

        Note: the tkinter.filedialog.asksaveasfilename dialog warns the user
            if he attempts to overwrite an already existing file.

        Returns:
            bool: True if the text was saved, False if the user did not
                select any filename or if there was an error during the saving.
        """
        raw_path = tk_filedialog.asksaveasfilename(
            defaultextension='.abc',
            filetypes=[('Fichiers ABC', '*.abc'), ('Tous les fichiers', '*.*')],
            initialdir='.')  # Under Windows, the current dir is not the initial dir
        if raw_path:
            path = normalize_path(raw_path)
            log.debug('Saving as: ' + path)
            return self._write_to_file(path)
        else:
            return False

    def on_file_save_as(self, event=None):
        """'File => Save As...' menu callback"""
        self._save_as()
        return 'break'
