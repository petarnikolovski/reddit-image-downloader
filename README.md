# Crawler for reddit

This scraper crawls all the pages (or first _n_ pages) of an /r group and detects posts that contain direct links to images. It downloads them, creates log file with links to content which was not downloaded, and creates sqlite database containing some metadata about downloads.

The app is a command line tool for now, and it lacks object oriented design.

This scraper is meant to be modular, in a sense that additional parsers can be implemented to scrape content from sites where direct link to image is not available. Some big changes must be made though. This is due to the fact that some imgur links may lead to galleries.

Built using Python 3.5.
