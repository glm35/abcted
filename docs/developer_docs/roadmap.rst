Roadmap
=======

Prochains développements
------------------------

* Refactor file management using pathlib (for better windows compat)

* Playback d'un tune ou d'une partie d'un tune

  * vérifier que si on charge la soundfont avant la création du séquenceur,
    il n'y a pas de son (à tester juste après un reboot de la machine).

  * Prendre en compte les enseignements généraux de demo_music_box.py:

  * arrêter proprement fluidsynth à la fin d'abcted;

  * attention à l'ordre de création du séquenceur et du chargement des
    soundfont.

* Documenter les raccourcis clavier de l'application (menu édition, barre de
  recherche, ...)

* Voir les nouveautés python 3.8 qui peuvent améliorer la lisibilité du code

* Tune list (outline)

* License au format SPDX dans les fichiers: https://spdx.org/ids-how

* refactoring avec tuple unpacking

  * https://treyhunner.com/2018/03/tuple-unpacking-improves-python-code-readability/

  * Boucles for

  * Index codés en dur, yc dans un contexte de Slicing (=> utiliser l’opérateur \*)

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


Random desired features for abcted
----------------------------------

* Display current line and column number (useful for located issues
  in an ABC file reported by an external tool).

* A command to format/wrap multi-line history header fields (H:)

* Syntax highlighting

* Internationalization & english translation
