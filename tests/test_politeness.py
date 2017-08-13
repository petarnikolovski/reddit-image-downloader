#!/usr/bin/python3


import pytest
from utils.politeness import get_politeness_factor


def test_politeness_for_false_inputs():
    """
    Test politeness factor for unknown domain inputs.
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
