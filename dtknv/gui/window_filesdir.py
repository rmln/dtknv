#! /usr/bin/python3

"""

Frame for file conversion. It holds labels and a button
to start conversion, enablen if conditions for running
are fulfilled.

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
        self.window = tk.Frame(master, relief='groove', borderwidth=0)
        # The label for basic info
        self.label_selection = tk.Label(self.window)
        self.label_selection.pack(anchor='w', padx=5, pady=5)
        # The conversion button
        self.btn_convert = tk.Button(self.window, 
                                     text=self.lng['button_convert'], 
                                     width=20, state='disabled',
                                     command=self.master.convert)
        self.btn_convert.pack(side='bottom', pady=5)

        self.window.pack(fill='both', anchor='w', expand=1)
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
            if 1: # overrided for time being
                # Inform user that this migh take time:
                self.master.update_status('label_pleasewait', 0)
                # Pass the extension list, depending on the
                # conversion mode:
                if self.set.set_convmode == 'tolat':
                    extensions = self.set.set_extensions
                else:
                    extensions = self.set.set_extensions_tocyr
                self.master.tocyr.EXT = extensions
                # Calculate
                self.master.tocyr.RECURSIVE = self.set.set_recursive
                self.filecount, self.filesize = \
                self.master.tocyr.calculatedirsize(self.set.set_dir)
                self.set.previous_folder = self.set.set_dir
                if not self.filecount:
                    self.master.update_status('label_nosupportedfiles', 0)
                else:
                    self.master.update_status('label_ok', 0)
            # The number of files
            text = text +   '\n' + self.lng['label_number'] % self.filecount
            # The size of file(s)
            text = text +  '\n' + self.lng['label_size'] %  \
                   '%0.2f' % self.filesize
            # The list of recognised extensions
            text = text +  '\n' + self.lng['options_extensions'] + \
                   extensions.replace(",", ", ")
            # Conversion mode
            text = text +  '\n' + self.lng['label_conv%s' % \
                                               self.set.set_convmode]
        self.label_selection.configure(text=text, justify='left')
