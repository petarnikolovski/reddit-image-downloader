#!/usr/bin/python3


import os


class Colors(object):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    NOCOLOR = '\033[0m'


def is_valid_domain(url):
    """
    Checks if the domain is valid for the application.
    """
    return 'www.reddit.com' in url


def is_valid_path(path):
    """
    Checks if the directory/file exists on a given path.
    """
    return os.path.exists(path)


def clean_path(path):
    """
    Check if the path ends with a slash. If it ends, remove it.
    """
    return path[:-1] if path.endswith('/') else path
