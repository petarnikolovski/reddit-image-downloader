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


def make_soup(url, parser='lxml', selenium=False):
    """
    Return a soup object. Default parser is lxml. Requests are made by
    default using url.request library.
    """
    if selenium:
        driver = webdriver.PhantomJS()
        driver.get(url)
        html = driver.page_source
        driver.close()
        return BeautifulSoup(html, parser)
    return BeautifulSoup(urlopen(url).read(), parser)


def get_politeness_factor():
    """
    Return politeness factor for reddit.com domain. Calculated according
    to instructions given here:

    https://stackoverflow.com/questions/8236046/typical-politeness-factor-for-a-web-crawler

    Archived versions:
    http://archive.is/AlBg0
    https://web.archive.org/web/20170730001425/https://stackoverflow.com/questions/8236046/typical-politeness-factor-for-a-web-crawler
    """
    DOMAIN_AUTHORITY = 99
    domain_size = DOMAIN_AUTHORITY // 10
    if domain_size <= 5: domain_size = 5
    minimal_crawl_time = min(exp(2.52166863221 + -0.530185027289 * log(domain_size)), 5)
    return minimal_crawl_time


if __name__ == '__main__':
    verbose, url, destination = parse_arguments()
