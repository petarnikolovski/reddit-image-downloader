#!/usr/bin/python3

import os
from argparse import ArgumentParser
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from selenium import webdriver
from collections import deque
from time import sleep
from math import log
from math import exp

def parse_arguments():
    """
    Parse input arguments of the program. Two positional arguments are
    mandatory: 'URL' and destination 'directory'. 'verbose' is optional.
    Example:

    crawlddit.py -v https://www.reddit.com/r/MemeEconomy/ ./dank_memes

    For more information type:

    crawlddit.py --help
    """
    parser = ArgumentParser(dectiption='reddit /r downloader')

    parser.add_argument('-v', '--verbose',
                        help='display download progress and information',
                        action='store_true')
    parser.add_argument('URL', help='source link')
    parser.add_argument('directory', help='destination directory')

    args = parser.parse_args()

    return (args.verbose, args.URL, args.directory)


if __name__ == '__main__':
    verbose, url, destination = parse_arguments()
