#!/usr/bin/python3


from itertools import groupby


"""
Logging, debugging, and analysis tools.
"""


def get_all_domains(posts):
    """
    Get all domains from list of files.
    """
    domains = []
    for post in posts:
        domains.append(post['domain'])

    domains.sort()
    grouped_domains = []
    for key, group in groupby(domains):
        grouped_domains.append((len(list(group)), key))
    return grouped_domains


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
        if post['image']['image_url']: downloadable += 1
    return downloadable
