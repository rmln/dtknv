#! /usr/bin/python3

"""

New interface for dtknv.

"""

import tkinter as tk
from gui.menu import Dmenu
from gui.window_exceptions import Exceptions
from gui.window_settings import Options
from gui.window_plaintext import PlainText
from gui.window_filesdir import FilesDir
        
from gui.settings import Set

class DtknvGui(tk.Frame):
    
    lng = Set.language

    def __init__(self, master=None):
        tk.Frame.__init__(self, master, height=270, width=500)
        self.sett = Set
        self.master.title('dtknv 0.5 alfa')
        self.pack(padx=0,pady=0,fill=tk.BOTH, expand=0)
        self.pack_propagate(0)
        # Variable to track opened windows
        self.master.windows_opened = []
        # Commands for interfaces
        self.master.lng = self.lng
        self.master.show_exceptions = self.show_exceptions
        self.master.show_options = self.show_options
        self.master.show_filesdir = self.show_filesdir
        self.master.show_plaintext = self.show_plaintext
        # Create and attach the menu
        self.menu = Dmenu(master)
        self.master.config(menu=self.menu.main)
        # Plain text / file conversion frames
        self.window_plaintext = PlainText(self)
        self.window_plaintext.window.forget()
        self.window_filesdir = FilesDir(self)
         # Status bar
        self.create_statusbar()
        # Shortcuts
        self.bind_all("<F2>", self.show_exceptions)
        self.bind_all("<F3>", self.show_options)
        self.bind_all("<F7>", self.show_filesdir)
        self.bind_all("<F8>", self.show_plaintext)
        # Select default mode
        self.show_filesdir()

        
    def create_statusbar(self):
        """Status bar"""
        self.status = tk.Label(self, relief='sunken', anchor='center')
        self.status.pack(side='bottom', fill='x', padx=1, pady=1)
    
    def update_status(self, text):
        """Update status text"""
        self.status.configure(text= '  ' + self.lng[text])

    def show_exceptions(self, *event):
        """Show exception window."""
        if 'window_exceptions' not in self.master.windows_opened:
            self.master.windows_opened.append('window_exceptions')
            Exceptions(self.master)

    def show_options(self, *event):
        """Show options window."""
        if 'window_options' not in self.master.windows_opened:
            self.master.windows_opened.append('window_options')
            Options(self.master)
        
    def show_filesdir(self, *event):
        """Show file conversion mode"""
        self.window_plaintext.window.forget()
        self.window_filesdir.window.pack()
        self.update_status('status_mode_filesdir')
        
    def show_plaintext(self, *event):
        """Show plain text mode"""
        self.window_filesdir.window.forget()
        self.window_plaintext.window.pack()
        self.update_status('status_mode_plaintext')
        
        
def show():
        """Show GUI"""
        root = tk.Tk()
        root.resizable(0,0)
        app = DtknvGui(master=root)
        app.mainloop()
