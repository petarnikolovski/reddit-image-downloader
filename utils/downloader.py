#!/usr/bin/python3


"""
Downloads files.
"""


import os
import sqlite3
from utils.consoleaccessories import is_valid_path
from utils.consoleaccessories import clean_path


def download_files(files, destination, verbose):
    """
    This function downloads files to a specified directory. Destination
    is a path to a directory where images will be stored. If verbose is
    True, then the download status is displayed.
    """
    current_directory = os.getcwd()
    os.chdir(destination)

    # Check if db exists in destination directory
    db_path = ''.join([clean_path(path), '/db.sqlite'])
    if not is_valid_path(db_path):
        conn = make_connection(path)

    os.chdir(current_directory)


def make_connection(path):
    return sqlite3.connect(path)
