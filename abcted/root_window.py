#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
import tkinter as tk
import tkinter.messagebox as tk_messagebox
from typing import Optional
import os

import edit_zone
import file
import file_utils
import player
import player_deck
import recent_files
import search_bar
import theme


def get_star_image():
    starpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'icons', 'star.png')
    # https://stackoverflow.com/questions/50499/how-do-i-get-the-path-and-name-of-the-file-that-is-currently-executing
    star = tk.PhotoImage(file=starpath)
    return star


class RootWindow():
    def __init__(self, raw_path=None, libfluidsynth_path=None):
        self.tk_root = tk.Tk()

        self._theme = theme.Theme()

        self._setup_synth(libfluidsynth_path)

        self._edit_zone = edit_zone.EditZone(self.tk_root, self._theme, self._synth)

        self._player_deck = player_deck.PlayerDeck(self.tk_root, self._edit_zone, self._synth)

        self._search_bar = search_bar.SearchBar(self.tk_root, self._edit_zone._scrolled_text)
        self._search_bar.match_color_bg = self._theme.hlsearchbg
        self._search_bar.match_color_fg = self._theme.hlsearchfg

        # Allow text cell to grow when more space is available
        self.tk_root.columnconfigure(0, weight=1)
        self.tk_root.rowconfigure(1, weight=1)   # edit zone

        self._file = file.File(self, self._edit_zone.get_buffer())
        self._file.set_root_window_title()
        self._edit_zone.set_check_text_change_since_last_save_cb(
            self._file.check_text_change_since_last_save)
        if raw_path:
            self._file.open(raw_path)

        # ---------------------------------------------------------------------
        #     Menu bar
        # ---------------------------------------------------------------------

        menu_bar = tk.Menu(self.tk_root)

        # ---- File menu

        self._file_menu = tk.Menu(menu_bar, tearoff=0)
        self._file_menu.add_command(label='Nouveau', underline=0,
                                    accelerator='Ctrl+N',
                                    command=self._file.on_file_new)
        self._file_menu.add_command(label='Ouvrir...', underline=0,
                                    accelerator='Ctrl+O',
                                    command=self._file.on_file_open)
        self._file_menu.add_separator()
        self._favrecent_index_first = 3  # The first favorite file is at index 3
        self._favrecent_nb = 0
        self._icon_star = get_star_image()
        self._build_fav_recent_menu_entries()
        recent_files.register_update_recent_files_cb(self._update_fav_recent_menu_entries)
        self._file_menu.add_separator()
        self._file_menu.add_command(label='Enregistrer', underline=0,
                                    accelerator='Ctrl+S',
                                    command=self._file.on_file_save)
        self._file_menu.add_command(label='Enregistrer sous...', underline=3,
                                    command=self._file.on_file_save_as)
        self._file_menu.add_separator()
        self._file_menu.add_command(label='Quitter', underline=0,
                                    accelerator='Alt+F4', command=self.exit)
        menu_bar.add_cascade(label='Fichier', underline=0, menu=self._file_menu)

        # ---- Edit menu

        self._edit_menu = tk.Menu(menu_bar, tearoff=0)
        self._edit_menu.add_command(label='Annuler', underline=4,
                                    accelerator='Ctrl+Z',
                                    command=self._edit_zone.on_edit_undo)
        self._edit_menu.add_command(label='Rétablir', underline=0,
                                    accelerator='Ctrl+Y',
                                    command=self._edit_zone.on_edit_redo)
        self._edit_menu.add_separator()
        self._edit_menu.add_command(label='Couper', underline=0,
                                    accelerator='Ctrl+X',
                                    command=self._edit_zone.on_edit_cut)
        self._edit_menu.add_command(label='Copier', underline=1,
                                    accelerator='Ctrl+C',
                                    command=self._edit_zone.on_edit_copy)
        self._edit_menu.add_command(label='Coller', underline=0,
                                    accelerator='Ctrl+V',
                                    command=self._edit_zone.on_edit_paste)
        self._edit_menu.add_command(label='Tout sélectionner', underline=0,
                                    accelerator='Ctrl+A',
                                    command=self._edit_zone.on_edit_select_all)
        self._edit_menu.add_separator()
        self._edit_menu.add_command(label='Rechercher...', underline=0,
                                    accelerator='Ctrl+F',
                                    command=self._search_bar.on_edit_search)
        menu_bar.add_cascade(label='Edition', underline=1, menu=self._edit_menu)

        # ---- Play menu

        play_menu = tk.Menu(menu_bar, tearoff=0)
        play_menu.add_command(label='Jouer', underline=0, accelerator='Ctrl+J',
                              command=self._player_deck.on_open_deck)
        menu_bar.add_cascade(label='Jouer', underline=0, menu=play_menu)

        self.tk_root.config(menu=menu_bar)

        # ---------------------------------------------------------------------
        #     Global shortcuts
        # ---------------------------------------------------------------------

        self.tk_root.bind('<Control-N>', self._file.on_file_new)
        self.tk_root.bind('<Control-n>', self._file.on_file_new)
        self.tk_root.bind('<Control-O>', self._file.on_file_open)
        self.tk_root.bind('<Control-o>', self._file.on_file_open)
        self.tk_root.bind('<Control-S>', self._file.on_file_save)
        self.tk_root.bind('<Control-s>', self._file.on_file_save)
        self.tk_root.bind('<Control-j>', self._player_deck.on_open_deck)
        self.tk_root.bind('Alt-Keypress-F4', self.exit)

        self._edit_zone._scrolled_text.bind('<Control-Y>',
                                            self._edit_zone.on_edit_redo)
        self._edit_zone._scrolled_text.bind('<Control-y>',
                                            self._edit_zone.on_edit_redo)
            # rem: if bound at root level: ctrl+y will do 'paste', not 'redo'
        self._edit_zone._scrolled_text.bind('<Control-A>',
                                            self._edit_zone.on_edit_select_all)
        self._edit_zone._scrolled_text.bind('<Control-a>',
                                            self._edit_zone.on_edit_select_all)
        self.tk_root.bind('<Control-F>', self._search_bar.on_edit_search)
        self.tk_root.bind('<Control-f>', self._search_bar.on_edit_search)

        self.tk_root.protocol('WM_DELETE_WINDOW', self.exit)

    def _setup_synth(self, libfluidsynth_path: Optional[str] = None):
        self._synth = player.Synth(libfluidsynth_path)
        try:
            self._synth.setup_synth()
            self._synth.select_instrument('Acoustic Grand Piano')
        except player.SingleNoteAbcPlayerException as e:
            # Under Windows, after we display a messagebox before the mainloop():
            # 1. the edit zone looses its focus (and it is difficult to get it back).
            # 2. the global keybindings do not work.
            #
            # Workaround : hide the root window before showing the messagebox
            self.tk_root.withdraw()
            tk_messagebox.showwarning(title='Erreur lors de l\'initialisation du synthétiseur', message=e)
            self.tk_root.deiconify()

    def _build_fav_recent_menu_entries(self):
        recents = recent_files.get_recent_files()
        for path in recents.keys():
            if recents[path] is True:  # favorite file
                icon = self._icon_star
            else:  # recent file
                icon = None
            self._file_menu.insert_command(
                index=self._favrecent_index_first + self._favrecent_nb,
                label=file_utils.prettify_path(path),
                compound='left',
                image=icon,
                command=lambda local_fav=path: self._file.on_file_open(path=local_fav))
            self._favrecent_nb += 1
            # https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result

        self._file_menu.insert_separator(
            index=self._favrecent_index_first + self._favrecent_nb)
        self._favrecent_nb += 1

        # Menu entry enabled if:
        # (1) there is an opened file with a name
        # and (2) it is not already listed in the favorites
        self._file_menu.insert_command(
            index=self._favrecent_index_first + self._favrecent_nb,
            label='Ajouter aux favoris',
            underline=0,
            state=self._file.get_menu_state('add_to_favorites'),
            command=self._file.on_file_add_to_favorites)
        self._favrecent_nb += 1

        self._file_menu.insert_command(
            index=self._favrecent_index_first + self._favrecent_nb,
            label='Retirer des favoris',
            underline=0,
            state=self._file.get_menu_state('remove_from_favorites'),
            command=self._file.on_file_remove_from_favorites)
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
        root_w, root_h = self.tk_root.winfo_screenwidth(),\
                         self.tk_root.winfo_screenheight()
        self.tk_root.geometry("%dx%d+0+0" % (root_w, root_h))

    def exit(self, event=None):
        log.debug('RootWindow.exit()')

        if self._file.ask_save_changes() == 'cancel':
            log.debug('RootWindow.exit(): ask save changes cancelled/failed, aborting')
            return 'break'
        else:
            self._player_deck.exit()
            self.tk_root.destroy()
            # TODO: fix segfault on exit

    def set_title(self, pretty_path, modified_flag):
        """Set the title of the root window

        The title shows the name of the file being edited, and a star '*'
        if the file has been modified in the editor since its last save on disk.

        Args:
            pretty_path (str): string representation of the file path
            modified_flag (bool): whether the file has been modified

        Returns:
            None
        """

        modified_flag_str = '* ' if modified_flag else ''
        self.tk_root.title(modified_flag_str + pretty_path)
