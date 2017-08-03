#!/usr/bin/python3


import sys
from argparse import ArgumentParser
from utils.debugtools import get_all_domains
from utils.debugtools import print_all_domains
from utils.debugtools import count_downloadable_images
from utils.downloader import download_files
from utils.consoleaccessories import is_valid_domain
from utils.consoleaccessories import is_valid_path
from domainparsers.reddit import get_all_posts


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


if __name__ == '__main__':
    verbose, pages, url, destination = parse_arguments()

    if not is_valid_domain(url):
        print('Domain must be reddit.com')
        sys.exit(0)

    if not is_valid_path(destination):
        print('Destination directory does not exist.')
        sys.exit(0)

    if verbose: print('Fetching available links...')
    if not pages: pages = 0
    images = get_all_posts(url, pages)

    if verbose: print(
        '{}/{} images available for download.'.format(
            count_downloadable_images(images) , len(images)
        )
    )
    download_files(images, destination, verbose)
    #print(images)
    #print_all_domains(get_all_domains(images))

    #print()
    #print(count_downloadable_images(images))
