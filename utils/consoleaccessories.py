#!/usr/bin/python3


import os


def is_valid_path(path):
    """
    Checks if the directory/file exists on a given path.
    """
    return os.path.exists(path)
