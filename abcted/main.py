#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging as log

import root_window


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug',
                        help='Affiche les messges de log (en anglais)',
                        action='store_true')
    parser.add_argument("-l", "--libfluidsynth-path",
                        help="Path to libfluidsynth (default: pyfluidsynth3 will try to find it).")
    parser.add_argument('filename', help='Fichier ABC à ouvrir au démarrage (optionnel)',
                        type=str, nargs='?')
    args = parser.parse_args()
    return args


def setup_logging(enable_debug):
    if enable_debug:
        log.basicConfig(
            format='%(asctime)s:%(levelname)s:%(threadName)s'
                   ':%(filename)s:%(funcName)s: %(message)s',
            level=log.DEBUG)
        log.info("Debug mode enabled")
    else:
        log.basicConfig(format='%(levelname)s:%(message)s', level=log.INFO)

    # Note: documentation of the attributes that can be used in the format
    # argument of logging.basicConfig:
    # https://docs.python.org/3/library/logging.html#logrecord-attributes


def main():
    args = parse_args()
    setup_logging(enable_debug=args.debug)
    root_win = root_window.RootWindow(raw_path=args.filename,
                                      libfluidsynth_path=args.libfluidsynth_path)
    root_win.tk_root.mainloop()


if __name__ == "__main__":
    main()
