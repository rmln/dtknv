#! /usr/bin/python3

"""

Frame for file conversion..

"""

import tkinter as tk
from gui.settings import Set

import helpers

class FilesDir:
    """Shows and calculates information for file/directory conversion"""
    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.set = Set
        self.window = tk.Frame(master, relief='groove', borderwidth=2)
        # The label for basic info
        self.label_selection = tk.Label(self.window)
        self.label_selection.pack(anchor='w', padx=5, pady=5)
        self.window.pack(anchor='w', padx=5, pady=8, fill='x')
        self.update_gui()
    
    def update_gui(self):
        """Update label text"""
        text = self.lng['label_file'] + str(self.set.set_file) + '\n' +  \
               self.lng['label_dir'] + str(self.set.set_dir) + '\n' +  \
               self.lng['label_dirout'] + str(self.set.set_dirout) 
        # A directory is selected, so calculate the size
        # and the number of the files it contains. Skip
        # the calculation if user selected the same folder.
        if self.set.set_file != self.set.NOP:
            ext = helpers.getext(self.set.set_file)
            # See if the extension is described in the language file.
            try:
                ext = self.lng['ext_%s' % ext]
            except:
                pass
            text =   text + '\n' + self.lng['label_type'] + ext
        elif self.set.set_dir != self.set.NOP:
            # Calculate file number and size:
            #if self.set.set_dir != self.set.previous_folder:
            if 1:
                # Inform user that this migh take time:
                self.master.update_status('label_pleasewait', 0)
                # Pass the extension list
                self.master.tocyr.EXT = self.set.extensions
                # Calculate
                self.master.tocyr.RECURSIVE = self.set.set_recursive
                self.filecount, self.filesize = \
                self.master.tocyr.calculatedirsize(self.set.set_dir)
                self.set.previous_folder = self.set.set_dir
                if not self.filecount:
                    self.master.update_status('label_nosupportedfiles', 0)
                else:
                    self.master.update_status('label_ok', 0)
            text = text +   '\n' + self.lng['label_number'] % self.filecount
            text = text +  '\n' + self.lng['label_size'] %  \
                   '%0.2f' % self.filesize 
            text = text +  '\n' + self.lng['options_extensions'] + \
                   self.set.set_extensions.replace(",", ", ")
        self.label_selection.configure(text=text, justify='left')
