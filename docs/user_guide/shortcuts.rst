==================
Raccourcis clavier
==================

Gestion de fichiers
===================

        self.tk_root.bind('<Control-N>', self._file.on_file_new)
        self.tk_root.bind('<Control-n>', self._file.on_file_new)
        self.tk_root.bind('<Control-O>', self._file.on_file_open)
        self.tk_root.bind('<Control-o>', self._file.on_file_open)
        self.tk_root.bind('<Control-S>', self._file.on_file_save)
        self.tk_root.bind('<Control-s>', self._file.on_file_save)
        self.tk_root.bind('<Control-j>', self._on_play)
        self.tk_root.bind('Alt-Keypress-F4', self.exit)


Zone d'édition du texte
=======================

        self._edit_zone._scrolled_text.bind('<Control-Y>',
                                            self._edit_zone.on_edit_redo)
        self._edit_zone._scrolled_text.bind('<Control-y>',
                                            self._edit_zone.on_edit_redo)
            # rem: if bound at root level: ctrl+y will do 'paste', not 'redo'
        self._edit_zone._scrolled_text.bind('<Control-A>',
                                            self._edit_zone.on_edit_select_all)
        self._edit_zone._scrolled_text.bind('<Control-a>',
                                            self._edit_zone.on_edit_select_all)


.. TODO: raccourcis implicites de tkinter

Recherche
=========

        self.tk_root.bind('<Control-F>', self._search_bar.on_edit_search)
        self.tk_root.bind('<Control-f>', self._search_bar.on_edit_search)

Raccourcis de la barre de recherche
-----------------------------------

            w.bind('<Escape>', self._on_search_close)
            w.bind('<F3>', self._on_search_forward)
            w.bind('<Down>', self._on_search_forward)
            w.bind('<Up>', self._on_search_backward)
            w.bind('<Alt-c>', self._on_toggle_match_case)
            w.bind('<Alt-C>', self._on_toggle_match_case)


Raccourcis de la zone de saisie du terme de recherche
-----------------------------------------------------

        self._search_entry.bind('<Return>', self._on_search_forward)
        self._search_entry.bind('<Control-A>', self._on_select_all_search_entry)
        self._search_entry.bind('<Control-a>', self._on_select_all_search_entry)


Jouer un morceau
================

```Ctrl + J```: joue le morceau courant (le morceau dans lequel est le
curseur clavier)
