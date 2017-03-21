#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
from ui.root_window import start_ui


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug',
                        help='Enable debug messages',
                        action='store_true')
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
    start_ui()


if __name__ == "__main__":
    main()
