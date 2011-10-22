#! /usr/bin/python3

"""

Frame for plain text conversion. The frame has it own
convertor instance, independent from the one used in file
conversion.

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
from srpismo.cyrconv import CirConv

class PlainText:
    """
    Plain text conversion, by taking the entry form text field
    and passing it to cyrconv.
    """
    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.window = tk.Frame(master)
        self.buttons()
        self.text()
        self.window.pack()
        # Class for conversion:
        self.convert = CirConv()

    def text(self):
        """Create a text field with a scroll bar"""
        frame_text = tk.Frame(self.window)
        field_text = tk.Text(frame_text)
        
        scrollbar = tk.Scrollbar(frame_text, width=15)
        scrollbar.config(command=field_text.yview)
        field_text.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side='right', fill='y')
        field_text.pack()
        frame_text.pack(side='top')
        
        #Make text field public
        self.field_text = field_text

    def clear_text_field(self, *e):
        """
        Erase text from the text field. 
        """
        self.field_text.delete('0.1', 'end')


    def get_text_field(self, *e):
        """
        Get text from the text field. 
        """
        return(self.field_text.get('0.1', 'end'))

    def insert_text(self, text):
        """
        Insert text into the text field, erasing first.
        """
        self.clear_text_field()
        self.field_text.insert('end', text)


    def to_cyrillic(self, *e):
        """
        Get text from text field, convert it to Cyrillic and
        return it to the textfield.
        """
        self._convert('to_cyrillic')


    def to_latin(self, *e):
        """
        Get text from text field, convert it to Cyrillic and
        return it to the textfield.
        """
        self._convert('to_latin')
    

    def _convert(self, mode):
        """
        Call conversion class.
        """
        # Get exception files from settings
        files = self.master.set.set_exc_files
        # Load them into the class
        self.convert.path = self.master.set.DEFEXCPATH
        self.convert.load_exceptions(files)
        text = self.get_text_field()[:-1]
        self.convert.text = text
        if mode == 'to_cyrillic':
            self.convert.convert_to_cyrillic()
        elif mode == 'to_latin':
            self.convert.convert_to_latin()
        else:
            raise ValueError('Mode must be "to_cyrillic" or "to_latin"')
        self.insert_text(self.convert.result)

    
    def buttons(self):
        """Create buttons"""
        frame_buttons = tk.Frame(self.window)
        btn_tolatin = tk.Button(frame_buttons, 
                                text=self.lng['button_erase'],
                                command=self.clear_text_field)
        btn_tocyr = tk.Button(frame_buttons,
                              text=self.lng['button_tocyr'],
                              command=self.to_cyrillic)
        btn_erase = tk.Button(frame_buttons,
                              text=self.lng['button_tolat'],
                              command=self.to_latin)
        btn_tolatin.pack(side='left', padx=3, pady=3)
        btn_erase.pack(side='left', padx=3, pady=3)
        btn_tocyr.pack(side='left', padx=3, pady=3)
        frame_buttons.pack(side='bottom')
