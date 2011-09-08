#! /usr/bin/python3

"""

New interface for dtknv.

"""

import tkinter as tk

class Options:
    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.window = tk.Toplevel(master)
        self.window.resizable(0,0)
        self.window.title(lng['window_options'])
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.main = tk.Frame(self.window, height=300, width=400)
        self.main.pack(padx=10, pady=10, fill='both', expand=1)
        #self.main.pack_propagate(0)
        # Options
        self.var_sett_verbose = tk.IntVar()
        self.var_sett_failsafe = tk.IntVar()
        self.var_sett_noram = tk.IntVar()
        self.var_sett_report = tk.IntVar()
        self.var_sett_reportname = tk.StringVar()
        self.var_sett_encoding = tk.StringVar()
        self.var_sett_warningmb = tk.StringVar()
        self.var_sett_warningn = tk.StringVar()
        self.var_sett_reportpath = tk.StringVar()
        # Create elements
        self.create_elements()
        self.create_buttons()
        self.window.grab_set()
        
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
        chks = [(self.var_sett_verbose, 'verbose'),
                (self.var_sett_failsafe, 'failsafe'),
                (self.var_sett_noram, 'noram'),
                (self.var_sett_report, 'report')]
        txts = [(self.var_sett_reportname, 'reportname'),
                (self.var_sett_reportpath, 'reportpath'),
                (self.var_sett_encoding, 'encoding'),
                (self.var_sett_warningmb, 'warningmb'),
                (self.var_sett_warningn, 'warningn')]
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
            box = tk.Entry(checkbuttons[n], width='5')
            if n == 'reportpath':
                box.configure(width='15')
            label.pack(side='left')
            box.pack(side='left')
            checkbuttons[n].pack(anchor='w')
        frame.pack(anchor='w', padx=7)
        
