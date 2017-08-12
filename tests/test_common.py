#!/usr/bin/python3


import pytest
from domainparsers.common import FileFormats
from domainparsers.common import Domains

def test_file_formats():
    """
    Test if formats class method returns a set of predefined formats.
    """
    result = {'.tiff', '.png', '.jpeg', '.webm', '.mp4', '.jpg', '.apng', '.gif'}
    assert FileFormats.formats() == result

def test_domains():
    """
    Test if the domain class returns a set of predefined domanins.
    """
    result = {'reddit', 'gfycat', 'blogspot', 'tumblr', 'imgur'}
    assert Domains.domains() == result
