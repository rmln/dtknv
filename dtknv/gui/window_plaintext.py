#! /usr/bin/python3

"""

Frame for plain text conversion..

"""

import tkinter as tk

class PlainText:
    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.window = tk.Frame(master)
        self.label = tk.Label(self.window, text='Plain text' )
        self.label.pack()
        self.window.pack()
