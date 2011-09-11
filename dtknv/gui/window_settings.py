#! /usr/bin/python3

"""

New interface for dtknv.

"""

import tkinter as tk

from gui.settings import Set

class Options:
    def __init__(self, master):
        self.set = Set
        self.master = master
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
        self.var_set_update = tk.IntVar()
        self.var_set_reportname = tk.StringVar()
        self.var_set_encoding = tk.StringVar()
        self.var_set_warningmb = tk.StringVar()
        self.var_set_warningn = tk.StringVar()
        self.var_set_reportpath = tk.StringVar()
        self.win_setting_elements()
        # Create elements
        self.create_elements()
        self.create_buttons()
        self.window.grab_set()

    def win_setting_elements(self): 
        """Get all attributes that contain settings"""
        #settings = self.
        for i in dir(self):
            if i.startswith('var_set_'):
                key = i[4:]
                fc = getattr(self.set, '%s' % key)
                getattr(self, i).set(fc)       
                        
    def close(self, *event):
        """Actions upon close"""
        self.master. windows_opened.remove('window_options')
        self.window.destroy()
        
    def check_entries(self, *event):
        """Check all entries"""
        print('I checked the entries...')

    
    def create_buttons(self):
        """Create buttons"""
        frame = tk.Frame(self.main)
        button_ok = tk.Button(frame, text=self.lng['button_ok'],
                              command=self.check_entries)
        button_ok.pack(side='left')
        button_cancel = tk.Button(frame, text=self.lng['button_cancel'],
                                  command=print)
        button_cancel.pack(side='left')
        frame.pack(pady=10)
        
        
    def create_elements(self):
        """Create elements"""
        frame = tk.Frame(self.main)
        chks = [(self.var_set_verbose, 'verbose'),
                (self.var_set_failsafe, 'failsafe'),
                (self.var_set_noram, 'noram'),
                (self.var_set_report, 'report'),
                 (self.var_set_update, 'update')]
        txts = [(self.var_set_reportname, 'reportname'),
                (self.var_set_reportpath, 'reportpath'),
                (self.var_set_encoding, 'encoding'),
                (self.var_set_warningmb, 'warningmb'),
                (self.var_set_warningn, 'warningn')]
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
            if n == 'reportpath':
                box.configure(width='15')
            label.pack(side='left')
            box.pack(side='left')
            checkbuttons[n].pack(anchor='w')
        frame.pack(anchor='w', padx=7)
        