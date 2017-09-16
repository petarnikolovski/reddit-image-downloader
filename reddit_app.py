#!/usr/bin/python3


"""
This is the GUI for the Reddit Downloader.
"""


from domainparsers.reddit import Reddit
from domainparsers.reddit import RedditException
from utils.downloader import Downloader
from utils.downloader import DownloaderException

import threading
import queue
from queue import Queue

from tkinter import Tk
from tkinter import Toplevel
from tkinter import TclError
from tkinter import Message
from tkinter import Menu
from tkinter import Frame
from tkinter import filedialog
from tkinter import font
from tkinter import Label
from tkinter import Button
from tkinter import messagebox
from tkinter import StringVar
from tkinter import IntVar
from tkinter import Entry
from tkinter import DISABLED
from tkinter import NORMAL
from tkinter import TOP
from tkinter import E
from tkinter import W
from tkinter.ttk import Progressbar


__author__ = 'petarGitNik'
__copyright__ = 'Copyright (c) 2017 petarGitNik petargitnik@gmail.com'
__version__ = 'v0.1.0'
__license__ = 'MIT'
__email__ = 'petargitnik@gmail.com'
__status__ = 'Development'


class RedditApp(Frame):

    def __init__(self, master=None):
        """
        Initialize the main application Frame and load it with other widgets.
        """
        super().__init__(master)
        self.root = master
        self.pack()
        self.setup_main_frame()
        self.create_menubar()
        self.create_widgets()

    def setup_main_frame(self):
        self.root.resizable(0, 0)
        self.root.wm_title('(sub)Reddit Downloader')

    def create_menubar(self):
        menubar = Menu(self.root)
        menubar.add_command(label='About', command=AboutWindow.about)
        menubar.add_command(label='Exit', command=self.root.quit)
        self.root.config(menu=menubar)

    def create_widgets(self):
        """
        Create widgets to populate the applications frame.
        """
        # URL, Pages, Destination
        paths_frame = Frame(self)

        lbl_url = Label(paths_frame, text='URL:')
        lbl_pages = Label(paths_frame, text='Pages:')
        lbl_destination = Label(paths_frame, text='Destination:')

        lbl_pages_help = Label(
            paths_frame, text='(Leave zero to crawl all pages)'
        )

        self.url_var = StringVar()
        self.pages_var = IntVar()
        self.destination_var = StringVar()

        url = Entry(paths_frame, textvariable=self.url_var)
        pages = Entry(paths_frame, textvariable=self.pages_var)
        destination = Entry(paths_frame, textvariable=self.destination_var)

        btn_chooser = Button(
            paths_frame, text='Destination', command=self.choose_directory
        )

        pad_x = 5
        pad_y = 7

        r = 0
        lbl_url.grid(row=r, column=0, sticky=E, padx=pad_x, pady=pad_y)
        url.grid(row=r, column=1)

        r += 1
        lbl_pages.grid(row=r, column=0, sticky=E)
        pages.grid(row=r, column=1, padx=pad_x, pady=pad_y)
        lbl_pages_help.grid(row=r, column=2)

        r += 1
        lbl_destination.grid(row=r, column=0, sticky=E)
        destination.grid(row=r, column=1, padx=pad_x, pady=pad_y)
        btn_chooser.grid(row=r, column=2, sticky=E+W)

        paths_frame.pack(side=TOP, padx=10, pady=10)

        # Download button
        download_frame = Frame(self)

        self.btn_download = Button(
            download_frame, text='Download', command=self.download_reddit
        )
        self.btn_download.pack(padx=10, pady=10)

        download_frame.pack(side=TOP)

        # Progress label
        progress_info = Frame(self)

        self.lbl_progress_info = Label(progress_info, text='')
        self.lbl_progress_info.pack(padx=10, pady=10)

        progress_info.pack(side=TOP)

    def add_progress_bar(self):
        """
        Add progress bar to root frame.
        """
        self.progress_frame = Frame(self)

        self.progress_bar = Progressbar(
            self.progress_frame, orient='horizontal', length=400, mode='indeterminate'
        )
        #self.progress_bar = Progressbar(
        #    progress_frame, orient='horizontal', length=400, mode='determinate'
        #)
        self.progress_bar.pack(padx=10, pady=10)
        self.progress_frame.pack(side=TOP)

    def remove_progress_bar(self):
        """
        Remove progress bare from root frame.
        """
        self.progress_bar.destroy()
        self.progress_frame.destroy()

    def change_progress_label(self, text):
        """
        Change text of progress bar label.
        """
        self.lbl_progress_info.configure(
            text=text, fg='red', font=(font.BOLD)
        )

    def choose_directory(self):
        """
        Update the destination path entry filed with the chosen path.
        """
        destination_path = filedialog.askdirectory(initialdir='~')
        self.destination_var.set(destination_path)

    def download_reddit(self):
        """
        Download images from subreddit.
        """
        try:
            reddit = Reddit(self.url_var.get(), self.pages_var.get())
        except RedditException:
            messagebox.showerror('Error', 'Please input valid link')
            return
        except TclError:
            messagebox.showerror('Error', 'Please input only whole numbers')
            return
        except Exception as e:
            print(e)
            messagebox.showerror('Error', 'Something went wrong with Reddit.')
            return

        try:
            self.downloader = Downloader(reddit, self.destination_var.get())
        except DownloaderException:
            messagebox.showerror('Error', 'Invalid download path')
            return
        except Exception as e:
            print(e)
            messagebox.showerror('Error', 'Something went wrong with Downloader.')
            return

        self.btn_download.configure(text='Cancel', command=self.cancel_download)
        self.change_progress_label('Fetching data...')

        self.add_progress_bar()
        self.progress_bar.start()
        self.queue = Queue()

        DownloadThread(self.queue, reddit, self.downloader).start()
        self.root.after(100, self.process_queue)

    def process_queue(self):
        """
        Stop the progress bar if the thread has yielded control. If download was
        canceled, re-enable download button only after thread has yielded control.
        """
        try:
            msg = self.queue.get(0)

            if self.btn_download['state'] == DISABLED:
                self.btn_download.configure(state=NORMAL)

            print(msg)
        except queue.Empty:
            self.root.after(100, self.process_queue)

    def cancel_download(self):
        """
        Cancel download process.
        """
        self.downloader.downloading = False
        self.btn_download.configure(text='Download', command=self.download_reddit)
        self.remove_progress_bar()
        self.change_progress_label('Download canceled.')
        self.btn_download.configure(state=DISABLED)


class DownloadThread(threading.Thread):
    """
    Start a download thread.
    """

    def __init__(self, queue, reddit, downloader):
        threading.Thread.__init__(self)
        self.queue = queue

        self.reddit = reddit
        self.downloader = downloader

    def run(self):
        """
        Fetching of download links and downloading process are located here.
        """
        self.reddit.get_all_posts()
        self.downloader.download_files()

        self.queue.put('Downloading finished')


class AboutWindow(object):
    """
    This is the Reddit Image Downloader. Paste URL into corresponding field,
    choose path to download directory, and choose how many pages of a subreddit
    you want to crawl.

    The application was made by petarGitNik (https://github.com/petargitnik).
    """

    @classmethod
    def about(cls):
        """
        Launch about window.
        """
        top = Toplevel()
        top.resizable(0, 0)
        top.title('About the application')

        about_message = AboutWindow.__doc__
        msg = Message(top, text=about_message)
        msg.pack()

        btn_dismiss = Button(top, text='Dismiss', command=top.destroy)
        btn_dismiss.pack()


if __name__ == '__main__':

    root = Tk()
    app = RedditApp(master=root)
    app.mainloop()
