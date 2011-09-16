#! /usr/bin/python3

"""

New interface for dtknv.

"""

import tkinter as tk
from tkinter import messagebox

from gui.menu import Dmenu
from gui.window_exceptions import Exceptions
from gui.window_settings import Options
from gui.window_plaintext import PlainText
from gui.window_filesdir import FilesDir

from convert import tocyr
from convert.tocyr import ToCyr
from srpismo.cyrconv import CirConv

        
from gui.settings import Set

class DtknvGui(tk.Frame):
    
    lng = Set.language

    def __init__(self, master=None):
        tk.Frame.__init__(self, master, height=270, width=500)
        self.set = Set
        self.master.title('dtknv 0.5 alfa')
        self.pack(padx=0,pady=0,fill=tk.BOTH, expand=0)
        self.pack_propagate(0)
        self.master.windows_opened = []
        # Conversion class
        self.tocyr = ToCyr()
        # Commands for interfaces
        self.master.lng = self.lng
        self.master.show_exceptions = self.show_exceptions
        self.master.show_options = self.show_options
        self.master.show_filesdir = self.show_filesdir
        self.master.show_plaintext = self.show_plaintext
        self.master.update_gui = self.update_gui
        self.master.kill_program = self.kill_program
        # Status bar
        self.create_statusbar()
        # Create and attach the menu
        self.menu = Dmenu(master)
        self.master.config(menu=self.menu.main)
        # Plain text / file conversion frames
        self.window_plaintext = PlainText(self)
        self.window_plaintext.window.forget()
        self.window_filesdir = FilesDir(self)
        # The conversion button
        self.btn_convert = tk.Button(self, text=self.lng['button_convert'], 
                                     width=20, state='disabled',
                                     command=self.convert)
        self.btn_convert.pack(side='bottom', pady=5)
        # Shortcuts
        self.bind_all("<F2>", self.show_exceptions)
        self.bind_all("<F3>", self.show_options)
        self.bind_all("<F7>", self.show_filesdir)
        self.bind_all("<F8>", self.show_plaintext)
        # Select default mode
        self.show_filesdir()

        
    def create_statusbar(self):
        """Status bar"""
        self.status = tk.Label(self, relief='sunken', anchor='w')
        self.status.pack(side='bottom', fill='x', padx=1, pady=1)
    
    def update_status(self, text, append=True):
        """Update status text"""
        if append:
            self.status.configure(text= '  ' + self.lng[text])
        else:
            self.status.configure(text=self.lng[text])
        # Update this widget, so the message is visible
        # during loops.
        self.status.update()    
        
    def show_exceptions(self, *event):
        """Show the exceptions window."""
        if 'window_exceptions' not in self.master.windows_opened:
            self.master.windows_opened.append('window_exceptions')
            Exceptions(self.master)

    def show_options(self, *event):
        """Show the options window."""
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
    
    def update_gui(self):
        """Update GUI stuff"""
        # Check if in and out dirs are the same,
        # and ask for the confirmation to continue.
        self.explicit_save_in_same_folder()
        # Save and load the settings, and then update the
        # gui:
        self.set.reload()
        self.window_filesdir.update_gui()
        # If everything is ready, enable the convert
        # button and bindig:
        if self.are_paths_ready():
            self.btn_convert.configure(state='normal')
            self.bind_all("<F5>", self.convert)
            self.btn_convert.configure(state='normal')
            self.update_status('label_ready', append=0)
        else:
            self.bind_all("<F5>", None)
            
    def explicit_save_in_same_folder(self):
        """ Converted files can be saved in the same folder
        only if explicitly allowed. The message to allow
        it will pop up if 1) the paths are same 2) the option
        to save in same folder is off."""
        same = self.set.set_dir ==  self.set.set_dirout
        selected = (self.set.set_dir != self.set.NOP) and \
                   (self.set.set_dirout != self.set.NOP)
        if (same and selected) and not self.set.set_sameinout:
            ask = messagebox.askyesno('', self.lng['msg_sameinout'])
            if ask:
                self.set.set_sameinout = 1
            else:
                # If a user declines to save in the same
                # folder, reset the output folder:
                self.set.set_dirout = self.set.NOP

    def are_paths_ready(self):
        """Check if paths are ready"""
        input_path_selected = (self.set.set_dir != self.set.NOP) or \
                              (self.set.set_file != self.set.NOP)
        output_path_selected = self.set.set_dirout != self.set.NOP
        if input_path_selected and output_path_selected:
            return True
        else:
            return False
    
    def convert(self, *e):
        """Start the convertsion"""
        # Disable the button and remove the bind
        self.btn_convert.configure(state='disabled')
        self.bind_all("<F5>", None)
        print("I'm converting now...")
        print('ENC', self.set.set_encoding)
        print('file', self.set.set_file)
        print('dirout', self.set.set_dirout)
        print('dir', self.set.set_dir)
        print('recursive', self.set.set_recursive)
        print('verbose', self.set.set_verbose)
        print('failsafe', self.set.set_failsafe)
        print('noram', self.set.set_noram)
        print('convertnames', self.set.set_convertnames)
        print('reportpath', self.set.set_reportpath)
        print('reportname', self.set.set_reportname)
        print('extensions', self.set.extensions)
        print('sameinout', self.set.set_sameinout)

    def kill_program(self, *e):
        """Save settings and exit."""
        self.set.save()
        self.destroy()
        self.master.destroy()
                    
        
def show():
        """Show GUI"""
        root = tk.Tk()
        root.resizable(0,0)
        app = DtknvGui(master=root)
        root.protocol("WM_DELETE_WINDOW", app.kill_program)
        app.mainloop()
