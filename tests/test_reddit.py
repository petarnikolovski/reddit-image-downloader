#!/usr/bin/python3


import pytest
from domainparsers.reddit import Reddit
from domainparsers.reddit import RedditException
from domainparsers.common import FileFormats

@pytest.fixture
def test_link():
    return Reddit('https://www.reddit.com/r/MemeEconomy/')

def test_invalid_link():
    """
    Test if the class raises exception for the invalid link.
    """
    with pytest.raises(RedditException):
        Reddit('https://reddit.com/')

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
