#!/usr/bin/python3


from math import log
from math import exp
from domainparsers.common import Domains


def get_politeness_factor(domain):
    """
    Return politeness factor for reddit.com domain. Calculated according
    to instructions given here:

    https://stackoverflow.com/questions/8236046/typical-politeness-factor-for-a-web-crawler

    Archived versions:
    http://archive.is/AlBg0
    https://web.archive.org/web/20170730001425/https://stackoverflow.com/questions/8236046/typical-politeness-factor-for-a-web-crawler
    """
    if not domain or domain not in Domains.domains():
        domain = 'other'

    DOMAIN_AUTHORITY = {
        Domains.REDDIT : 99,
        Domains.IMGUR : 93,
        Domains.GFYCAT : 70,
        Domains.TUMBLR : 100, # tumblr allows crawl time of 1s https://www.tumblr.com/robots.txt
        Domains.BLOGSPOT : 97,
        'other' : 0,
    }
    domain_size = DOMAIN_AUTHORITY[domain] // 10
    if domain_size <= 5: domain_size = 5
    minimal_crawl_time = min(exp(2.52166863221 + -0.530185027289 * log(domain_size)), 5)
    return minimal_crawl_time
