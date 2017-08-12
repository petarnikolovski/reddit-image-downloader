#!/usr/bin/python3


"""
Parser for gfycat site. For now, it can only parse direct links to videos.
By default, it only downloads .webm format.
"""


from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup


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


def parse_gfycat(url):
    """
    Get direct link for post image/video from gfycat.
    """
    soup = make_soup(url)
    source = soup.find('source', attrs={'id' : 'webmSource'})
    return source['src'] if source else None
