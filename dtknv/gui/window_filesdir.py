#! /usr/bin/python3

"""

Frame for file conversion. It holds labels and a button
to start conversion, enabled if conditions for running
are fulfilled.

"""

#
#    Copyright (C) 2011  Romeo Mlinar (mlinar [a] languagebits.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import tkinter as tk

import helpers

class FilesDir:
    """
    Shows and calculates information for file/directory conversion.
    """
    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.set = self.master.main_settings
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
        """
        Update label text,  with info about paths and file 
        size and number.
        """
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
            # TODO: Add an option to override this.
            #if self.set.set_dir != self.set.previous_folder:
            if 1: # overrided for time being
                # Inform user that this migh take time:
                self.master.update_status('label_pleasewait', 0)
                # Pass the extension list, depending on the
                # conversion mode:
                if self.set.set_convmode == 'tolat':
                    extensions = self.set.set_extensions
                    self.master.tocyr.EXT = self.set.extensions
                else:
                    extensions = self.set.set_extensions_tocyr
                    self.master.tocyr.EXT = self.set.extensions_tocyr
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
