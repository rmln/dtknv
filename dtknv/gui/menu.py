#! /usr/bin/python3

"""

Menu interface for dtknv.

"""

import tkinter as tk

class Dmenu:
    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.main = tk.Menu(master)
        self.file = tk.Menu(self.main, tearoff=0)
        # File
        self.main.add_cascade(label=self.lng['menu_main'],
                             menu=self.file,
                             underline=0)
        # File: Load file, Load directory, Exit
        self.file.add_command(label=self.lng['menu_file_loadf'], command=print)
        self.file.add_command(label=self.lng['menu_file_loadd'], command=print)
        self.file.add_command(label=self.lng['menu_file_outpath'], command=print)
        self.file.add_separator()
        self.file.add_command(label=self.lng['menu_file_saveprofile'], 
                              command=print)
        self.file.add_separator()
        self.file.add_command(label=self.lng['menu_file_exit'], 
                              command=print)
        # Settings
        self.sett = tk.Menu(self.main, tearoff=0)
        self.main.add_cascade(label=self.lng['menu_settings'],
                              menu=self.sett,
                              underline=0)
        #Setting variables
        self.var_sett_samedir = tk.IntVar()
        self.var_sett_convertnames = tk.IntVar()
        self.var_sett_recursive = tk.IntVar()
        # Settings: Save in same, Convert names, Recursive
        # Exceptions, Mode1, Mode2, Advanced
        self.sett.add_checkbutton(label=self.lng['menu_settings_samedir'], 
                                  command=print,
                                  variable=self.var_sett_samedir)
        self.sett.add_checkbutton(label=self.lng['menu_settings_names'], 
                                  command=print,
                                  variable=self.var_sett_convertnames)
        self.sett.add_checkbutton(label=self.lng['menu_settings_recur'], 
                                  command=print,
                                  variable=self.var_sett_recursive)
        self.sett.add_separator()
        
        
        self.sett.add_command(label=self.lng['menu_settings_showfilesdir'], 
                                  command=master.show_filesdir)
        self.sett.add_command(label=self.lng['menu_settings_showplaintext'], 
                                  command=master.show_plaintext)
        self.sett.add_separator()
        
        
        self.sett.add_command(label=self.lng['menu_settings_exceptions'], 
                              command=master.show_exceptions)
        self.sett.add_separator()
        
        
        self.sett.add_command(label=self.lng['menu_settings_adv'], 
                              command=master.show_options)
        # Help
        self.help = tk.Menu(self.main, tearoff=0)
        self.main.add_cascade(label=self.lng['menu_help'],
                              menu=self.help,
                              underline=0)
        # Help: Instructions, About
        self.help.add_command(label=self.lng['menu_help_help'], command=print)
        self.help.add_command(label=self.lng['menu_help_about'], command=print)

