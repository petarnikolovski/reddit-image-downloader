#!/usr/bin/python3


import os
import re
from argparse import ArgumentParser
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from collections import deque
from itertools import groupby
from time import sleep
from math import log
from math import exp


FILE_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.webm']


class Colors(object):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    NOCOLOR = '\033[0m'


def parse_arguments():
    """
    Parse input arguments of the program. Two positional arguments are
    mandatory: 'URL' and destination 'directory'. 'verbose' is optional.
    Example:

    crawlddit.py -v https://www.reddit.com/r/MemeEconomy/ ./dank_memes

    For more information type:

    crawlddit.py --help
    """
    parser = ArgumentParser(description='reddit /r downloader')

    parser.add_argument('-v', '--verbose',
                        help='display download progress and information',
                        action='store_true')
    parser.add_argument('-p', help='crawl P number of pages', type=int)
    parser.add_argument('URL', help='source link')
    parser.add_argument('directory', help='destination directory')

    args = parser.parse_args()

    return (args.verbose, args.p, args.URL, args.directory)


def make_soup(url, parser='lxml', selenium=False):
    """
    Return a soup object. Default parser is lxml. Requests are made by
    default using url.request library.
    """
    if selenium:
        driver = webdriver.PhantomJS()
        driver.get(url)
        html = driver.page_source
        driver.close()
        return BeautifulSoup(html, parser)
    return BeautifulSoup(urlopen(url).read(), parser)


def make_beautiful_soup(url, driver, parser='lxml'):
    """
    Get soup object from url using selenium driver. If request is
    redirected, then confirm redirect dialog.
    """
    driver.get(url)

    submit_exists = driver.find_element_by_xpath(
        '//button[@type='submit'][@value='yes']'
    )
    if submit_exists:
        confirm_redirect_dialog(driver)

    return BeautifulSoup(driver.page_source, parser)


def confirm_redirect_dialog(driver):
    """
    If redirection dialog pops up, click confirm/continue button.
    """
    # '//button[@type='submit' and @value='yes']'
    driver.find_element_by_xpath(
        '//button[@type='submit'][@value='yes']'
    ).click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_an_element_located(
            (By.XPATH, '//span[@class='next-button']')
        )
    )


def get_all_posts(url, pages):
    """
    Crawl links of all posts, or posts from P number of pages. If P
    i.e. 'pages' is 0, then crawl all pages.
    """
    driver = webdriver.PhantomJS()

    images = []
    crawl = True
    crawl_time = get_politeness_factor()
    page = 1 if pages else 0

    while (page <= pages) and crawl:
        soup = make_beautiful_soup(url, driver)
        pictures, next_page = get_files_from_a_page(soup, url)

        images.extend(pictures)
        url = next_page

        if pages: page += 1
        if not next_page: crawl = False

        sleep(crawl_time)

    driver.close()
    return images


def get_files_from_a_page(soup, url=None):
    """
    Get links and other information to all files from a single page.
    Return link for next page if it exists.
    """
    things = soup.find_all('div', attrs={'class' : re.compile(r'\sthing\sid-t3.+')})
    images = deque({
            'url' : get_post_url(div),
            'filename' : None,
            'domain' : get_post_domain(div),
            'post_title' : get_post_title(div),
            'posted_on' : get_post_timestamp(div),
            'link_to_comments' : get_link_to_comments(div),
            'on_page' : url,
            'html_status_token' : 0,
        } for div in things
    )

    next_page_span = soup.find('span', attrs={'class' : 'next-button'})
    next_page = next_page_span.a['href'] if next_page_span else None

    return (images, next_page)


def get_link_to_comments(div):
    """
    Get a link to a comment section.
    """
    li = div.find('li', attrs={'class' : 'first'})
    #return ''.join(['https://www.reddit.com', li.a['href']])
    return li.a['href']


def get_post_timestamp(div):
    """
    Get time and date when post was created.
    """
    time = div.find('time')
    return time['datetime'] if time.has_attr('datetime') else None


def get_p_title_tag(div):
    """
    Get <p> tag with class="title".
    """
    return div.find('p', attrs={'class' : 'title'})


def get_post_url(div):
    """
    Get url of a post.
    """
    p = get_p_title_tag(div)
    return p.a['href']


def get_post_domain(div):
    """
    Get domain of a post.
    """
    p = get_p_title_tag(div)
    span = p.find('span', attrs={'class' : 'domain'})
    return span.a.string


def get_post_title(div):
    """
    Get title of a post.
    """
    return get_p_title_tag(div).a.string


def get_politeness_factor():
    """
    Return politeness factor for reddit.com domain. Calculated according
    to instructions given here:

    https://stackoverflow.com/questions/8236046/typical-politeness-factor-for-a-web-crawler

    Archived versions:
    http://archive.is/AlBg0
    https://web.archive.org/web/20170730001425/https://stackoverflow.com/questions/8236046/typical-politeness-factor-for-a-web-crawler
    """
    DOMAIN_AUTHORITY = 99
    domain_size = DOMAIN_AUTHORITY // 10
    if domain_size <= 5: domain_size = 5
    minimal_crawl_time = min(exp(2.52166863221 + -0.530185027289 * log(domain_size)), 5)
    return minimal_crawl_time


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
    for domain in domains:
        print(domain[0], domain[1])


if __name__ == '__main__':
    verbose, pages, url, destination = parse_arguments()

    if not pages: pages = 0
    images = get_all_posts(url, pages)

    print(images)
    #print(next_page)
    print(len(images))
    print_all_domains(get_all_domains(images))
