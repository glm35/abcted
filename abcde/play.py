#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Play an ABC tune or a tune selection
"""

import logging as log

from edit_zone_buffer import EditZoneBuffer


def play(buffer: EditZoneBuffer):
    log.debug('Line at cursor: ' + str(buffer.get_line_no_at_cursor()))
