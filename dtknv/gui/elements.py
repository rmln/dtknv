#! /usr/bin/python3

"""

Various elements for the GUI. 

"""

import os
import webbrowser

from functools import partial

import tkinter as tk
from tkinter  import filedialog

import helpers

class ExcDropDownMenu:
    """
    Create menues of the json file in the path
    folder and attach the commands/options
    for their use.

    The class is called by the main.py and 
    window_exceptions.py.

    Files loop:

    1. Get path example.json from the directory.
    2. Create a menu item.
    3. Create an item ID, and put it into the dictionary (i.e. 
       {'exaple.json': ID})
    
    
    """

    def __init__(self, parent=None, path=None, lng=None, src='from_menu', 
                 main=None):
        """Create menu"""
        self.lng = lng
        self.path = path
        self.parent = parent
        self.main = main
        self.tk_files = {}
        self.create_menu(mode=src)


    def create_menu(self, mode):
        """Create drop down menu on a button"""
        self.parent.add_command(label=self.lng['button_standardsr'], 
                              command=print)

        # Other exceptions
        files = self.get_all_exc_files()
        if files:
            for i in files.keys():
                # Hash a file name, convert it to string; then
                # assign to its name tk.IntVar() to be used
                # in menu variable.
                hashed_name_tk_int = str(hash(i))
                hashed_name_tk_int = getattr(tk, 'IntVar')()
                # If file i  was found in settings, then it is
                # in use, so set the variable:
                if (i in self.main.set.set_exc_files) and mode == 'from_menu':
                    hashed_name_tk_int.set(1)
                self.tk_files[i] = hashed_name_tk_int
                # Applies if the class was called from menu
                if mode == 'from_menu':
                    label = self.lng['button_fileexc'] % i
                    self.parent.add_checkbutton(label=label, 
                          command=partial(self.use_file, hashed_name_tk_int),
                          variable=hashed_name_tk_int)
                # Applies if the class was called from exceptions window
                elif mode == 'from_exc':
                    label = label=self.lng['button_fileexc'] % i
                    self.parent.add_command(label=label,
                          command=partial(self.load_file, i))
                else:
                    raise ValueError('Mode must be "from_menu" or "from_exc"')

    def use_file(self, e):
        """
        Set file that corresponds with menu variable
        as (not) beeing in use.
        """
        files_in_use = []
        # Loop throught the dictionary that holds
        # checkbutton values, and if the value is
        # 1, place the file name into the settings
        # list.
        for file_item in self.tk_files.keys():
            if self.tk_files[file_item].get():
                files_in_use.append(file_item)
        # Self.main comes from the main program, and it was
        # passed when whis class was called.
        self.main.set.set_exc_files = files_in_use 
                

    
    def load_file(self, f):
        """
        Send signal that f file should be loaded.
        """
        self.main.load_file_create_cells(f)
        
    
    def get_all_exc_files(self):
        """Return a list of all present exc files"""
        files = {}
        fs = helpers.getallfiles(self.path, 'json')
        if fs:
            for i in fs:
                files[helpers.filename(i)] = fs
            return files
        else:
            return False
        


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
        
            
