# Crawler for reddit

This scraper crawls all pages (or first _n_ pages) of a subreddit and detects posts that contain direct links to images. It downloads them, creates log file with links to content which has not been downloaded, and creates sqlite database containing some metadata about downloads.

Tha app can be used with its GUI or as a command line tool.

This scraper is meant to be modular, in a sense that additional parsers can be implemented to scrape content from sites where direct link to an image is not available.

Built using Python 3.5.
