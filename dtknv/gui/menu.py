#! /usr/bin/python3

"""

Menu interface for dtknv.

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
import sys
import webbrowser 

import tkinter as tk
from tkinter import messagebox
from functools import partial

import helpers
from gui import elements

import version

class Dmenu:

    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.main = tk.Menu(master)
        self.file = tk.Menu(self.main, tearoff=0)
        self.set = master.main_settings
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
        # Settings variables
        self.var_sett_sameinout = tk.IntVar()
        self.var_sett_convertnames = tk.IntVar()
        self.var_sett_recursive = tk.IntVar()
        self.var_sett_lng = tk.IntVar()
        self.var_sett_lnglat = tk.IntVar()
        self.var_sett_lngeng = tk.IntVar()
        self.var_sett_convmode = tk.StringVar() # Conversion mode
        # Assign from the settings file
        self.var_sett_convertnames.set(self.set.set_convertnames)
        self.var_sett_recursive.set(self.set.set_recursive)
        self.var_sett_sameinout.set(self.set.set_sameinout)
        self.var_sett_convmode.set(self.set.set_convmode)
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
        # Settings -> Conversion mode
        self.sett.add_radiobutton(label=self.lng['menu_settings_tolat'],
                                  variable = self.var_sett_convmode,
                                  command=partial(self.assign_convmode,
                                                  'tolat'))
        self.sett.add_radiobutton(label=self.lng['menu_settings_tocyr'],
                                  variable = self.var_sett_convmode,
                                  command=partial(self.assign_convmode,
                                                  'tocyr'))
        self.sett.add_separator()
        # Settings -> Exceptions
        self.sett.add_command(label=self.lng['menu_settings_exceptions'], 
                              command=master.show_exceptions)
        # Settings -> Select exceptions
        self.menu_exc = tk.Menu(self.main, tearoff=0)
        self.sett.add_cascade(label=self.lng['menu_settings_excfiles'], 
                              menu=self.menu_exc)
        self.create_exceptions_menu()
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
        self.help.add_command(label=self.lng['menu_help_help'], 
                              command=self.open_help)
        self.help.add_command(label=self.lng['menu_help_update'],
                              command=self.master.show_newversion)
        self.help.add_command(label=self.lng['menu_help_about'],
                              command=self.master.show_aboutwindow)
        # Shortcuts
        self.master.bind_all('<Control-o>', self.browse_file)
        self.master.bind_all('<Control-f>', self.browse_dirin)
        self.master.bind_all('<Control-u>', self.browse_dirout)
        # Invoke index 7 is conversion mode is tolat, otherwise
        # index 8.
        if self.set.set_convmode == 'tolat':
            self.sett.invoke(7)
        elif self.set.set_convmode == 'tocyr':
            self.sett.invoke(8)
        else:
            raise ValueError('Convmode must be tocyr or tolat.')


    def create_exceptions_menu(self):
        """
        Create exceptions menu.
        """
        # Call ExcDropDownMenu with parameters to create
        # a submenu with checkbuttons.
        elements.ExcDropDownMenu(parent=self.menu_exc, path=self.PATH, 
                                 lng=self.lng, main=self,
                                 src='from_menu')

    def open_help(self, *e):
        """
        Open help file in locally, and if it fails
        try the online version.
        """
        browser = webbrowser.get()
        language = self.set.set_language
        # If GUI language is in English, default to
        # Serbian.
        if language == 'lngeng':
            language = 'lnglat'
            messagebox.showinfo('', self.lng['msg_nohelpinenglish'])
        # Local path, determined by the GUI language.
        help_file_name = 'uputstvo-%s.html' % language
        help_local_path = os.path.join(self.set.APPDIR, 'doc', help_file_name) 
        if os.path.exists(help_local_path):
            # Open browser
            browser.open(help_local_path)
        else:
            open_homepage = messagebox.askyesno(
                self.lng['label_error_generic'], 
                self.lng['msg_nolocalhelp'])
            if open_homepage:
                browser.open(self.set.URL_HELP + '?pismo=%s&ver=%s' % \
                                 (language, version.__version__))
                

    def browse_file(self, *e):
        """
        Browse for a file.
        """
        filetypes = self.get_file_descriptions()
        path  = elements.Browse(mode='file',
                                filetypes=filetypes,
                                initpath=self.set.set_last_filepath,
                                lng=self.lng).path
        if path != '':
            self.set.set_file = path
            path_to_file = helpers.get_file_path(self.set.set_file)
            self.set.set_last_filepath = path_to_file
            self.set.set_dir = self.set.NOP
            # If same/in out is selected, set the proper
            # out path:
            if self.set.set_sameinout:
                self.set.set_dirout = path_to_file
            self.master.update_gui()
            self.master.show_filesdir()

    
    def browse_dirin(self, *e):
        """
        Browse for an input directory.
        """
        path = elements.Browse(initpath=self.set.set_last_dirin,
                               mode='dirin',
                               lng=self.lng).path
        if path != '':
            # The path is OK, so assign it to the variable,
            # and reset the file variable.
            self.set.set_dir = path
            self.set.set_last_dirin = path
            self.set.set_file = self.set.NOP
            self.assign_same('in')
            self.master.update_gui()
            self.master.show_filesdir()

        
    def browse_dirout(self, *e):
        """
        Browse for an output directory.
        """
        path = elements.Browse(initpath=self.set.set_last_dirout,
                               mode='dirout',
                               lng=self.lng).path
        if path != '':
            self.set.set_dirout = path
            self.set.set_last_dirout = path
            self.assign_same('out')
            self.master.update_gui()
            self.master.show_filesdir()
            # If same/in out is selected, set the proper
            # out path:
            if self.set.set_sameinout:
                self.set.set_sameinout = 0
                self.sett.invoke(0)

    
    def languagechanged(self, to):
        """
        Inform user that the language change will be active
        after restart.
        """
        self.set.set_language = to
        self.set.reload()
        key = '%s_msg_restart' % to
        text = self.set.multilanguage[key]
        messagebox.showinfo('', text)

    
    def assign_same(self, src='in'):
        """
        Check if folders are the same.
        """
        if src == 'in':
            if self.set.set_sameinout:
                self.set.set_dirout =  self.set.set_dir
        elif src == 'out':
            if self.set.set_sameinout:
                if self.set.set_dir != self.set.NOP: 
                    self.set.set_dir =  self.set.set_dirout
        else:
            raise ValueError("src must be 'in' or 'out'")
    
        
    def assign_convmode(self, v):
        """
        Assign correct conversion mode string.
        """
        self.set.set_convmode = v
        # Refresh the interface
        try:
            self.master.update_gui()
        except AttributeError:
            # This probably means that the rest of the interface
            # is not created on the program startup.
            pass


    def assign_chk(self, v):
        """
        Assign value from menu to global settings.
        This is to pass values into the self.set, which
        is then saved in settings.py.
        
        I.e.:

        self.set.set_recursive = self.var_sett_recursive.get()
        
        """
        setattr(self.set, 'set_%s' % v,
                getattr(self, 'var_sett_%s' % v).get())
        if v == 'sameinout' and self.set.set_sameinout:
            # "Save in same dir" option is on, so set the paths
            if self.set.set_dir != self.set.NOP:
                self.set.set_dirout = self.set.set_dir
            # Same as above, but for a file:
            if self.set.set_file != self.set.NOP:
                self.set.set_dirout = helpers.get_file_path(self.set.set_file)
            self.master.update_gui()
        if v == 'sameinout' and not self.set.set_sameinout:
            self.set.set_dirout =  self.set.NOP
            self.master.update_gui()
        if v == 'recursive':
            self.master.update_gui()


    def get_file_descriptions(self):
        """
        Return a file extension/description object to be used
        in identifying patterns within dialogues.
        """
        if self.set.set_convmode == 'tocyr':
            extensions = self.set.extensions_tocyr
        elif self.set.set_convmode == 'tolat':
            extensions = self.set.extensions
        else:
            raise ValueError('set_convmode must be "tolat" or "tocyr".')
        # Compile the extension filter
        cext = []
        # Go through the extensions and add corresponding
        # description from the language file/dictionary. If
        # no description is found, add generic one.
        for e in extensions:
            pattern = '*.%s' % e
            try:
                description = self.lng['ext_%s' % e]
            except:
                description = self.lng['ext_?generic'] + e
            cext.append((description, pattern))
        # Add option for all extensions
        cext.append((self.lng['ext_*'], '.*'))
        return cext

