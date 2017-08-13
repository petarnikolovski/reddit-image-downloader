#!/usr/bin/python3


import pytest
from utils.politeness import get_politeness_factor
from domainparsers.common import Domains


def test_politeness_for_false_inputs():
    """
    Test politeness factor for False values.
    """
    assert get_politeness_factor(None) == 5
    assert get_politeness_factor(0) == 5
    assert get_politeness_factor(False) == 5
    assert get_politeness_factor([]) == 5

def test_politeness_for_unwknown_domains():
    """
    Test politeness factor for unknown domain inputs.
    """
    assert get_politeness_factor('flickr') == 5
    assert get_politeness_factor('pexels') == 5
    assert get_politeness_factor('instagram') == 5

def test_politeness_for_known_domains():
    """
    Test politeness factor for known domains.
    """
    assert get_politeness_factor(Domains.REDDIT) == 3.88348544015422
    assert get_politeness_factor(Domains.IMGUR) == 3.88348544015422
    assert get_politeness_factor(Domains.GFYCAT) == 4.436989947253095
    assert get_politeness_factor(Domains.TUMBLR) == 3.6724994960588933
    assert get_politeness_factor(Domains.BLOGSPOT) == 3.88348544015422
