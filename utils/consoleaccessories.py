#!/usr/bin/python3


import os


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
