#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os


def normalize_path(raw_path):
    """
    Given a path to a file (ie absolute or relative directory name plus
    filename) typically coming from the outside of the program, make it
    absolute and normalize it.

    Args:
        raw_path: path before normalization

    Returns:
        path after normalization

    """

    # Transform relative paths into absolute paths:
    if not os.path.isabs(raw_path):
        raw_path = os.path.abspath(raw_path)
    # Normalize path, eg to get a consistent path separator:
    path = os.path.normpath(raw_path)
    return path


def prettify_path(path):
    """
    Given a path (eg '/home/gwen/Musique/gwen_tunes.abc'), return the filename
    followed between parenthesis by the directory.  If possible, the directory
    is relative to the home directory.

    Example: 'gwen_tunes.abc (~/Musique)'

    Returns:
        a string with the prettified filename
    """
    dirname = os.path.dirname(path)
    home = os.path.expanduser('~')
    if dirname.startswith(home):
        dirname = '~' + dirname[len(home):]
    pretty = '{} ({})'.format(os.path.basename(path), dirname)
    return pretty
