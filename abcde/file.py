#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manage ABC files: open, save, detect on-disk change, ...
"""

import logging as log
import tkinter.filedialog as tk_filedialog
import tkinter.messagebox as tk_messagebox
import os

from edit_zone_buffer import EditZoneBuffer


class File():
    def __init__(self, root_window, buffer: EditZoneBuffer):
        self._root_window = root_window
        self._buffer = buffer  # Text buffer to be saved in file (this is a EditZoneBuffer object)
        self._filename = None  # Absolute file name (absolute path + file name)

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

    def _reset_with_new_text(self, text, filename=None):
        """Setup the text buffer with new text data and a new filename."""
        self._filename = filename

        # Replace the contents of the edit zone with the contents of the file
        self._buffer.replace(text)
        self._update_last_saved_text(text)

        self.set_root_window_title()  # Must be done here after the reset of self._modified_flag

    def on_file_new(self, event=None):
        """'File => New' menu callback"""
        log.debug('File.on_file_new()')
        if self.ask_save_changes() == 'cancel':
            log.debug('File.on_file_new(): ask save changes cancelled/failed, leaving')
        else:
            self._reset_with_new_text(text='\n', filename=None)  # '\n' will be removed by _reset_with_new_text()
        return 'break'

    def set_root_window_title(self):
        """Set the title of the root window from the filename."""
        if self._filename is None:
            filename = 'New ABC File.abc'
        else:
            # If possible, build a dir name relative to the user's home directory
            dirname = os.path.dirname(self._filename)
            home = os.path.expanduser('~')
            if dirname.startswith(home):
                dirname = '~' + dirname[len(home):]
            filename = '{} ({})'.format(os.path.basename(self._filename), dirname)
        self._root_window.set_title(filename, self._modified_flag)

    def ask_save_changes(self):
        """Propose to save the current text if it has changed.

        If the current text has changed and has never been saved, or if
        it has changed since last save, propose the user to save the text.

        If the user chooses to save the text, ask for a filename if there
        is no filename yet, then save the text.

        Returns:
            str: 'ok' or 'cancel'

            Returns 'ok' if the user choosed to save the file or to discard
            the changes

            Returns 'cancel' if the user choosed to cancel the
            current operation (open, new, ...)
        """
        if not self._modified_flag:
            return 'ok'

        ret = tk_messagebox.askyesnocancel(
            title='Unsaved changes',
            message='The ABC text has been modified and the changes have not been saved.'
                    ' Would you like to save the text?')
        if ret is None:  # cancel
            return 'cancel'
        elif ret == False:  # no
            return 'ok'
        else:  # yes (ret == True)
            if self._save() == True:
                return 'ok'
            else:  # Save failed or was cancelled by user
                return 'cancel'

    def open(self, filename):
        """Open a file given its filename.

        In case the file cannot be opened, an error message box is displayed and that's it.

        Params:
            filename(str): absolute path + filename
        """
        log.debug('File.open(): opening: ' + filename)
        text = None
        try:
            with open(filename, 'r') as file:
                try:
                    text = file.read()
                except UnicodeDecodeError as e:
                    log.debug('File.open(): caught exception UnicodeDecodeError: ' + str(e))
                    tk_messagebox.showerror('Open failed', 'Could not open ' + filename
                                            + ': it is not encoded in UTF-8.'
                                            + ' Please fix the encoding and retry.')
        except FileNotFoundError as e:
            log.debug('File.open(): caught exception ' + type(e).__name__ + ' : '+ str(e))
            tk_messagebox.showerror('Open failed', 'Could not open ' + filename + ': '
                                    + str(e))
        except Exception as e:  # Catch-all handler for other file exceptions
            log.debug('File.open(): caught exception ' + type(e).__name__ + ' : '+ str(e))
            tk_messagebox.showerror('Open failed', 'Could not open ' + filename + ': '
                                    + str(e))

        if text is None:
            log.debug('File.open(): read failed, leaving')
        else:
            self._reset_with_new_text(text=text, filename=filename)

    def on_file_open(self, event=None):
        """'File => Open...' menu callback"""
        log.debug('File.on_file_open(): entering')

        if self.ask_save_changes() == 'cancel':
            log.debug('File.on_file_open(): ask save changes cancelled/failed, leaving')
            return 'break'

        filename = tk_filedialog.askopenfilename(  # filename is a 'str' object
            defaultextension='.abc',
            filetypes = [('ABC Files', '*.abc'), ('All Files', '*.*')],
            initialdir='.')  # Under Windows, the current dir is not the initial dir
        if not filename:
            log.debug('File.on_file_open(): no file selected, leaving')
            return 'break'

        self.open(filename)
        return 'break'

    def _write_to_file(self, filename=None):
        """Return True in case of success else False"""
        if filename is None:
            filename = self._filename
        return_status = True
        try:
            text = self._buffer.get()
            with open(filename, 'w') as file:
                file.write(text)
                self._update_last_saved_text(text)
        except IOError as e:
            log.debug('File._write_to_file(): caught exception ' + type(e).__name__ + ' : '+ str(e))
            tk_messagebox.showerror('Write failed', 'Could not write to ' + filename + ': '
                                    + str(e))
            return_status = False
        return return_status

    def _save(self):
        """Save text to file.

        If no filename has been chosen yet, ask the user for one.

        Returns:
            bool: True if the text was saved, False if it was not whatever the reason
                (error, no filename specified, ...)
        """
        if self._filename is None:
            return self._save_as()
        else:
            if self._write_to_file() == True:
                self.set_root_window_title()
                return True
            else:
                return False

    def on_file_save(self, event=None):
        """'File => Save' menu callback"""
        self._save()
        return 'break'

    def _save_as(self):
        """Select filename then save text.

        Note: the tkinter.filedialog.asksaveasfilename dialog warns the user
            if he attempts to overwrite an already existing file.

        Returns:
            bool: True if the text was saved, False if the user did not
                select any filename or if there was an error during the saving.
        """
        filename = tk_filedialog.asksaveasfilename(
            defaultextension='.abc',
            filetypes=[('ABC Files', '*.abc'), ('All Files', '*.*')],
            initialdir='.')  # Under Windows, the current dir is not the initial dir
        if filename:
            log.debug('Saving as: ' + filename)
            ret = self._write_to_file(filename)
            if ret == True:
                self._filename = filename
                self.set_root_window_title()
                return True
        return False

    def on_file_save_as(self, event=None):
        """'File => Save As...' menu callback"""
        self._save_as()
        return 'break'
