#! /usr/bin/python3

"""

Frame for file conversion..

"""

import tkinter as tk

class FilesDir:
    
    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.window = tk.Frame(master, width=100)
        self.label = tk.Label(self.window, relief='sunken')
        self.label.pack()
        self.window.pack(anchor='w', padx=5, pady=5)
        self.update()
    
    def update(self):
        """Update label text"""
        text = self.lng['label_file'] + str(self.master.sett.set_file) + '\n' +  \
                      self.lng['label_dir'] + str(self.master.sett.set_dir) + '\n' +  \
                      self.lng['label_dirout'] + str(self.master.sett.set_dirout)
                      
        self.label.configure(text=text, justify='left')
