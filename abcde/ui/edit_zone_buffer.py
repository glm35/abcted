#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk


class EditZoneBuffer:
    """Provide an interface to the text in the edit zone so that the ABC
       parser code can interact with it without knowing it is handled by
       tkinter.

       This provides an abstraction that would make it easier
       to use the parser code in another application (eg EasyABC) or
       with another toolkit. In addition, it is more efficient than
       providing the whole buffer and cursor position to the parser.
    """

    def __init__(self, scrolled_text):
        self._scrolled_text = scrolled_text  # This is a tkinter.scrolledtext.ScrolledText

    def get(self):
        """Get the whole buffer contents

        :return: a string
        """
        return self._scrolled_text.get(1.0, tk.END)

    def get_current_line_to_cursor(self):
        """Get the current line of text from the beginning of the line to the
        text cursor.

        :return: a string
        """
        insert_index = self._scrolled_text.index(tk.INSERT)
        (cur_line, cur_col) = insert_index.split('.')
        line_start_index = '{}.{}'.format(cur_line, 0)
        return self._scrolled_text.get(line_start_index, insert_index)

    def get_line(self, line_no):
        """
        Get a string with the contents of a given line.

        :param: line_no: Number of the desired line, starting at 1.

        :return: The line contents as a string. The empty string if line_no
                 is out of range (before the first line or after the last
                 line)
        """

        index_start = str(line_no) + ".0"
        index_end = str(line_no) + ".end"
        return self._scrolled_text.get(index_start, index_end)

    def get_line_no_at_cursor(self):
        """Get the number of the line where the text cursor is.

        :return: The line number, starting at 1.
         """
        return int(self._scrolled_text.index(tk.INSERT).split('.')[0])

    def dump(self, tag='---', text=None):
        """Debug tool to print the text buffer or an arbitrary text
           and watch the ending line."""
        if text is None:
            text = self._scrolled_text.get(1.0, tk.END)
        print('<{0}>{1}</{0}>'.format(tag, text))

    def replace(self, text: str):
        """Replace the contents of the buffer with the given text."""
        self._scrolled_text.delete(1.0, tk.END)
        self._scrolled_text.insert(1.0, text)

        # For some reason, tkinter adds a new empty line to the
        # edit zone. Carefully remove that spurious line, else the
        # 'text changed' flag computation in file.py will bug.
        (line, col) = tuple(map(int, self._scrolled_text.index(tk.END).split('.')))
        if col == 0 and line > 2:
            last_line = self._scrolled_text.get('{0}.{1}'.format(line - 1, 0), '{0}.{1}'.format(line - 1, 'end'))
            if last_line == '':
                self._scrolled_text.delete('{0}.{1}'.format(int(line) - 2, 'end'))
