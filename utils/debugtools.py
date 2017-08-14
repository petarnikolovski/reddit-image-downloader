#!/usr/bin/python3


"""
Debugging, and analysis tools.
"""


def print_all_domains(domains):
    """
    Print list of all domains appearing in /r group. First element is
    number of times a domain appears in a posts list, second element is
    corresponding domain name.
    """
    for domain in sorted(domains, key=lambda x: x[0]):
        print(domain[0], domain[1])


def count_downloadable_images(posts):
    """
    Count images from post that have direct download link available.
    """
    downloadable = 0
    for post in posts:
        if post['image']['url']: downloadable += 1
    return downloadable
