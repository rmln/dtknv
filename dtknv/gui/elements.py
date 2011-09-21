#! /usr/bin/python3

"""

Various elements for the GUI. 

"""

import os
import webbrowser

import tkinter as tk
from tkinter  import filedialog

import helpers


class Link:
    """Clicable HTTP link that opens default browser"""
    def __init__(self, master, text='text', link='localhost',
                 anchor='w', padx=10, pady=1):
        self.link = link
        self.label = tk.Label(master)
        self.label.configure(text=text, fg='blue', cursor='hand1')
        self.label.bind('<Button-1>', self.browse)
        self.label.pack(anchor=anchor, padx=padx, pady=pady)

    def browse(self, *e):
        """Open browser"""
        browser = webbrowser.get()
        browser.open(self.link)


class Browse:
    """Browse for file or folder"""
    def __init__(self, mode, initpath=None):
        """Start the class."""
        if initpath == (None or '(?)'):
            initpath = helpers.def_report_path()
        self.show(mode, initpath)
    
    def show(self, mode, initpath):
        """Open directory or file"""
        if mode == 'file':
            path = os.path.split(initpath)[0]
            self.path = filedialog.askopenfilenames(multiple=False)
            # On NT tkinter returns string, on Linux tuple.
            if os.name != 'nt' and self.path != '':
                self.path = self.path[0]                
        elif mode == 'dir':
            self.path = filedialog.askdirectory(initialdir=initpath)
        else:
            raise ValueError("Mode must be 'dir' of 'file'")
        
            
