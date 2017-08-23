#!/usr/bin/python3


import pytest
from domainparsers.reddit import Reddit
from domainparsers.reddit import RedditException
from domainparsers.common import FileFormats
from domainparsers.common import Domains


__author__ = 'petarGitNik'
__copyright__ = 'Copyright (c) 2017 petarGitNik petargitnik@gmail.com'
__version__ = 'v0.1.0'
__license__ = 'MIT'
__email__ = 'petargitnik@gmail.com'
__status__ = 'Development'


@pytest.fixture
def test_link():
    return Reddit('https://www.reddit.com/r/MemeEconomy/', 15)

def test_invalid_link():
    """
    Test if the class raises exception for the invalid link.
    """
    with pytest.raises(RedditException):
        Reddit('https://reddit.com/', None)

def test_file_formats(test_link):
    """
    Test if the known_file_format method returns correct formats.
    """
    url_1 = 'http://i.imgur.com/jedEzFL.jpg'
    url_2 = 'http://i.imgur.com/jedEzFL.png'
    url_3 = 'http://i.imgur.com/jedEzFL.webm'
    url_4 = 'http://i.imgur.com/jedEzFL.m'
    result_1 = FileFormats.JPG
    result_2 = FileFormats.PNG
    result_3 = FileFormats.WEBM
    result_4 = None
    assert test_link.known_file_format(url_1) == result_1
    assert test_link.known_file_format(url_2) == result_2
    assert test_link.known_file_format(url_3) == result_3
    assert test_link.known_file_format(url_4) == result_4

def test_image_dictionary(test_link):
    """
    Test if the image_dictionary method returns dictinary in correct
    format.
    """
    url = 'https://example.com'
    filename = 'example.com'
    result = {'url' : url, 'filename' : filename}
    assert test_link.image_dictionary(url, filename) == result

def test_image_filename(test_link):
    """
    Test whether the image filename function returns the correct file
    name.
    """
    url_1 = 'http://i.imgur.com/lciC5G8.jpg'
    url_2 = 'http://i.imgur.com/lciC5G8.jpg?1'
    url_3 = 'http://i.imgur.com/lciC5G8.png'
    result_1_2 = 'lciC5G8.jpg'
    result_3 = 'lciC5G8.png'
    assert test_link.get_image_filename(url_1) == result_1_2
    assert test_link.get_image_filename(url_2) == result_1_2
    assert test_link.get_image_filename(url_3) == result_3

def test_domain(test_link):
    """
    Test if method known_domain returns correct domain.
    """
    url_1 = 'http://i.imgur.com/lciC5G8.jpg'
    url_2 = 'https://www.instagram.com'
    assert test_link.known_domain(url_1) == Domains.IMGUR
    assert test_link.known_domain(url_2) == None
    assert test_link.known_domain(test_link.url) == Domains.REDDIT

def test_normalization_of_images(test_link):
    """
    Test if normalize_pages returns 0 for None, or pages number otherwise.
    """
    assert test_link.pages == 15
    assert Reddit('http://www.reddit.com/', None).pages == 0
