#!/usr/bin/python3


"""
Parser for gfycat site. For now, it can only parse direct links to videos.
By default, it only downloads .webm format.
"""


from domainparsers.internetaccess import make_soup


def parse_gfycat(url):
    """
    Get direct link for post image/video from gfycat.
    """
    soup = make_soup(url)
    source = soup.find('source', attrs={'id' : 'webmSource'})
    return source['src'] if source else None
