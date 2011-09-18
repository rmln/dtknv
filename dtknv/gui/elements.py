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
        
            
