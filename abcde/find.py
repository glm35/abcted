#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk

# Basic find window
# Based on "Tkinter GUI Application Development Blueprint" p54


def find_text(root_window=None, text_widget=None):
    search_toplevel = tk.Toplevel(root_window)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root_window)

    tk.Label(search_toplevel, text="Find All:").grid(row=0, column=0,
                                                     sticky='e')

    search_entry_widget = tk.Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = tk.IntVar()
    tk.Checkbutton(
        search_toplevel, text='Ignore Case',
        variable=ignore_case_value
    ).grid(row=1, column=1, sticky='e', padx=2, pady=2)
    tk.Button(
        search_toplevel, text="Find All", underline=0,
        command=lambda: search_output(
            search_entry_widget.get(), ignore_case_value.get(),
            text_widget, search_toplevel,
            search_entry_widget)
    ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

    def close_search_window():
        text_widget.tag_remove('match', '1.0', tk.END)
        search_toplevel.destroy()

    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    return "break"


def search_output(needle, if_ignore_case, content_text,
                  search_toplevel, search_box):
    content_text.tag_remove('match', '1.0', tk.END)
    matches_found = 0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(needle, start_pos,
                                            nocase=if_ignore_case,
                                            stopindex=tk.END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(needle))
            content_text.tag_add('match', start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
        content_text.tag_config(
            'match', foreground='red', background='yellow')
    search_box.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))
