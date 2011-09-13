#! /usr/bin/python3

"""

Frame for file conversion..

"""

import tkinter as tk
from gui.settings import Set

class FilesDir:
    
    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.set = Set
        self.window = tk.Frame(master, relief='groove', borderwidth=2)
        # The label for basic info
        self.label_selection = tk.Label(self.window)
        self.label_selection.pack(anchor='w', padx=5, pady=5)
        # The label about selected file or dir
        self.window.pack(anchor='w', padx=5, pady=8, fill='x')
        self.update_gui()
    
    def update_gui(self):
        """Update label text"""
        
        text = self.lng['label_file'] + str(self.set.set_file) + '\n' +  \
                      self.lng['label_dir'] + str(self.set.set_dir) + '\n' +  \
                      self.lng['label_dirout'] + str(self.set.set_dirout)
        self.label_selection.configure(text=text, justify='left')
