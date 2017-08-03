#!/usr/bin/python3


"""
Downloads files.
"""


import os


def download_files(files, destination, verbose):
    """
    This function downloads files to a specified directory. Destination
    is a path to a directory where images will be stored. If verbose is
    True, then the download status is displayed.
    """
    current_directory = os.getcwd()
    os.chdir(destination)

    os.chdir(current_directory)


if __name__ == '__main__':
    print(__doc__)
