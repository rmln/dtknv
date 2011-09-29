#! /usr/bin/python3

"""

Menu interface for dtknv.

"""

import os

import tkinter as tk
from tkinter import messagebox
from functools import partial
import helpers
from gui import elements
from gui.settings import Set

class Dmenu:


    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.main = tk.Menu(master)
        self.file = tk.Menu(self.main, tearoff=0)
        self.set = Set
        self.PATH = self.set.DEFEXCPATH
        # File
        self.main.add_cascade(label=self.lng['menu_main'], menu=self.file)
        # File: Load file, Load directory, Exit
        self.file.add_command(label=self.lng['menu_file_loadf'],
                              command=self.browse_file)
        self.file.add_command(label=self.lng['menu_file_loadd'],
                              command=self.browse_dirin)
        self.file.add_command(label=self.lng['menu_file_outpath'],
                              command=self.browse_dirout)
        
        self.file.add_separator()
        # Redirect exit to the exit() function
        self.file.add_command(label=self.lng['menu_file_exit'],
                              command=self.master.kill_program)
        # Settings
        self.sett = tk.Menu(self.main, tearoff=0)
        self.main.add_cascade(label=self.lng['menu_settings'], menu=self.sett)
        #Setting variables
        self.var_sett_sameinout = tk.IntVar()
        self.var_sett_convertnames = tk.IntVar()
        self.var_sett_recursive = tk.IntVar()
        self.var_sett_lng = tk.IntVar()
        self.var_sett_lnglat = tk.IntVar()
        self.var_sett_lngeng = tk.IntVar()
        # Assign
        self.var_sett_convertnames.set(self.set.set_convertnames)
        self.var_sett_recursive.set(self.set.set_recursive)
        self.var_sett_sameinout.set(self.set.set_sameinout)
        #self.set.set_convertnames = self.var_sett_convertnames.get()
        # Settings: Save in same, Convert names, Recursive
        # Exceptions, Mode1, Mode2, Advanced
        self.sett.add_checkbutton(label=self.lng['menu_settings_samedir'], 
                                  variable=self.var_sett_sameinout,
                                  command=partial(self.assign_chk,
                                                  v='sameinout'))
        self.sett.add_checkbutton(label=self.lng['menu_settings_names'], 
                                  variable=self.var_sett_convertnames,
                                  command=partial(self.assign_chk,
                                                  v='convertnames'))
        self.sett.add_checkbutton(label=self.lng['menu_settings_recur'], 
                                  variable=self.var_sett_recursive,
                                  command=partial(self.assign_chk,
                                                  v='recursive'))
        self.sett.add_separator()
        # Settings -> Basic settings
        self.sett.add_command(label=self.lng['menu_settings_showfilesdir'], 
                                  command=master.show_filesdir)
        self.sett.add_command(label=self.lng['menu_settings_showplaintext'], 
                                  command=master.show_plaintext)
        self.sett.add_separator()
        # Settings -> Exceptions
        self.sett.add_command(label=self.lng['menu_settings_exceptions'], 
                              command=master.show_exceptions)
        # Settings -> Select exceptions
        self.menu_exc = tk.Menu(self.main, tearoff=0)
        self.sett.add_cascade(label=self.lng['menu_settings_excfiles'], 
                              menu=self.menu_exc)
        self.create_exceptions_menu()
#-------------------
        self.sett.add_separator()
        # Settings -> Language
        self.menu_language = tk.Menu(self.main, tearoff=0)
        self.sett.add_cascade(label=self.lng['menu_settings_language'], 
                              menu=self.menu_language)
        self.menu_language.add_command(label=self.lng['menu_settings_lngcyr'], 
                                       command=partial(self.languagechanged, 
                                       to='lngcyr'))
        self.menu_language.add_command(label=self.lng['menu_settings_lnglat'], 
                                       command=partial(self.languagechanged,
                                       to='lnglat'))
        self.menu_language.add_command(label=self.lng['menu_settings_lngeng'], 
                                           command=partial(self.languagechanged,
                                           to='lngeng'))
        # Settings -> Advanced settings
        self.sett.add_command(label=self.lng['menu_settings_adv'], 
                              command=master.show_options)
        # Help
        self.help = tk.Menu(self.main, tearoff=0)
        self.main.add_cascade(label=self.lng['menu_help'], menu=self.help)
        # Help: Instructions, About
        self.help.add_command(label=self.lng['menu_help_help'], command=print)
        self.help.add_command(label=self.lng['menu_help_about'], command=print)
        self.help.add_command(label=self.lng['menu_help_update'],
                              command=self.master.show_newversion)
        # Shortcuts
        self.master.bind_all('<Control-o>', self.browse_file)
        self.master.bind_all('<Control-f>', self.browse_dirin)
        self.master.bind_all('<Control-u>', self.browse_dirout)


    def create_exceptions_menu(self):
        """Create exceptions menu."""
        # Call ExcDropDownMenu with parameters to create
        # a submenu with checkbuttons.
        elements.ExcDropDownMenu(parent=self.menu_exc, path=self.PATH, 
                                 lng=self.lng, main=self,
                                 src='from_menu')

    def browse_file(self, *e):
        """Browse for a file"""
        self.set.set_file = elements.Browse(mode='file').path
        self.set.set_dir = self.set.NOP
        self.master.update_gui()
    
    def browse_dirin(self, *e):
        self.set.set_dir = elements.Browse(mode='dir',
                           initpath=r'/home/marw/.dtest/in').path
        self.set.set_file = self.set.NOP
        self.assign_same('in')
        self.master.update_gui()
        
    def browse_dirout(self, *e):
        self.set.set_dirout = elements.Browse(mode='dir',
                              initpath=r'/home/marw/.dtest/out').path
        self.assign_same('out')
        self.master.update_gui()
    
    def languagechanged(self, to):
        """Inform a user that language will be active after restart"""
        self.set.set_language = to
        self.set.reload()
        key = '%s_msg_restart' % to
        text = self.set.multilanguage[key]
        messagebox.showinfo('', text)

    
    def assign_same(self, src='in'):
        """Check if folders are the same"""
        if src == 'in':
            if self.set.set_sameinout:
                self.set.set_dirout =  self.set.set_dir
        elif src == 'out':
            if self.set.set_sameinout:
                self.set.set_dir =  self.set.set_dirout
        else:
            raise ValueError("src must be 'in' or 'out'")
        


    def assign_chk(self, v):
        """Assign value from menu to global settings.
        This is to pass values into the self.set, which
        is then saved in settings.py.
        
        I.e.:

        self.set.set_racursive = self.var_sett_recursive.get()
        
        """
        setattr(self.set, 'set_%s' % v,
                getattr(self, 'var_sett_%s' % v).get())
        if v == 'sameinout' and self.set.set_sameinout:
            self.set.set_dir =  self.set.set_dirout
            self.master.update_gui()
        if v == 'sameinout' and not self.set.set_sameinout:
            self.set.set_dirout =  self.set.NOP
            self.master.update_gui()
        
            
            
