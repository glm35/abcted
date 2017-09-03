#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import ui.root_window


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug',
                        help='Enable debug messages',
                        action='store_true')
    parser.add_argument('filename', help='ABC file to open at startup (optional)', type=str, nargs='?')
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
    root = ui.root_window.RootWindow(filename=args.filename)
    root.mainloop()


if __name__ == "__main__":
    main()
