#! /usr/bin/python3

"""

New, menu-based interface for dtknv. 

It consists of several parts:

DtknvGui   - main frame that holds everything else;
Dmenu      - menus,
Options    - top window with options,
PlainText  - a frame with a text field, used for plain text
             conversions,
FilesDir   - a frame with labels/info for converting files, and
             a button that starts the conversion,
NewVersion - a small top window with links to download new version,
             if available. 

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



# BUGS/TODO
#
# - Error in single file conversion (re self.window_filesdir.filecount)
#

import tkinter as tk
from tkinter import messagebox

import time
import threading

from gui.menu import Dmenu
from gui.window_exceptions import Exceptions
from gui.window_settings import Options
from gui.window_plaintext import PlainText
from gui.window_filesdir import FilesDir
from gui.window_checknew import NewVersion
from gui.window_about import AboutWindow

from convert import tocyr
from convert.tocyr import ToCyr
from srpismo.cyrconv import CirConv

from gui.settings import Settings

import version

import helpers

class DtknvGui(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master, height=270, width=500)
        # Settings
        self.main_settings = Settings()
        self.set = self.main_settings
        self.lng = self.set.language
        self.master.title(self.lng['label_about_name'] + ' ' + \
                              version.__version__)
        self.pack(padx=0,pady=0,fill=tk.BOTH, expand=0)
        self.pack_propagate(0)
        self.master.windows_opened = []
        # Conversion class
        self.tocyr = ToCyr()
        # Commands for interfaces
        self.master.main_settings = self.main_settings
        self.master.lng = self.lng
        self.master.show_exceptions = self.show_exceptions
        self.master.show_options = self.show_options
        self.master.show_filesdir = self.show_filesdir
        self.master.show_plaintext = self.show_plaintext
        self.master.show_newversion = self.show_newversion
        self.master.show_aboutwindow = self.show_aboutwindow
        self.master.convert = self.convert
        self.master.update_gui = self.update_gui
        self.master.kill_program = self.kill_program
        # Status bar
        self.create_statusbar()
        # Create and attach the menu
        self.menu = Dmenu(master)
        self.master.config(menu=self.menu.main)
        # This is called in window_exceptions.py to 
        # recreate exceptions menu:
        self.master.recreate_excetions_menu = self.menu.create_exceptions_menu
        # Plain text / file conversion frames
        self.window_plaintext = PlainText(self)
        self.window_plaintext.window.forget()
        self.window_filesdir = FilesDir(self)
        # Shortcuts
        self.bind_all("<F2>", self.show_exceptions)
        self.bind_all("<F3>", self.show_options)
        self.bind_all("<F7>", self.show_filesdir)
        self.bind_all("<F8>", self.show_plaintext)
        # Select default mode
        #self.show_plaintext()
        self.show_filesdir()

        
    def create_statusbar(self):
        """
        Status bar.
        """
        self.status = tk.Label(self, relief='sunken', anchor='w')
        self.status.pack(side='bottom', fill='x', padx=1, pady=1)
    

    def update_status(self, text, append=True):
        """
        Update status text.
        """
        if append:
            self.status.configure(text= '  ' + self.lng[text])
        else:
            self.status.configure(text=self.lng[text])
        # Update this widget, so the message is visible
        # during loops.
        self.status.update()
        

    def show_newversion(self, *e):
        """
        Check if new version is available, and if yes
        show details and the download link.
        """
        if 'window_newversion' not in self.master.windows_opened:
            self.master.windows_opened.append('window_newversion')
            NewVersion(self.master)
        
        
    def show_exceptions(self, *event):
        """
        Show the exceptions window.
        """
        if 'window_exceptions' not in self.master.windows_opened:
            self.master.windows_opened.append('window_exceptions')
            Exceptions(self.master)

            
    def show_aboutwindow(self, *e):
        """
        Show About window
        """
        if 'window_about' not in self.master.windows_opened:
            self.master.windows_opened.append('window_about')
            AboutWindow(self.master)


    def show_options(self, *event):
        """
        Show the options window.
        """
        if 'window_options' not in self.master.windows_opened:
            self.master.windows_opened.append('window_options')
            Options(self.master)

        
    def show_filesdir(self, *event):
        """
        Show file conversion mode.
        """
        self.window_plaintext.window.forget()
        self.window_filesdir.window.pack(anchor='w', fill='both', expand=1)
        self.update_status('status_mode_filesdir')

        
    def show_plaintext(self, *event):
        """
        Show plain text mode.
        """
        self.window_filesdir.window.forget()
        self.window_plaintext.window.pack()
        self.update_status('status_mode_plaintext')

    
    def update_gui(self):
        """
        Update GUI stuff.
        """
        #print('-'*20)
        #print('dirout', self.set.set_dirout)
        #print('dir', self.set.set_dir)
        #print('file', self.set.set_file)
        # Check if in and out dirs are the same,
        # and ask for the confirmation to continue.
        self.explicit_save_in_same_folder()
        # Refresh extensions:
        if self.set.set_convmode == 'tolat':
            self.tocyr.EXTENSIONS = self.set.extensions
        else:
            self.tocyr.EXTENSIONS = self.set.extensions_tocyr
        # If file is slected, but the converson mode cannot be
        # applied to it, reset the path.
        self.check_allowed_extensions()
        # Save and load the settings, and then update the
        # gui:
        self.set.reload()
        self.window_filesdir.update_gui()
        self.status.configure(bg='gray')
        # By default, block the run button.
        self.window_filesdir.btn_convert.configure(state='disabled')
        # If everything is ready, enable the convert
        # button and bindig:
        if self.are_paths_ready():
            self.window_filesdir.btn_convert.configure(state='normal')
            self.bind_all("<F5>", self.convert)
            self.update_status('label_ready', append=0)
        else:
            self.bind_all("<F5>", None)
        # Unbind click in status bar
        self.status.unbind('<Button-1>')
        self.status.configure(cursor='arrow')


    def check_allowed_extensions(self):
        """
        Check if file extension is allowed in the
        conversion mode.
        """
        # If file is slected, but the converson mode cannot be
        # applied to it, reset the path.
        file_selected = self.set.set_file != self.set.NOP
        if file_selected and (self.set.set_convmode == 'tocyr'):
            if helpers.getext(self.set.set_file) not in \
                    self.tocyr.EXTENSIONS:
                self.set.set_file = self.set.NOP
                messagebox.showwarning('',
                                   self.lng['msg_extension_not_supported'])
        

    def explicit_save_in_same_folder(self):
        """
        Converted files can be saved in the same folder
        only if explicitly allowed. The message to allow
        it will pop up if 1) the paths are the same 2) the option
        to save in same folder is off.
        """
        same = self.set.set_dir ==  self.set.set_dirout
        selected = (self.set.set_dir != self.set.NOP) and \
                   (self.set.set_dirout != self.set.NOP)
        if (same and selected) and not self.set.set_sameinout:
            ask = messagebox.askyesno('', self.lng['msg_sameinout'])
            if ask:
                self.set.set_sameinout = 1
            else:
                # If user declines to save in the same
                # folder, reset the output folder.
                self.set.set_dirout = self.set.NOP


    def are_paths_ready(self):
        """
        Check if paths are ready.
        """
        input_path_selected = (self.set.set_dir != \
                                   self.set.NOP) or \
                              (self.set.set_file != \
                                   self.set.NOP)
        output_path_selected = self.set.set_dirout != \
            self.set.NOP
        # If directory conversion is selected, the number of files
        # must be higher than zero.
        if self.set.set_dir != self.set.NOP:
           if self.window_filesdir.filecount == 0:
               return False
        # Check the paths.
        if input_path_selected and output_path_selected:
            return True
        else:
            return False

    
    def convert(self, *e):
        """Start the convertsion"""
        # Disable the button and remove the bind
        self.window_filesdir.btn_convert.configure(state='disabled')
        self.bind_all("<F5>", None)
        # Set up the conversion class
        self.tocyr.ENC = self.set.set_encoding
        # After the checks in the gui, of of the
        # following ar this stage should be
        # a correct path.
        if self.set.set_file != self.set.NOP:
            self.tocyr.PATHIN = self.set.set_file
        else:
            self.tocyr.PATHIN = self.set.set_dir
        self.tocyr.PATHOUT =  self.set.set_dirout
        self.tocyr.RECURSIVE = self.set.set_recursive
        self.tocyr.CONVMODE = self.set.set_convmode
        self.tocyr.SHOW = self.set.set_verbose 
        self.tocyr.FAILSAFE =  0 if self.set.set_failsafe else 1
        # This has to be negated, since the user was
        # asked whether NOT to use RAM, but the scrips
        # expects answer on whether to USE it.
        self.tocyr.USERAM = 0 if self.set.set_noram else 1
        self.tocyr.CONVERTFNAMES = self.set.set_convertnames
        self.tocyr.REPORTPATH = self.set.set_reportpath
        self.tocyr.REPORTNAME = self.set.set_reportname
        self.tocyr.REPORT = self.set.set_report
        # Extensions are conversion mode dependant
        if self.set.set_convmode == 'tolat':
            self.tocyr.EXT = self.set.extensions
        else:
            self.tocyr.EXT = self.set.extensions_tocyr
        self.tocyr.SAMEOUTPATH = self.set.set_sameinout
        self.tocyr.SHOW = self.set.set_verbose
        self.tocyr.CALLEDFROM = 'dtknv tk interface'
        # Exceptio files and the path
        self.tocyr.DEFEXCPATH = self.set.DEFEXCPATH
        self.tocyr.EXCFILES  = self.set.set_exc_files
        # Start the thread
        self.th = threading.Thread(target = self.tocyr.run)
        self.th.start()
        while True:
            self.status.configure(text=self.lng['label_conversion'], 
                                  bg='yellow')
            self.status.update()
            time.sleep(1)
            self.status.configure(text=self.lng['label_conversion'],
                                  bg='red')
            self.status.update()
            time.sleep(0.3)
            if not self.th.is_alive():
                # Report is created?
                if self.tocyr.report:
                    reptext = self.lng['label_finishedcheck']
                else:
                    reptext = self.lng['label_no_report']
                # Was there errors?
                if self.tocyr.errors_during_work:
                    reptext =  self.lng['label_finishedwitherrors'] + reptext
                    repcol = "orange"
                else:
                    reptext = self.lng['label_finished'] + reptext
                    repcol = "green"
                self.status.configure(text=reptext, bg=repcol, cursor='hand1')
                self.status.bind('<Button-1>', self.open_report)
                break


    def open_report(self, *e):
        """
        Open the report file so user can inspect it.
        """
        if self.tocyr.report:
            try:
                helpers.open_text_viewer(self.tocyr.report.file)
            except:
                messagebox.showwarning(self.lng['label_error_generic'],
                                   self.lng['msg_error_opening_report'] % \
                                       self.tocyr.report.file)
        else:
            messagebox.showwarning('', self.lng['msg_report_not_created'])
           

    def kill_program(self, *e):
        """
        Save settings and exit.
        """
        # Reset paths:
        self.set.set_file = self.set.NOP
        self.set.set_dirin = self.set.NOP
        self.set.set_dir = self.set.NOP
        # Save the settings
        self.set.save()
        # Destroy all windows
        self.destroy()
        self.master.destroy()
                    
        
def show():
        """Show GUI"""
        root = tk.Tk()
        root.resizable(0,0)
        app = DtknvGui(master=root)
        root.protocol("WM_DELETE_WINDOW", app.kill_program)
        app.mainloop()
