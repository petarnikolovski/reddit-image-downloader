#!/usr/bin/python3


"""
This is the GUI for the Reddit Downloader.
"""


from tkinter import Tk
from tkinter import Frame
from tkinter import filedialog
from tkinter import Label
from tkinter import Button
from tkinter import StringVar
from tkinter import IntVar
from tkinter import Entry
from tkinter import TOP
from tkinter import E
from tkinter import W


class RedditApp(Frame):

    def __init__(self, master=None):
        """
        Initialize the main application Frame and load it with other widgets.
        """
        super().__init__(master)
        self.pack()
        self.create_widgets()

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

        url_var = StringVar()
        pages_var = IntVar()
        self.destination_var = StringVar()

        url = Entry(paths_frame, textvariable=url_var)
        pages = Entry(paths_frame, textvariable=pages_var)
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

        btn_download = Button(
            download_frame, text='Download', command=self.download_reddit
        )
        btn_download.pack()

        download_frame.pack(side=TOP)

    def choose_directory(self):
        """
        Update the destination path entry filed with the chosen path.
        """
        destination_path = filedialog.askdirectory(initialdir='~')
        self.destination_var.set(destination_path)

    def download_reddit(self):
        pass

if __name__ == '__main__':

    root = Tk()
    root.resizable(0, 0)
    root.wm_title('(sub)Reddit Downloader')

    app = RedditApp(master=root)
    app.mainloop()
