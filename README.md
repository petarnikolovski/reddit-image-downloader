# Crawler for reddit

This scraper crawls all the pages (or first _n_ pages) of a subreddit and detects posts that contain direct links to images. It downloads them, creates log file with links to content which has not been downloaded, and creates sqlite database containing some metadata about downloads.

The app is a command line tool for now.

This scraper is meant to be modular, in a sense that additional parsers can be implemented to scrape content from sites where direct link to an image is not available. Some big changes must be made though. This is due to the fact that some imgur links may lead to galleries. Oh, and there is also a problem with imgur's _.gifv_ (app detects it as gif despite not being a gif).

Built using Python 3.5.

## TODO

* Create GUI on top of the app (tkinter)
