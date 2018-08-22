#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging

import root_window


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug',
                        help='Affiche les messges de log (en anglais)',
                        action='store_true')
    parser.add_argument('filename', help='Fichier ABC à ouvrir au démarrage (optionnel)', type=str, nargs='?')
    args = parser.parse_args()
    return args


def setup_logging(enable_debug):
    logging_level = logging.DEBUG if enable_debug else logging.WARNING
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)
    if enable_debug:
        logging.info("Debug mode enabled")


def main():
    args = parse_args()
    setup_logging(enable_debug=args.debug)
    root_win = root_window.RootWindow(raw_path=args.filename)
    root_win.tk_root.mainloop()


if __name__ == "__main__":
    main()
