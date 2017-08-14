#!/usr/bin/python3


"""
Debugging, and analysis tools.
"""


def count_downloadable_images(posts):
    """
    Count images from post that have direct download link available.
    """
    downloadable = 0
    for post in posts:
        if post['image']['url']: downloadable += 1
    return downloadable
