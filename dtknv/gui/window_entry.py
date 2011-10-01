#! /usr/bin/python3
"""

A message box with entry.

"""

import os
import tkinter as tk
from tkinter import messagebox

class MsgEntry:

    def __init__(self, master, lng, text, path):
        """Show a message box with an entry"""
        self.path = path
        self.entry = False
        self.lng = lng
        self.window = tk.Toplevel(master)
        self.window.resizable(0,0)
        self.main = tk.Frame(self.window, height=100, width=300)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        # Show text
        self.label = tk.Label(self.main)
        self.label.configure(text=text, justify='left', wraplength=200)
        self.label.pack(pady=5)
        # Entry
        self.var_entered = tk.StringVar()
        self.txt_text = tk.Entry(self.main, width=30, 
                                 textvariable=self.var_entered)
        self.txt_text.pack()
        self.txt_text.focus_set()
        self.txt_text.bind('<Return>', self.confirm)
        # Button
        self.btn_ok = tk.Button(self.main)
        self.btn_ok.configure(text=lng['button_ok'], command=self.confirm)
        self.btn_ok.pack(pady=5, padx=5)
         
        # Pack main frame
        self.main.pack(padx=0, pady=0, fill='both', expand=1)
        self.main.pack_propagate(0)
        self.window.grab_set()


    def close(self, *e):
        """Verify if needed, and close"""
        self.window.destroy()
        self.entry = False

    def verify(self, text):
        """See if text contains invalid character"""
        invalid_chars = """\/:*?"<>|'"""
        for i in text:
            if i in invalid_chars:
                raise ValueError
        # Check if file already exists
        if os.path.exists(os.path.join(self.path, text+'.json')):
            raise OSError
        return text

    def confirm(self, *e):
        """Conform entry end return value"""
        text = self.var_entered.get().strip()
        try:
            # See if text is valid. If not,
            # the error will block window
            # from reaching destroy() and 
            # return().
            verified = self.verify(text)
            self.window.destroy()
            self.entry = verified
        except ValueError:
            messagebox.showwarning(self.lng['label_error'],
                                   self.lng['label_invalidchar'])
        except OSError:
            messagebox.showwarning(self.lng['label_error'],
                                   self.lng['label_filealreadyexists'] \
                                       % (text + '.json'))
            
