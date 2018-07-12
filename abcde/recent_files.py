#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Manage the lists of recent files and favorite files.
"""

import logging as log
import os

CONFIG_DIR = '~/.config/abcde/'
FAVORITE_FILES = CONFIG_DIR + 'favorite_files.txt'
RECENT_FILES = CONFIG_DIR + 'recent_files.txt'
MAX_RECENT_FILES_NB = 10

recent_files = []
update_recent_files_cb = None


def register_update_recent_files_cb(callback):
    """Register a function that will be called each time the list of recent or
    favorite files is updated.

    Args:
        callback: function without parameter

    Returns:
        None

    """
    global update_recent_files_cb
    update_recent_files_cb = callback


def read_favorite_files():
    """Read the "favorite files" file

    Read the "favorite files" file and return the list of favorite files.

    Returns: a list of favorite file strings
    """

    return _read_file_list(FAVORITE_FILES)


def read_recent_files():
    """Read the "recent files" file

    Read the "recent files" file and return the list of favorite files.

    Returns: a list of recent file strings
    """
    global recent_files

    recent_files = _read_file_list(RECENT_FILES)
    return recent_files.copy()


def update_recent_files(filename):
    """Update the recent files list and save to disk

    Args:
        filename: file name of the recent file

    Returns:
        None
    """
    global recent_files

    # Transform relative paths into absolute paths:
    if not os.path.isabs(filename):
        filename = os.path.abspath(filename)
    # Normalize path, eg to get a consistent path separator:
    filename = os.path.normpath(filename)

    # Insert/move file at the beginning of the list
    try:
        recent_files.remove(filename)
    except ValueError:
        pass
    recent_files.insert(0, filename)

    # Limit the number of recent files kept
    recent_files = recent_files[:MAX_RECENT_FILES_NB]

    # Write recent files list on disk
    _write_recent_files()

    # Update menu
    if update_recent_files_cb is not None:
        update_recent_files_cb()


def _write_recent_files():
    """Write the list of recent files to disk

    Returns:
        None
    """
    global recent_files

    # Create the config dir if it does not exist
    try:
        os.makedirs(os.path.expanduser(CONFIG_DIR))
        log.info('Created dir ' + CONFIG_DIR)
    except OSError:
        pass

    # Write the recent files
    filename = os.path.expanduser(RECENT_FILES)
    with open(filename, 'w') as f:
        for recent in recent_files:
            f.write(recent + '\n')


def _read_file_list(file_list_name):
    """Read a text file containing a list of files

    Read the "favorite files" or "recent files" file, skip empty lines, skip
    comment lines, expand ~, check the file format and return the list of
    files.

    Args:
        file_list_name(str): filename with path

    Returns: a list of file strings
    """

    file_list = []
    abs_file_list_name = os.path.expanduser(file_list_name)

    try:
        with open(abs_file_list_name, 'r') as f:
            for line in f:
                line = line.strip()
                if line == '':
                    continue
                if line.startswith('#'):
                    continue
                filename = line

                if filename.startswith('~'):
                    filename = os.path.expanduser(line)

                # Transform relative paths into absolute paths:
                if not os.path.isabs(filename):
                    filename = os.path.abspath(filename)

                # Normalize path, eg to get a consistent path separator:
                filename = os.path.normpath(filename)

                # Note: we do not check that the file exists, is a file or
                # is readable.  A favorite file may not always be readable,
                # eg if it is on a removable device or a network drive.

                file_list.append(filename)
    except FileNotFoundError:
        log.debug('File not found: ' + abs_file_list_name)

    # TODO: test not UTF-8 encoded favorite_files.txt + issue warning log message
    # rem: on Windows 7, no prb to read a ISO-8859-1 encoded file
    # => test this on Linux

    # TODO: test other IO errors (ie file not readable, ...)

    return file_list
