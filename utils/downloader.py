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
from utils.logtools import write_log
from utils.politeness import get_politeness_factor
from datetime import datetime
from time import sleep


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
    # in that case, there is no need to 'clean path'
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
        token = file_obj['html_status_token']

        # to implement: check db if file was downloaded already
        if image_url and token < 3:
            if verbose: display_status(file_obj['image']['image_url'], currently_downloading, total)
            sldn = file_obj['second_level_domain_name']
            crawl_time = get_politeness_factor(sldn)

            try:
                write_file_to_filesystem(image_url, filename)
            except HTTPError as e:
                status = e.code
                print('Could not download, error status:', status)

                if status == '404':
                    if verbose: print('File not found.')
                    file_obj['last_html_status'] = status

                    write_a_record_to_db(c, file_obj, status, 0)
                    write_log(file_obj)
                    currently_downloading += 1
                elif status == '429':
                    if verbose: print('Too many requests were made to the server')
                    file_obj['last_html_status'] = status

                    write_a_record_to_db(c, file_obj, status, 0)
                    write_log(file_obj)
                    currently_downloading += 1
                else:
                    if verbose and token < 2: print('Downloading will be retried later.')
                    if verbose and token == 2: print('Could not download.')
                    file_obj['last_html_status'] = status
                    file_obj['html_status_token'] += 1

                    if token < 3:
                        files.append(file_obj)
                    else:
                        write_a_record_to_db(c, file_obj, status, 0)
                        write_log(file_obj)
            except URLError as e:
                if verbose: print('Something went wrong.')
                if verbose: print(e.reason)

                write_a_record_to_db(c, file_obj, file_obj['last_html_status'], 0)
                write_log(file_obj)
                currently_downloading += 1
            else:
                # This is else from try/except - a bit unreadable
                write_a_record_to_db(c, file_obj, 200, 1)
                currently_downloading += 1

            # If two consecutive domains are different, there is no need to
            # wait for the next download
            with suppress(IndexError):
                if file_obj['domain'] == files[1]['domain']:
                    sleep(crawl_time)
        else:
            # write_a_record_to_db(c, file_obj, file_obj['last_html_status'], 0)
            write_log(file_obj)

    conn.commit()
    conn.close()
    os.chdir(current_directory)


def write_a_record_to_db(cursor, file_obj, status, downloaded):
    """
    Insert metadata into database.
    """
    image = (
        file_obj['url'],
        file_obj['image']['image_url'],
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
