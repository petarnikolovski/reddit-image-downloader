#!/usr/bin/python3


"""
Parser for reddit.
"""


import re
from contextlib import suppress
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from domainparsers.gfycat import Gfycat
from domainparsers.common import FileFormats
from domainparsers.common import Domains
from utils.politeness import get_politeness_factor
from collections import deque
from itertools import groupby
from time import sleep


class RedditException(Exception):
    """
    This exception is raised if supplied link is invalid.
    """
    pass


class Reddit(object):

    def __init__(self, url, pages):
        self.url = self.sanitize(url)
        self.pages = self.normalize_pages(pages)
        self.images = deque() # consider changing images to posts

    def sanitize(self, url):
        """
        Check if the provided domain is indeed reddit.
        """
        if re.match('https?\:\/\/www.reddit\.com\/', url):
            return url
        raise RedditException('Invalid link.')

    def normalize_pages(self, pages):
        """
        If input pages are of None type, turn them into int type.
        """
        return 0 if not pages else pages

    def make_beautiful_soup(self, url, driver, parser='lxml'):
        """
        Get soup object from url using selenium driver. If request is
        redirected, then confirm redirect dialog.
        """
        driver.get(url)

        with suppress(NoSuchElementException):
            submit_exists = driver.find_element_by_xpath(
                "//button[@type='submit'][@value='yes']"
            )

            self.confirm_redirect_dialog(driver)

        return BeautifulSoup(driver.page_source, parser)

    def confirm_redirect_dialog(self, driver):
        """
        If redirection dialog pops up, click confirm/continue button.
        """
        button = driver.find_element_by_xpath(
            "//button[@type='submit' and @value='yes']"
        )
        driver.execute_script("arguments[0].click();", button)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//span[@class='next-button']")
                )
            )
        except TimeoutException as e:
            driver.save_screenshot('screenshot.png')
            print('Loading taking too much time.\n', e)

    def get_all_posts(self):
        """
        Crawl links of all posts, or posts from P number of pages. If P
        i.e. 'pages' is 0, then crawl all pages.
        """
        driver = webdriver.PhantomJS()

        crawl = True
        crawl_time = get_politeness_factor(Domains.REDDIT)
        page = 1 if self.pages else 0
        url = self.url # starting page

        while (page <= self.pages) and crawl:
            soup = self.make_beautiful_soup(url, driver)
            pictures, next_page = self.get_files_from_a_page(soup, url)

            self.images.extend(pictures)
            url = next_page

            if self.pages: page += 1
            if not next_page: crawl = False

            sleep(crawl_time)

        driver.close()
        return

    def get_files_from_a_page(self, soup, url=None):
        """
        Get links and other information to all files from a single page.
        Return link for next page if it exists.
        """
        things = soup.find_all('div', attrs={'class' : re.compile(r'\sthing\sid-t3.+')})
        images = deque({
                'url' : self.get_post_url(div),
                'image' : self.get_image(div),
                'domain' : self.get_post_domain(div),
                'second_level_domain_name' : self.known_domain(url),
                'post_title' : self.get_post_title(div),
                'posted_on' : self.get_post_timestamp(div),
                'link_to_comments' : self.get_link_to_comments(div),
                'on_page' : url,
                'last_http_status' : None,
                'http_status_token' : 0,
            } for div in things
        )

        next_page_span = soup.find('span', attrs={'class' : 'next-button'})
        next_page = next_page_span.a['href'] if next_page_span else None

        return (images, next_page)

    def get_image(self, div):
        """
        Get image url and image filename.
        """
        url = self.get_post_url(div)
        if self.known_file_format(url):
            return self.image_dictionary(url, self.get_image_filename(url))
        image_url = self.get_image_link_from_allowed_domain(url, self.known_domain(url))
        filename = self.get_image_filename(image_url) if image_url else None
        return self.image_dictionary(image_url, filename)

    def get_image_link_from_allowed_domain(self, url, domain):
        """
        Use correct domain parser.
        """
        if domain == Domains.REDDIT:
            return None
        elif domain == Domains.IMGUR:
            return None
        elif domain == Domains.GFYCAT:
            return Gfycat(url).parse_gfycat()
        elif domain == Domains.TUMBLR:
            return None
        elif domain == Domains.BLOGSPOT:
            return None
        else:
            return None
        # raise DomainMissingException('Unknown domain, missing parsing tools.')

    def known_domain(self, url):
        """
        Check if the domain is in the list of known/allowed domains.
        """
        for domain in Domains.domains():
            if domain in url:
                return domain
        return None

    def get_image_filename(self, url):
        """
        Get image file name from its url.
        """
        candidate = url.split('/')[-1]
        extension = self.known_file_format(url)
        pattern = ''.join(['.+\\', extension])
        return re.match(pattern, candidate).group(0)

    def image_dictionary(self, url, filename):
        """
        Returns a dictionary with image url and corresponding filename.
        """
        return {'url' : url, 'filename' : filename}

    def known_file_format(self, url):
        """
        Check if the url contains known file format extension.
        """
        for extension in FileFormats.formats():
            if extension in url:
                return extension
        return None

    def get_link_to_comments(self, div):
        """
        Get a link to a comment section.
        """
        li = div.find('li', attrs={'class' : 'first'})
        return li.a['href']

    def get_post_timestamp(self, div):
        """
        Get time and date when post was created.
        """
        time = div.find('time')
        return time['datetime'] if time.has_attr('datetime') else None

    def get_p_title_tag(self, div):
        """
        Get <p> tag with class="title".
        """
        return div.find('p', attrs={'class' : 'title'})

    def get_post_url(self, div):
        """
        Get url of a post.
        """
        p = self.get_p_title_tag(div)
        return p.a['href']

    def get_post_domain(self, div):
        """
        Get domain of a post.
        """
        p = self.get_p_title_tag(div)
        span = p.find('span', attrs={'class' : 'domain'})
        return span.a.string

    def get_post_title(self, div):
        """
        Get title of a post.
        """
        return self.get_p_title_tag(div).a.string

    def get_all_domains(self):
        """
        Get all domains from list of files.
        """
        domains = []
        for image in self.images:
            domains.append(image['domain'])

        domains.sort()
        grouped_domains = []
        for key, group in groupby(domains):
            grouped_domains.append((len(list(group)), key))
        return grouped_domains

    def print_all_domains(self):
        """
        Print list of all domains appearing in /r group. First element is
        number of times a domain appears in a posts list, second element is
        corresponding domain name.
        """
        domains = self.get_all_domains()
        for domain in sorted(domains, key=lambda x: x[0]):
            print(domain[0], domain[1])

    def count_downloadable_images(self):
        """
        Count images from post that have direct download link available.
        """
        downloadable = 0
        for post in self.images:
            if post['image']['url']: downloadable += 1
        return downloadable
