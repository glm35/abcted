Roadmap
=======

Prochains développements
------------------------

* Documenter les raccourcis clavier de l'application (menu édition, barre de
  recherche, ...)

* Tune list (outline)

* Playback d'un tune ou d'une partie d'un tune

** demo_music_box.py

** vérifier que si on charge la soundfont avant la création du séquenceur,
   il n'y a pas de son (à tester juste après un reboot de la machine).

* Prendre en compte les enseignements généraux de demo_music_box.py:

** arrêter proprement fluidsynth à la fin d'abcde;

** attention à l'ordre de création du séquenceur et du chargement des
   soundfont.

* Le nom abcde est déjà pris (paquet abcde "A Better CD Encoder" sous debian/ubuntu/mint):
  trouver un autre nom. "abcted" (ou "abcTed", ou "ABCtED" ou "ABCted") semble un bon candidat pas encore pris
  (cf. http://abcnotation.com/software


pyfluidsynth3 features & fixes
------------------------------

* make it possible to register a Python callback (example in
  tests/demo_music_box.py with direct calls to the low-level fluidsynth API

* fluidsequencer.py: with BPM_DEFAULT=120 and the default value of
  ticks_per_second in fluidsynth which is 1000, TPB_DEFAULT should be 500

Main features
-------------

* Tune playback (whole tune, selection, with loop, with tick)

* "Print" tune to external PDF viewer


Random desired features for abcde
---------------------------------

* Display current line and column number (useful for located issues
  in an ABC file reported by an external tool).

* A command to format/wrap multi-line history header fields (H:)

* Syntax highlighting

* Internationalization & english translation
