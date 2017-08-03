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


if __name__ == '__main__':
    print(__doc__)
