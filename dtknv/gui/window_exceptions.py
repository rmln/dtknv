#! /usr/bin/python3

"""

Exceptions interface for dtknv.

"""

import os
import tkinter as tk
from tkinter import messagebox
from functools import partial

import helpers
from srpismo.cyrconv import Replace
from gui.window_entry import MsgEntry

class Exceptions:
    
    # Default path for exception files
    PATH = os.path.join(helpers.def_report_path(),'.dtknvtestinstall')

    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.window = tk.Toplevel(master)
        self.window.resizable(0,0)
        self.window.title(self.lng['window_exceptions'])
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.main = tk.Frame(self.window, height=300, width=300)
        self.main.pack(padx=0, pady=0, fill='both', expand=1)
        self.main.pack_propagate(0)
        # Default pairs
        self.exc = self.load_exc('sample_rep.json')
        # Create needed widgets
        self.create_cells(self.exc)
        self.create_buttons()
        # Grab the window, so main program window
        # is not accessible
        self.window.grab_set()

    def read_cells(self, *e):
        """Read the content of cells and return a
        dictionary"""
        sr = {}
        for i in self.entry_sr.keys():
            search = i.get()
            replace = self.entry_sr[i].get()
            if search.strip() == '' and replace.strip() != '':
                # "Search" and "replace" fields must both
                # be blank.
                messagebox.showwarning(self.lng['label_error'],
                                   self.lng['label_fieldsblank'])

                return False
            elif search in sr.keys() and search != '':
                # Keys in a dictionary that holds "search"
                # strings must be unique.
                messagebox.showwarning(self.lng['label_error'],
                                   self.lng['label_fieldsrepeat'])
                return False
            else:
                sr[search] = replace
        return sr

    def get_all_exc_files(self):
        """Return a list of all present exc files"""
        files = {}
        fs = helpers.getallfiles(self.PATH, 'json')
        if fs:
            for i in fs:
                files[helpers.filename(i)] = fs
            return files
        else:
            return False
        
        
    def close(self, *event):
        """Actions upon close"""
        self.master.windows_opened.remove('window_exceptions')
        self.window.destroy()

    def load_exc(self, f):
        """Load replacement strings."""
        f = os.path.join(self.PATH, f)
        exceptions = Replace().load(f)
        return(exceptions)

    def save_exc(self, *e):
        """Save replacement strings."""
        strings = self.read_cells()
        if strings:
            f = os.path.join(self.PATH, self.active_filename)
            Replace().save(f, strings)
            print('saved in', f)

    def create_cells(self, exc=False):
        """Create cells for exception text"""
        # ----------------------------------------------
        frame_fieldsscroll = tk.Text(self.main, relief='flat')
        self.frame_fieldsscroll = frame_fieldsscroll
        text_fields = tk.Text(frame_fieldsscroll, relief='flat')
        frame_fieldsscroll.window_create('insert', window=text_fields)
        
        if exc:
            keys = list(self.exc.keys())
            values = list(self.exc.values())
        else:
            keys = ('',) * 10
            values = ('',) * 10

        tf = {}
        for item in range(len(keys)):
            #tf[f] = tk.Frame(text_fields)

            e_find = tk.Entry(text_fields, width=16)
            e_replace = tk.Entry(text_fields, width=16)

            e_find.insert(0, keys[item])
            e_replace.insert(0, values[item])

            e_find.grid(row=0, column=0)
            e_replace.grid(row=0, column=1)

            text_fields.window_create('insert', window=e_find)
            text_fields.window_create('insert', window=e_replace)
            
            # Put them into dictionary
            tf[e_find] = e_replace
            # Bind function that discovers which cells have
            # focus.
            e_find.bind('<FocusIn>', 
                        partial(self.selected_content, 
                        e_find, 'f', 'select'))
            e_replace.bind('<FocusIn>',
                           partial(self.selected_content, 
                           e_replace, 'r', 'select'))
            # Bind, so field properties are restored
            # when focus is out
            e_find.bind('<FocusOut>', 
                        partial(self.selected_content, 
                        e_find, 'f', 'reset'))
            e_replace.bind('<FocusOut>', 
                           partial(self.selected_content, 
                           e_replace, 'r', 'reset'))
            text_fields.insert('end', '\n')
        
        scrollbar = tk.Scrollbar(frame_fieldsscroll, width=15)
        scrollbar.config(command=text_fields.yview)
        text_fields.config(yscrollcommand=scrollbar.set)
        
        frame_fieldsscroll.pack()
        scrollbar.pack(side='right', fill='y')
        text_fields.pack(fill='both')
        
        text_fields.configure(state='disabled')
        frame_fieldsscroll.configure(state='disabled')
        # Ordered by search, replace
        self.entry_sr = tf
        # Ordered by replace, search
        self.entry_rs = {tf[i]: i for i in tf}


    def selected_content(self, *w):
        """Calculate which cells are selected."""
        if w[1] == 'f':
            self.sel_find = w[0]
            self.sel_replace = self.entry_sr[w[0]]
        elif w[1] == 'r':
            self.sel_replace = w[0]
            self.sel_find = self.entry_rs[w[0]]
        else:
             raise ValueError("2nd value must be 'f' or 'r'")
        # Configure
        if w[2] == 'select':
            self.fields_color('yellow')
        elif w[2] == 'reset':
            self.fields_color('white')
            # If there's no value in "find", gray out
            # the field
            if self.sel_find.get().strip() == '':
                self.fields_color('gray')
            # If "replace" string is blank, that
            # means that the "find" string will
            # be erased in the target text
            if self.sel_replace.get().strip() == '':
                print("replace is blank")
                if ' ' in self.sel_replace.get():
                    self.fields_color('orange')
                else:
                    self.fields_color('red')
        else:
            raise ValueError("3rd value must be 'select' or 'reset'")

    def fields_color(self, color):
        """Set colors in the fields"""
        self.sel_replace.configure(bg=color)
        self.sel_find.configure(bg=color)
        
    def create_buttons(self):
        """Frame for buttons"""
        # Frames in this window
        frame_buttons = tk.Frame(self.window)
        # Buttons & menus
        menu_array = [('saveexc', self.save_exc),
                        ('addcells', self.new_set),
                        ('removecells', self.new_set),
                        ('newexcfile', self.new_set)]
        #Menu button actions ---------------
        button_actions = tk.Menubutton(frame_buttons, 
                                    text=self.lng['button_exc_commands'],
                                    relief=tk.RAISED,
                                    width=10)
        menu_actions = tk.Menu(button_actions, tearoff=0)
        # Commands in this menu:
        menu_objects = {}
        for b, c in menu_array:
            menu_objects[b] = menu_actions.add_command( \
                label=self.lng['button_%s' % b],
                command=c)
        button_actions.configure(menu=menu_actions)
        button_actions.pack(side='left', pady=3, padx=5)
        # Menu button actions end --------------

        # Menu button load ---------------
        button_load = tk.Menubutton(frame_buttons, 
                                    text=self.lng['button_load'],
                                    relief=tk.RAISED,
                                    width=10)
        menu_load = tk.Menu(button_load, tearoff=0)
        # Standard exceptions
        menu_load.add_command(label=self.lng['button_standardsr'], 
                              command=print)
        # Other exceptions
        files = self.get_all_exc_files()
        if files:
            for i in files.keys():
                menu_load.add_command(label=self.lng['button_fileexc'] \
                                          % i, command=print)
        button_load.configure(menu=menu_load)
        button_load.pack(pady=3, padx=5)
        # Menu button end --------------
        frame_buttons.pack(padx=10, pady=10)

    def new_set(self, *e):
        """Create a blank sheet for values"""
        self.new_filename = self.get_filename()
        if self.new_filename:
            self.active_filename = self.new_filename + '.json'
            self.frame_fieldsscroll.destroy()
            self.create_cells()

    def get_filename(self, *e):
        """Show a message box and ask for a file name"""
        # Disable closing of the corrent windows
        # TODO: It is possible to close this window
        # while filename message is shown.
        filename = MsgEntry(master=self.master, lng=self.lng, 
                            text=self.lng['label_enterfilenameexc'])
        self.window.wait_window(filename.window)
        return filename.entry
