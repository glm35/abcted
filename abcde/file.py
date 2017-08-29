#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manage ABC files: open, save, detect on-disk change, ...
"""

import logging as log
import tkinter as tk
import tkinter.filedialog as tk_filedialog
import tkinter.messagebox as tk_messagebox
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

    def _dump_edit_buffer(self, text=None, tag='text'):
        """Debug tool to print a text buffer and watch the ending line."""
        if text is None:
            text = self.buffer.get(1.0, tk.END)
        print('<{0}>{1}</{0}>'.format(tag, text))

    def check_text_change_since_last_save(self, update_ui=True):
        """Check whether the text in the edit zone has changed since the last time
           the buffer was saved. If so, update the ui.
        """
        old_modified_flag = self._modified_flag
        text = self.buffer.get(1.0, tk.END)

        if text != self._last_saved_text:
            self._modified_flag = True
        else:
            self._modified_flag = False
        if update_ui and old_modified_flag != self._modified_flag:
            self.set_root_title()
        return self._modified_flag

    def on_file_new(self, event=None):
        """'File => New' menu callback"""
        log.debug('File.on_file_new()')
        # TODO
        # TODO: si le fichier courant est modifié: proposer de le sauver
        return 'break'

    def set_root_title(self):
        """Set the title of the root window from the filename."""
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

    def on_file_open(self, event=None):
        """'File => Open...' menu callback"""
        # TODO: allow open from the CLI with a specified file
        log.debug('File.open(): entering')

        if self.ask_save_changes() == 'cancel':
            log.debug('File.open(): ask save changes cancelled/failed, leaving')
            return 'break'

        filename = tk_filedialog.askopenfilename(
            defaultextension='.abc',
            filetypes = [('ABC Files', '*.abc'), ('All Files', '*.*')])
        if not filename:
            log.debug('File.open(): no file selected, leaving')
            return 'break'

        log.debug('File.open(): opening: ' + filename)
        with open(filename, 'r') as file:
            try:
                text = file.read()
            except UnicodeDecodeError as e:
                log.debug('File.open(): caught exception UnicodeDecodeError: ' + str(e))
                text = None
                tk_messagebox.showerror('Open failed', 'Could not open ' + filename
                                        + ': it is not encoded in UTF-8.'
                                        + ' Please fix the encoding and retry.')
            # TODO: handle IO errors
        if text is None:
            log.debug('File.open(): read failed, leaving')
            return 'break'
        self.filename = filename

        # Replace the contents of the edit zone
        # with the contents of the file
        self.buffer.delete(1.0, tk.END)
        self.buffer.insert(1.0, text)
        self._update_last_saved_text(text)

        self.set_root_title()  # Must be done here after the reset of self._modified_flag

        # For some reason, tkinter adds a new empty line to the
        # edit zone. Carefully remove that spurious line, else the
        # 'text changed' flag computation will bug.
        (line, col) = tuple(map(int, self.buffer.index(tk.END).split('.')))
        if col == 0 and line > 2:
            last_line = self.buffer.get('{0}.{1}'.format(line-1, 0), '{0}.{1}'.format(line-1, 'end'))
            if last_line == '':
                self.buffer.delete('{0}.{1}'.format(int(line)-2, 'end'))

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

    def _save(self):
        """Save text to file.

        If no filename has been chosen yet, ask the user for one.

        Returns:
            bool: True if the text was saved, False if it was not whatever the reason
                (error, no filename specified, ...)
        """
        if self.filename is None:
            return self._save_as()
        else:
            if self._write_to_file() == True:
                self.set_root_title()
                return True
            else:
                return False

    def on_file_save(self, event=None):
        """'File => Save' menu callback"""
        self._save()
        return 'break'

    def _save_as(self):
        """Select filename then save text.

        Returns:
            bool: True if the text was saved, False if the user did not
                select any filename or if there was an error during the saving.
        """
        filename = tk_filedialog.asksaveasfilename(
            defaultextension='.abc',
            filetypes=[('ABC Files', '*.abc'), ('All Files', '*.*')])
        if filename:
            log.debug('Saving as: ' + filename)
            ret = self._write_to_file(filename)
            if ret == True:
                self.filename = filename
                self.set_root_title()
                return True
        return False

    def on_file_save_as(self, event=None):
        """'File => Save As...' menu callback"""
        self._save_as()
        return 'break'