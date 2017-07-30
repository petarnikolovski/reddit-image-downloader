#!/usr/bin/python3

from argparse import ArgumentParser

def parse_arguments():
    """
    Parse input arguments of the program. Two positional arguments are
    mandatory: 'URL' and destination 'directory'. 'verbose' is optional.
    Example:

    crawlddit.py -v https://www.reddit.com/r/MemeEconomy/ ./dank_memes

    For more information type:

    crawlddit.py --help
    """
    parser = ArgumentParser(dectiption='reddit /r downloader')

    parser.add_argument('-v', '--verbose',
                        help='display download progress and information',
                        action='store_true')
    parser.add_argument('URL', help='source link')
    parser.add_argument('directory', help='destination directory')

    args = parser.parse_args()

    return (args.verbose, args.URL, args.directory)


if __name__ == '__main__':
    verbose, url, destination = parse_arguments()
