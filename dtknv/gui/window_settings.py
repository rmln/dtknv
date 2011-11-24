#! /usr/bin/python3

"""

Settings interface.

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
from tkinter import messagebox

from gui.elements import Browse

class Options:
    def __init__(self, master):
        self.master = master
        self.set = self.master.main_settings
        self.lng = self.master.lng
        self.window = tk.Toplevel(master)
        self.window.resizable(0,0)
        self.window.title(self.lng['window_options'])
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.main = tk.Frame(self.window, height=300, width=400)
        self.main.pack(padx=10, pady=10, fill='both', expand=1)
        #self.main.pack_propagate(0)
        # Options
        self.var_set_verbose = tk.IntVar()
        self.var_set_failsafe = tk.IntVar()
        self.var_set_noram = tk.IntVar()
        self.var_set_report = tk.IntVar()
        self.var_set_reportname = tk.StringVar()
        self.var_set_encoding = tk.StringVar()
        self.var_set_warningmb = tk.IntVar()
        self.var_set_warningn = tk.IntVar()
        self.var_set_reportpath = tk.StringVar()
        self.var_set_extensions = tk.StringVar()
        self.var_set_extensions_tocyr = tk.StringVar()
        self.settings_load()
        # Create elements
        self.create_elements()
        self.create_buttons()
        self.window.grab_set()


    def settings_load(self): 
        """
        Get all attributes that contain settings.
        """
        self.set.load()
        for i in dir(self):
            if i.startswith('var_set_'):
                key = i[4:]
                fc = getattr(self.set, '%s' % key)
                getattr(self, i).set(fc)


    def settings_save(self, *event): 
        """
        Get all attributes that contain settings.
        """
        for i in dir(self):
            if i.startswith('var_set_'):
                key = i[4:]
                value = getattr(self, i).get()
                setattr(self.set, '%s' % key, value)
        self.set.save()
        self.settings_load()


    def are_settings_changed(self, *event): 
        """
        Get all attributes that contain settings.
        """
        for i in dir(self):
            if i.startswith('var_set_'):
                key = i[4:]
                fc = getattr(self.set, '%s' % key)
                value = getattr(self, i).get()
                if value != fc:
                    return True
        return False

     
    def create_buttons(self):
        """
        Create buttons.
        """
        frame = tk.Frame(self.main)
        button_ok = tk.Button(frame, text=self.lng['button_ok'],
                              command=self.settings_save)
        button_ok.pack(side='left', padx=3)
        button_cancel = tk.Button(frame, text=self.lng['button_close'],
                                  command=self.close)
        button_cancel.pack(side='left', padx=3)
        button_cancel = tk.Button(frame, text=self.lng['button_default'],
                                  command=self.reset_settings)
        button_cancel.pack(side='left', padx=3)
        frame.pack(pady=10)
        
        
    def create_elements(self):
        """
        Create elements.
        """
        frame = tk.Frame(self.main)
        chks = [(self.var_set_verbose, 'verbose'),
                (self.var_set_failsafe, 'failsafe'),
                (self.var_set_noram, 'noram'),
                (self.var_set_report, 'report')]
        txts = [(self.var_set_reportname, 'reportname'),
                (self.var_set_reportpath, 'reportpath'),
                (self.var_set_encoding, 'encoding'),
                (self.var_set_warningmb, 'warningmb'),
                (self.var_set_warningn, 'warningn'),
                (self.var_set_extensions, 'extensions'),
                (self.var_set_extensions_tocyr, 'extensions_tocyr')]
        # Checkbuttons ---------------------------
        checkbuttons = {}
        for e, n in chks:
            checkbuttons[n] = tk.Checkbutton(frame, 
                              text=self.lng['options_%s' % n],
                              variable=e,
                              justify='left')
            checkbuttons[n].pack(anchor='w')
        # Text fields -----------------------
        for e, n in txts:
            checkbuttons[n] = tk.Frame(frame)
            label  = tk.Label(checkbuttons[n], 
                              text=self.lng['options_%s' % n],
                              justify='left')
            box = tk.Entry(checkbuttons[n], width='5', textvariable=e)
            if n in ('reportpath', 'extensions', 'extensions_tocyr'):
                box.configure(width='30')
                # In Cyrillic to Latin conversion, only
                # txt files are supported, so disable entry
                # to this field.
                if n == 'extensions_tocyr':
                    box.configure(state='disabled')
            if n == 'reportpath':
                box.bind('<Double-Button-1>', self.browse_folder)
                self.txt_reportpath = box
            label.pack(side='left')
            box.pack(side='left')
            checkbuttons[n].pack(anchor='w')
        frame.pack(anchor='w', padx=7)
        

    def close(self, *event):
        """
        Close, but check for changes.
        """
        if self.are_settings_changed():
            ask = messagebox.askyesno(self.lng['window_options'], 
                                      self.lng['msg_settingschanged'])
            if ask:
                self.settings_save()
                self.master.update_gui()
        self.master.windows_opened.remove('window_options')
        self.window.destroy()

    
    def browse_folder(self, *e):
        """Browse for folder and place path in the entry"""
        path = Browse(mode='dir', initpath=None).path
        if path != '':
            self.txt_reportpath.delete(0, 'end')
            self.txt_reportpath.insert('end', path)


    def reset_settings(self, *e):
        """Reset the settings"""
        self.set.reset_settings(default=True)
        self.settings_load()
        
