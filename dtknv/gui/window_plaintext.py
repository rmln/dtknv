#! /usr/bin/python3

"""

Frame for plain text conversion..

"""

import tkinter as tk

class PlainText:
    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.window = tk.Frame(master)
        self.buttons()
        self.text()
        self.window.pack()

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
    
    def buttons(self):
        """Create buttons"""
        frame_buttons = tk.Frame(self.window)
        btn_tolatin = tk.Button(frame_buttons, text=self.lng['button_erase'], command=print)
        btn_tocyr = tk.Button(frame_buttons, text=self.lng['button_tocyr'], command=print)
        btn_erase = tk.Button(frame_buttons, text=self.lng['button_tolat'], command=print)
        btn_tolatin.pack(side='left', padx=3, pady=3)
        btn_erase.pack(side='left', padx=3, pady=3)
        btn_tocyr.pack(side='left', padx=3, pady=3)
        frame_buttons.pack(side='bottom')