#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Play an ABC tune or a tune selection
"""

import logging as log

import abcparser
from edit_zone_buffer import EditZoneBuffer


def play(buffer: EditZoneBuffer):
    raw_tune = abcparser.get_current_raw_tune(buffer)
    # TODO: handle AbcParserException
    log.debug('raw_tune: ' + str(raw_tune))
