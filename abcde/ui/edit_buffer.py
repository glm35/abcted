#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter


class EditBuffer:
    """Provide an interface to the text in the edit zone so that the ABC
       parser code can interact with it without knowing it is handled by
       tkinter.

       This provides an abstraction that would make it easier
       to use the parser code in another application (eg EasyABC) or
       with another toolkit. In addition, it is more efficient than
       providing the whole buffer and cursor position to the parser.
    """

    def __init__(self, edit_zone):
        self._edit_zone = edit_zone

    def get_current_line_to_cursor(self):
        """Get the current line of text from the beginning of the line to the
        text cursor.

        :return: a string
        """
        insert_index = self._edit_zone.index(tkinter.INSERT)
        (cur_line, cur_col) = insert_index.split('.')
        line_start_index = '{}.{}'.format(cur_line, 0)
        return self._edit_zone.get(line_start_index, insert_index)

    def get_line(self, line_no):
        """
        Get a string with the contents of a given line.

        :param: line_no: Number of the desired line, starting at 1.

        :return: The line contents as a string.
        """

        # TODO: what if line_no is out of range?

        index_start = str(line_no) + ".0"
        index_end = str(line_no) + ".end"
        return self._edit_zone.get(index_start, index_end)

    def get_line_no_at_cursor(self):
        """Get the number of the line where the text cursor is.

        :return: The line number, starting at 1.
         """
        return int(self._edit_zone.index(tkinter.INSERT).split('.')[0])
