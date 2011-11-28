#! /usr/bin/python3

"""

Just an "about" window.

"""

__version__ = '0.5'

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


import os
import time
import tkinter as tk

from gui.elements import Link

import version
import helpers

class AboutWindow:
    
    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.window = tk.Toplevel(master)
        self.window.resizable(0,0)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.main = tk.Frame(self.window, height=100, width=400)
        self.main.pack(padx=0, pady=0, fill='both', expand=1)
        self.window.title(self.lng['window_about'])
        self.buttons()
        self.widgets()
        

    def widgets(self):
        """
        Create a label for text.
        """
        # Program title
        self.label_title = tk.Label(self.main, justify='left')
        self.label_title.configure(text=self.lng['label_about_name'],
                                   font=('Ubuntu', 16))
        self.label_title.pack(padx=20, pady=5, anchor='w')
        # About text
        self.about_text = tk.Label(self.main, justify='left', wraplength=400)
        # Format about text
        text = self.lng['label_about_desc'] % version.__version__ + '\n\n'
        text = text + self.lng['label_about_license'] + ' '
        text = text + self.lng['label_about_mail'].replace('--a--', '@') + '\n\n'
        text = text + self.lng['label_about_author'] + ' © ' +  \
               self.lng['label_about_year']
        self.about_text.configure(text=text)
        self.about_text.pack(padx=20, pady=10, anchor='w')
        # Links
        Link(self.window, text='Language bits', 
             link=r'http://www.languagebits.com/',
             padx=20)

    
    def buttons(self):
        """
        Create buttons.
        """
        frame_buttons = tk.Frame(self.window)
        btn_close = tk.Button(frame_buttons, 
                                text=self.lng['button_close'], 
                                command=self.close)
        btn_close.pack(side='left', padx=3, pady=10)
        frame_buttons.pack(side='bottom')


    def close(self, *e):
        """
        Close this window.
        """
        self.master. windows_opened.remove('window_about')
        self.window.destroy()
