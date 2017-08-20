#!/usr/bin/python3


"""
This is the GUI for the Reddit Downloader.
"""


from tkinter import Tk
from tkinter import Frame
from tkinter import filedialog


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
        pass


if __name__ == '__main__':

    root = Tk()
    root.resizable(0, 0)
    root.wm_title('(sub)Reddit Downloader')

    app = RedditApp(master=root)
    app.mainloop()
