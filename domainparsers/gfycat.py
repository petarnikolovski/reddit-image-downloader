#!/usr/bin/python3


"""
Parser for gfycat site. For now, it can only parse direct links to videos.
By default, it only downloads .webm format.
"""


from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup


__author__ = 'petarGitNik'
__copyright__ = 'Copyright (c) 2017 petarGitNik petargitnik@gmail.com'
__version__ = 'v0.1.0'
__license__ = 'MIT'
__email__ = 'petargitnik@gmail.com'
__status__ = 'Development'


class Gfycat(object):

    def __init__(self, url):
        self.url = url

    def make_soup(self, parser='lxml'):
        """
        Return a soup object. Default parser is lxml. Requests are made by
        default using url.request library.
        """
        return BeautifulSoup(urlopen(self.url).read(), parser)

    def parse_gfycat(self):
        """
        Get direct link for post image/video from gfycat.
        """
        soup = self.make_soup()
        source = soup.find('source', attrs={'id' : 'webmSource'})
        return source['src'] if source else None
