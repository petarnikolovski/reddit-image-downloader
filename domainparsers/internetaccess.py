#!/usr/bin/python3


"""
Contains tools to access web pages and make soup objects out of them.
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
