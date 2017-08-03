#!/usr/bin/python3


class Colors(object):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    NOCOLOR = '\033[0m'


def is_valid_domain(url):
    """
    Checks if the domain is valid for the application.
    """
    if 'www.reddit.com' in url:
        return True
    return False


if __name__ == '__main__':
    print(__doc__)
