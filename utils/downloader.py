#!/usr/bin/python3


"""
Downloads files.
"""


import os
import sqlite3
from contextlib import suppress
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from shutil import copyfileobj
from utils.consoleaccessories import is_valid_path
from utils.consoleaccessories import clean_path
from utils.debugtools import count_downloadable_images
from utils.politeness import get_politeness_factor
from time import sleep


DB_TEMPLATE = """
DROP TABLE IF EXISTS images;

CREATE TABLE images (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
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

def download_files(files, destination, verbose):
    """
    This function downloads files to a specified directory. Destination
    is a path to a directory where images will be stored. If verbose is
    True, then the download status is displayed.
    """
    current_directory = os.getcwd()
    os.chdir(destination)

    # Since directory has changed, you do not have to use abs path for db
    # you could use './db.sqlite'
    # in that case, there is no need to clean path
    db_path = ''.join([clean_path(destination), '/db.sqlite'])

    # Check if db exists in destination directory
    if not is_valid_path(db_path):
        conn = make_connection(db_path)
        c = conn.cursor()
        c.executescript(DB_TEMPLATE)
        conn.commit()

    conn = make_connection(db_path)
    c = conn.cursor()

    # Download, deal with exception, save to db, log things...
    total = count_downloadable_images(files)
    currently_downloading = 1
    while files:
        file_obj = files.popleft()

        image_url = file_obj['image']['image_url']
        filename = file_obj['image']['filename']
        if image_url:
            if verbose: display_status(file_obj['image']['image_url'], currently_downloading, total)
            sldn = file_obj['second_level_domain_name']
            crawl_time = get_politeness_factor(sldn)

            # skip downloading if file is already downloaded
            try:
                write_file_to_filesystem(image_url, filename)
            except HTTPError as e:
                status = e.code
                print('Could not downloade, error status:', status)

                if status == '404':
                    print('File not found.')
                    # log missing, and write to db
                    currently_downloading += 1
                elif status == '429':
                    print('Too many requests were made to the server')
                    # does not return file at the end of the deque
                    currently_downloading += 1
                else:
                    print('Downloading will be retried later.')
                    # log this
                    files.append(file_obj)
            except URLError as e:
                print('Something went wrong with connection.')
                print('Connection may have been refused.')
            else:
                pass
                currently_downloading += 1

            # If two consecutive domains are different, there is no need to
            # wait for the next download
            with suppress(IndexError):
                if file_obj['domain'] == files[1]['domain']:
                    sleep(crawl_time)

    conn.close()
    os.chdir(current_directory)


def write_file_to_filesystem(url, filename):
    """
    Write a file to a file system.
    """
    with urlopen(url) as r, open(filename, 'wb') as f:
        copyfileobj(r, f)


def display_status(url, currently_at, total):
    """
    Display the link of the image which is downloading, and download
    progress.
    """
    print(
        'Progress: {}/{}.\tDownloading: {}'.format(
            currently_at, total, url
        )
    )


def make_connection(path):
    """
    Make connection to database.
    """
    return sqlite3.connect(path)
