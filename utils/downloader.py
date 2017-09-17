#!/usr/bin/python3


"""
Download images from reddit. Use this in combination with Reddit class. Example:

```python3
reddit = Reddit('https://www.reddit.com/r/MemeEconomy/', 2)
reddit.get_all_posts()
images = reddit.images

downloader = Downloader(reddit, '~/memes', verbose=True)
downloader.download_files()
```
"""


__author__ = 'petarGitNik'
__copyright__ = 'Copyright (c) 2017 petarGitNik petargitnik@gmail.com'
__version__ = 'v0.1.0'
__license__ = 'MIT'
__email__ = 'petargitnik@gmail.com'
__status__ = 'Development'


import os
import sqlite3
from contextlib import suppress
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from shutil import copyfileobj
from utils.politeness import get_politeness_factor
from datetime import datetime
from time import sleep


class DownloaderListener(object):
    """
    Listents for changes in download progress. Variable should be:

    currently_at = [int]
    """

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class DownloaderException(Exception):
    """
    Raise this exception if there is something wrong with supplied path or with
    downloading process.
    """
    pass

class Downloader(object):
    """
    This class downloads files from provided source.
    """
    DB_TEMPLATE = """
    DROP TABLE IF EXISTS images;

    CREATE TABLE images (
      PostUrl TEXT,
      ImageUrl TEXT,
      Filename TEXT,
      Domain TEXT,
      PostTitle TEXT,
      CommentSectionUrl TEXT,
      PostedOn TEXT,
      LastHtmlStatusCode INTEGER,
      Downloaded INTEGER,
      DownloadDate TEXT
    );
    """

    def __init__(self, reddit, destination, verbose=False):
        """
        If variable self.downloading is set to False, download process is stopped.
        """
        self.files = reddit.images
        self.total = reddit.count_downloadable_images()
        self.destination = self.valid_destination(destination)
        self.verbose = verbose

        self.downloading = True
        self.observers = []

    def download_files(self):
        """
        This function downloads files to a specified directory. Destination
        is a path to a directory where images will be stored. If verbose is
        True, then the download status is displayed.
        """
        current_directory = os.getcwd()
        os.chdir(self.destination)

        db_path = './db.sqlite'

        # Check if db exists in destination directory
        if not self.db_exists(db_path):
            conn = self.make_connection(db_path)
            c = conn.cursor()
            c.executescript(self.DB_TEMPLATE)
            conn.commit()

        conn = self.make_connection(db_path)
        c = conn.cursor()

        # Download, deal with exception, save to db, log things...
        currently_downloading = 1
        while self.files and self.downloading:
            file_obj = self.files.popleft()

            image_url = file_obj['image']['url']
            filename = file_obj['image']['filename']
            token = file_obj['http_status_token']

            # to implement: check in db if file was downloaded already
            if image_url and token < 3:
                if self.verbose:
                    self.display_status(file_obj['image']['url'], currently_downloading, self.total)

                sldn = file_obj['second_level_domain_name']
                crawl_time = get_politeness_factor(sldn)

                try:
                    self.write_file_to_filesystem(image_url, filename)
                except HTTPError as e:
                    status = e.code
                    print('Could not download, error status:', status)

                    if status == 404:
                        if self.verbose: print('File not found.')
                        file_obj['last_http_status'] = status

                        self.write_a_record_to_db(c, file_obj, status, 0)
                        self.write_log(file_obj)
                        currently_downloading += 1
                    elif status == 429:
                        if self.verbose: print('Too many requests were made to the server')
                        file_obj['last_http_status'] = status

                        self.write_a_record_to_db(c, file_obj, status, 0)
                        self.write_log(file_obj)
                        currently_downloading += 1
                    elif status == 403:
                        if self.verbose: print('Forbidden.')
                        file_obj['last_http_status'] = status

                        self.write_a_record_to_db(c, file_obj, status, 0)
                        self.write_log(file_obj)
                        currently_downloading += 1
                    else:
                        if self.verbose and token < 2: print('Downloading will be retried later.')
                        if self.verbose and token == 2: print('Could not download.')
                        file_obj['last_http_status'] = status
                        file_obj['http_status_token'] += 1

                        if token < 3:
                            self.files.append(file_obj)
                        else:
                            self.write_a_record_to_db(c, file_obj, status, 0)
                            self.write_log(file_obj)
                except URLError as e:
                    if self.verbose: print('Something went wrong.')
                    if self.verbose: print(e.reason)

                    self.write_a_record_to_db(c, file_obj, file_obj['last_http_status'], 0)
                    self.write_log(file_obj)
                    currently_downloading += 1
                else:
                    # This is else from try/except - a bit unreadable
                    self.write_a_record_to_db(c, file_obj, 200, 1)
                    currently_downloading += 1

                # If two consecutive domains are different, there is no need to
                # wait for the next download
                with suppress(IndexError):
                    if file_obj['domain'] == self.files[1]['domain']:
                        sleep(crawl_time)
            else:
                # write_a_record_to_db(c, file_obj, file_obj['last_http_status'], 0)
                self.write_log(file_obj)

            if self.observers:
                self.update_observers(currently_at=currently_downloading)

        conn.commit()
        conn.close()
        os.chdir(current_directory)

    def write_a_record_to_db(self, cursor, file_obj, status, downloaded):
        """
        Insert metadata into database.
        """
        image = (
            file_obj['url'],
            file_obj['image']['url'],
            file_obj['image']['filename'],
            file_obj['domain'],
            file_obj['post_title'],
            file_obj['link_to_comments'],
            file_obj['posted_on'],
            status,
            downloaded,
            str(datetime.now()),
        )
        cursor.execute("INSERT INTO images VALUES(?,?,?,?,?,?,?,?,?,?)", image)

    def write_file_to_filesystem(self, url, filename):
        """
        Write a file to a file system.
        """
        with urlopen(url) as r, open(filename, 'wb') as f:
            copyfileobj(r, f)

    def display_status(self, url, currently_at, total):
        """
        Display the link of the image which is downloading, and download
        progress.
        """
        print(
            'Progress: {}/{}. Downloading: {}'.format(
                currently_at, total, url
            )
        )

    def make_connection(self, path):
        """
        Make connection to database.
        """
        return sqlite3.connect(path)

    def db_exists(self, path):
        """
        Checks if the directory/file exists on a given path.
        """
        return os.path.exists(path)

    def valid_destination(self, path):
        """
        Check if destination directory provided by the user is valid.
        """
        if os.path.exists(path):
            return path
        raise DownloaderException('Destination directory does not exist.')

    def write_log(self, post):
        """
        Write to a log file.
        """
        with open('download.log', 'a') as f:
            f.write(''.join(['-'*15, ' ', str(datetime.now()), ' ', '-'*15, '\n']))
            f.write(''.join(['Post URL -> ', post['url'], '\n']))
            f.write(''.join(['Post Comments -> ', post['link_to_comments'], '\n']))
            f.write(''.join(['Last HTTP status -> ', str(post['last_http_status']), '\n']))
            f.write('\n')

    def register(self, observer):
        """
        Register an observer for Downloader class. If observer is already present
        do not add it again.
        """
        if not observer in self.observers:
            self.observers.append(observer)

    def unregister(self):
        """
        Unregister all observers.
        """
        if self.observers:
            del self.observers[:]

    def update_observers(self, **kwargs):
        """
        Update all observers.
        """
        for observer in self.observers:
            observer.update(**kwargs)
