#! /usr/bin/python3

"""

Frame for file conversion..

"""

import tkinter as tk

class FilesDir:
    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.window = tk.Frame(master, bg='yellow', width=100)
        self.label = tk.Label(self.window, text='Files and directories' , bg='red')
        self.label.pack()
        self.window.pack()
