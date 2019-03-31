#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import tkinter as tk
import tkinter.font
from typing import Optional, Tuple, Union


class SearchBar:
    def __init__(self, container_frame: Union[tk.Tk, tk.Frame],
                 text_widget: tk.Text):
        self._container_frame: Union[tk.Tk, tk.Frame] = container_frame
        self._text: tk.Text = text_widget

        self._search_frame: Optional[tk.Frame] = None
        self._search_entry: Optional[tk.Entry] = None
        self._match_case: Optional[tk.Checkbutton] = None
        self._match_case_var: Optional[tk.IntVar] = None
        self._result_count_label: Optional[tk.Label] = None

        self._cur_match: Optional[Tuple[str, str]] = None
        self._cur_needle: str = ''
        self._resist_bottom: bool = True
        self._resist_top: bool = True

        self.match_color_fg = 'red'
        self.match_color_bg = 'yellow'

    def on_edit_search(self, event=None):
        """Create the search frame if it does not exist yet, else just focus
        """
        if self._search_frame is None:
            self._setup_search_bar()
        self._search_entry.focus()
        self._search_entry.select_range(0, tk.END)
        self._search_frame.grid(row=0, sticky=tk.E + tk.W)

    def _on_search_forward(self, event=None):
        self._search()

    def _on_search_backward(self, event=None):
        self._search(direction='backward')

    def _on_search_close(self, event=None):
        self._text.tag_remove('match', '1.0', tk.END)
        self._text.tag_remove('current_match', '1.0', tk.END)
        self._result_count_label.configure(text='')
        if self._cur_match is not None:
            # Set cursor position in the text widget at the end of the
            # current search term found:
            self._text.mark_set(tk.INSERT, self._cur_match[1])
            # Set the selection in the text widget to be the current search
            # term found:
            self._text.tag_remove(tk.SEL, '1.0', tk.END)
            self._text.tag_add(tk.SEL, *self._cur_match)
            # Forget current match:
            self._cur_match = None
        else:
            self._text.see(tk.INSERT)

        self._search_frame.grid_forget()
        self._text.focus()

    def _setup_search_bar(self):
        """Compose the search bar frame"""
        self._search_frame = tk.Frame(self._container_frame)

        # 1. Create the widgets
        needle_label = tk.Label(self._search_frame, text='Rechercher:')

        self._search_entry = tk.Entry(self._search_frame, width=25)

        next_button = tk.Button(self._search_frame, text='Suivant',
                                command=self._on_search_forward)
        next_button.bind('<Return>', self._on_search_forward)

        prev_button = tk.Button(self._search_frame, text='Précédent',
                                command=self._on_search_backward)
        prev_button.bind('<Return>', self._on_search_backward)

        self._match_case_var = tk.IntVar()
        self._match_case = tk.Checkbutton(self._search_frame,
                                    text='Respecter la casse',
                                    underline=13,
                                    padx=10,
                                    variable=self._match_case_var)

        self._result_count_label = tk.Label(self._search_frame, text='', padx=10)
        label_font = tk.font.nametofont(
            self._result_count_label.cget('font')).copy()
        label_font.configure(weight='bold')
        self._result_count_label.configure(font=label_font)

        close_button = tk.Button(self._search_frame, text='Fermer',
                                 command=self._on_search_close)
        close_button.bind('<Return>', self._on_search_close)

        # 2. Pack the widgets
        needle_label.pack(side=tk.LEFT, fill=tk.NONE)
        self._search_entry.pack(side=tk.LEFT)
        next_button.pack(side=tk.LEFT)
        prev_button.pack(side=tk.LEFT)
        self._match_case.pack(side=tk.LEFT)
        self._result_count_label.pack(side=tk.LEFT)

        close_button.pack(side=tk.RIGHT)

        # 3. Create keyboard shortcuts for some widgets

        self._search_entry.bind('<Return>', self._on_search_forward)
        self._search_entry.bind('<Control-A>', self._on_select_all_search_entry)
        self._search_entry.bind('<Control-a>', self._on_select_all_search_entry)

        # Close the search window with Escape key press:
        # (plus some other search bar level key bindings)
        #
        # Impractical to bind <Escape> to the frame because the event will only
        # trigger if the frame has focus, and by default a frame does not have the
        # keyboard focus.
        # (https://stackoverflow.com/questions/16923167/why-doesnt-the-bind-method-work-with-a-frame-widget-in-tkinter)
        #
        # Workaround: bind <Escape> to all the widgets of the search bar that
        # can have focus

        for w in self._search_entry, next_button, prev_button, \
                 self._match_case, close_button:
            w.bind('<Escape>', self._on_search_close)
            w.bind('<F3>', self._on_search_forward)
            w.bind('<Down>', self._on_search_forward)
            w.bind('<Up>', self._on_search_backward)
            w.bind('<Alt-c>', self._on_toggle_match_case)
            w.bind('<Alt-C>', self._on_toggle_match_case)

    def _on_select_all_search_entry(self, event=None):
        self._search_entry.select_range(0, tk.END)
        return 'break'

    def _on_toggle_match_case(self, event=None):
        self._match_case.toggle()
        return 'break'

    def _search(self, direction: str = 'forward') -> None:
        """
        Search the text widget

        Args:
            direction: 'forward' or 'backward'

        Returns:
            None
        """

        # Cleanup previous search:
        self._text.tag_remove('match', '1.0', tk.END)
        self._text.tag_remove('current_match', '1.0', tk.END)
        self._result_count_label.configure(text='')

        needle: str = self._search_entry.get()
        if needle != self._cur_needle:
            self._cur_needle = needle
            self._cur_match = None
            self._resist_bottom = True
            self._resist_top = True
        if needle == '':
            return  # Nothing to search

        # Look for all the needles, mark them with the 'match' tag, and
        # create the matches list
        matches = []  # list of tuples of index (start_pos, end_pos)
        start_pos = '1.0'
        while True:
            start_pos = self._text.search(pattern=needle,
                                          nocase=not self._match_case_var.get(),
                                          index=start_pos,
                                          stopindex=tk.END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(needle))
            matches.append((start_pos, end_pos))
            self._text.tag_add('match', start_pos, end_pos)
            start_pos = end_pos
        if len(matches) == 0:
            self._result_count_label.configure(text='Aucune occurence trouvée')
            return
        self._text.tag_config('match',
                              foreground=self.match_color_fg,
                              background=self.match_color_bg)

        # Update current match
        # (there should always be a current match)
        if direction == 'forward':
            self._resist_top = True
            for (start_pos, end_pos) in matches:
                if self._cur_match is None:
                    if self._text.compare(tk.INSERT, '<', end_pos):
                        self._cur_match = (start_pos, end_pos)
                        break
                elif self._text.compare(self._cur_match[1], '<=', start_pos):
                    self._cur_match = (start_pos, end_pos)
                    break
            else:
                # no break ie current match not found:
                # restart at top after a short resistance
                # (but no resistance if it is the first search)
                if self._resist_bottom and self._cur_match is not None:
                    self._resist_bottom = False
                else:
                    self._cur_match = matches[0]
                    self._resist_bottom = True
        else:  # 'backward'
            self._resist_bottom = True
            rmatches = list(reversed(matches))
            for (start_pos, end_pos) in rmatches:
                if self._cur_match is None:
                    if self._text.compare(tk.INSERT, '>=', start_pos):
                        self._cur_match = (start_pos, end_pos)
                        break
                elif self._text.compare(self._cur_match[0], '>', start_pos):
                    self._cur_match = (start_pos, end_pos)
                    break
            else:
                # no break ie current match not found:
                # restart at bottom after a short resistance
                # (but no resistance if it is the first search)
                if self._resist_top and self._cur_match is not None:
                    self._resist_top = False
                else:
                    self._cur_match = rmatches[0]
                    self._resist_top = True


        # Make sure the current match is visible
        self._text.see(self._cur_match[0])

        # Highlight the current match differently
        # from the other matches (as if it were selected)
        self._text.tag_remove('current_match', '1.0', tk.END)
        self._text.tag_add('current_match', *self._cur_match)
        self._text.tag_config('current_match',
                              foreground=self._text.tag_cget(tk.SEL,
                                                             'foreground'),
                              background=self._text.tag_cget(tk.SEL,
                                                             'background'))

        # Update the number of match found label
        match_no = matches.index(self._cur_match) + 1
        match_count = len(matches)
        self._result_count_label.configure(
            text=f'Occurence {match_no} sur {match_count}')
