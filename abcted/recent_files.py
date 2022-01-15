#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Manage the lists of recent files and favorite files.
"""

# TODO: update design notes, write section in user guide (explain how recent files are automatically added and removed)
# Rem: if open favorite file fails, it is not removed from the list
# (could be on a removable media) (workaround if desired to remove from
# favorites a file that cannot be opened: close the program and edit
# manually favorite_files.txt)

import collections
import logging as log
import os

from file_utils import normalize_path


CONFIG_DIR = '~/.config/abcted/'
FAVORITE_FILES_FILENAME = 'favorite_files.txt'
FAVORITE_FILES_PATH = CONFIG_DIR + FAVORITE_FILES_FILENAME
RECENT_FILES_FILENAME = 'recent_files.txt'
RECENT_FILES_PATH = CONFIG_DIR + RECENT_FILES_FILENAME
MAX_RECENT_FILES_NB = 10

recent_files_list = []
favorite_files_list = []
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


def get_recent_files():
    """Read and merge the lists of recent and favorite files

    Returns:
        An OrderedDict where the key is the path of the recent and/or
        favorite file and where the value is True if the file is a favorite
        file

    """
    global recent_files_list, favorite_files_list

    favrecent = collections.OrderedDict()
    recent_files_list = _read_file_list(RECENT_FILES_PATH)
    for r in recent_files_list:
        favrecent[r] = False
    favorite_files_list = _read_file_list(FAVORITE_FILES_PATH)
    for f in favorite_files_list:
        favrecent[f] = True
    return favrecent


def promote_recent_file(path):
    """Make a file the most recent file.

    Promote the given file at the top of the recent file list and save
    list to disk.  Add file to recent file list if not already there.

    Args:
        path: normalized path of the recent file

    Returns:
        None
    """
    global recent_files_list

    # Insert/move file at the beginning of the list
    try:
        recent_files_list.remove(path)
    except ValueError:
        pass
    recent_files_list.insert(0, path)

    # Limit the number of recent files kept
    recent_files_list = recent_files_list[:MAX_RECENT_FILES_NB]

    # Write recent files list to disk
    _write_file_list(recent_files_list, RECENT_FILES_FILENAME)

    # Update menu
    if update_recent_files_cb is not None:
        update_recent_files_cb()


def remove_recent_file(path):
    """Remove file from the list of recent files

    Remove the given file from the list of recent files and save the list
    to disk.  If the file is not in the list, ignore quietly the removal
    request.

    Args:
        path: normalized path of the file to remove from recent files

    Returns:
        None
    """
    global recent_files_list

    try:
        recent_files_list.remove(path)
        _write_file_list(recent_files_list, RECENT_FILES_FILENAME)
        if update_recent_files_cb is not None:
            update_recent_files_cb()  # Update menu
    except ValueError:  # path not in favorite files list
        pass


def add_to_favorites(path):
    """Add file to favorites.

    Add the given file at the top of the list of favorite files.  If the file
    is already in the list, promote file at the top of the list.  Finally
    save favorite files list to disk.

    Args:
        path: normalized path of the file to add to favorites

    Returns:
        None
    """
    global favorite_files_list

    # Insert/move file at the beginning of the list
    try:
        favorite_files_list.remove(path)
    except ValueError:
        pass
    favorite_files_list.insert(0, path)

    # Write recent files list on disk
    _write_file_list(favorite_files_list, FAVORITE_FILES_FILENAME)

    # Update menu
    if update_recent_files_cb is not None:
        update_recent_files_cb()


def remove_from_favorites(path):
    """Remove file from favorites.

    Remove the given file from the list of favorite files and save the list
    to disk.  If the file is not in the list, ignore quietly the removal
    request.

    Args:
        path: normalized path of the file to remove from favorites

    Returns:
        None
    """
    global favorite_files_list

    try:
        favorite_files_list.remove(path)
        _write_file_list(favorite_files_list, FAVORITE_FILES_FILENAME)
        if update_recent_files_cb is not None:
            update_recent_files_cb()  # Update menu
    except ValueError:  # path not in favorite files list
        pass


def _write_file_list(file_list: list, filename: str):
    """Write a list of paths to a file in the config dir

    Given a list of file paths, write each path on a single line to a
    text file in the config dir.  Create the config dir if it does not exist.

    Args:
        file_list: list of file paths
        filename: name of the file where the file paths will be
          written to.

    Returns:
        None
    """

    # Create the config dir if it does not exist
    try:
        os.makedirs(os.path.expanduser(CONFIG_DIR))
        log.info('Created dir ' + CONFIG_DIR)
    except OSError:
        pass

    # Write the list of file paths:
    path = os.path.expanduser(CONFIG_DIR + filename)
    with open(path, 'w') as f:
        for file_path in file_list:
            f.write(file_path + '\n')


def _read_file_list(file_list_path):
    """Read a text file containing a list of file paths.

    Read the "favorite files" or "recent files" file, skip empty lines, skip
    comment lines, expand ~, check the file format and return the list of
    paths.

    Args:
        file_list_path(str): path of the file list file

    Returns: a list of file strings
    """

    file_list = []
    abs_file_list_name = os.path.expanduser(file_list_path)

    try:
        with open(abs_file_list_name, 'r') as f:
            for line in f:
                line = line.strip()
                if line == '':
                    continue
                if line.startswith('#'):
                    continue
                raw_path = line

                if raw_path.startswith('~'):
                    raw_path = os.path.expanduser(line)

                path = normalize_path(raw_path)

                # Note: we do not check that the file exists, is a file or
                # is readable.  A favorite file may not always be readable,
                # eg if it is on a removable device or a network drive.

                file_list.append(path)
    except FileNotFoundError:
        log.debug('file not found: ' + abs_file_list_name)

    # TODO: test not UTF-8 encoded favorite_files.txt + issue warning log message
    # rem: on Windows 7, no prb to read a ISO-8859-1 encoded file
    # => test this on Linux

    # TODO: test other IO errors (ie file not readable, ...)

    return file_list
