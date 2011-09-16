#! /usr/bin/python3

"""

Various elements for the GUI. 

"""

import tkinter as tk
from tkinter  import filedialog
import helpers
import os

class Browse:
    """Browse for file or folder"""
    def __init__(self, mode, path=None):
        """Start the class."""
        if path == None or '(?)':
            path = helpers.def_report_path()
        self.show(mode, path)
    
    def show(self, mode, path):
        """Open directory or file"""
        if mode == 'file':
            path = os.path.split(path)[0]
            self.path = filedialog.askopenfilenames(multiple=False)
            # On NT tkinter returns string, on Linux tuple.
            if os.name != 'nt' and self.path != '':
                self.path = self.path[0]                
        elif mode == 'dir':
            self.path = filedialog.askdirectory(initialdir=path)
        else:
            raise ValueError("Mode must be 'dir' of 'file'")
        
            
