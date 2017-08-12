#!/usr/bin/python3


import pytest
from domainparsers.reddit import Reddit
from domainparsers.reddit import RedditException

@pytest.fixture
def test_link():
    return Reddit('https://www.reddit.com/r/MemeEconomy/')

def test_invalid_link():
    """
    Test if the class raises exception for the invalid link.
    """
    with pytest.raises(RedditException):
        Reddit('https://reddit.com/')
