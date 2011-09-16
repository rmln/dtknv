#! /usr/bin/python3

"""

Frame for file conversion..

"""

import tkinter as tk
from gui.settings import Set

import helpers

class FilesDir:
    
    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.set = Set
        self.window = tk.Frame(master, relief='groove', borderwidth=2)
        # The label for basic info
        self.label_selection = tk.Label(self.window)
        self.label_selection.pack(anchor='w', padx=5, pady=5)
        # The label about selected file or 
        self.window.pack(anchor='w', padx=5, pady=8, fill='x')
        self.update_gui()
    
    def update_gui(self):
        """Update label text"""
        text = self.lng['label_file'] + str(self.set.set_file) + '\n' +  \
                      self.lng['label_dir'] + str(self.set.set_dir) + '\n' +  \
                      self.lng['label_dirout'] + str(self.set.set_dirout) 
        # Directory is selected
        if self.set.set_file != self.set.NOP:
            ext = helpers.getext(self.set.set_file)
            # See if extension is described in the language file.
            try:
                ext = self.lng['ext_%s' % ext]
            except:
                pass
            text =   text + '\n' + self.lng['label_type'] + ext
        elif self.set.set_dir != self.set.NOP:
            # Calculate file number and size:
            self.filecount, self.filesize = '?', '?'
            self.filecount, self.filesize = \
                self.master.tocyr.calculatedirsize(self.set.set_dir)
            text = text +   '\n' + self.lng['label_number'] % self.filecount
            text = text +  '\n' + self.lng['label_size'] %  self.filesize 
            text = text +  '\n' + self.lng['options_extensions'] + \
                   self.set.set_extensions.replace(",", ", ")
        self.label_selection.configure(text=text, justify='left')
