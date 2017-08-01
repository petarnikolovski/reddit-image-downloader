#!/usr/bin/python3


def get_politeness_factor(domain):
    """
    Return politeness factor for reddit.com domain. Calculated according
    to instructions given here:

    https://stackoverflow.com/questions/8236046/typical-politeness-factor-for-a-web-crawler

    Archived versions:
    http://archive.is/AlBg0
    https://web.archive.org/web/20170730001425/https://stackoverflow.com/questions/8236046/typical-politeness-factor-for-a-web-crawler
    """
    DOMAIN_AUTHORITY = {
        'reddit' : 99,
        'imgur' : 93,
        'gfycat' : 70,
        'tumblr' : 99, # tumblr allows crawl time of 1s https://www.tumblr.com/robots.txt
        'instagram' : None, # instagram robots.txt forbids all bots
        'blogspot' : None,
        'other' : 0,
    }
    domain_size = DOMAIN_AUTHORITY[domain] // 10
    if domain_size <= 5: domain_size = 5
    minimal_crawl_time = min(exp(2.52166863221 + -0.530185027289 * log(domain_size)), 5)
    return minimal_crawl_time
