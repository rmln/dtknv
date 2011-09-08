#! /usr/bin/python3

"""

Exceptions interface for dtknv.

"""

import tkinter as tk

class Exceptions:
    
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
        # Create buttons
        self.create_buttons()
        self.create_cells()
        self.window.grab_set()
        

    def close(self, *event):
        """Actions upon close"""
        self.master. windows_opened.remove('window_exceptions')
        self.window.destroy()

    def create_cells(self):
        """Create cells for exception text"""
        # ----------------------------------------------
        frame_fieldsscroll = tk.Text(self.main, relief='flat')
        text_fields = tk.Text(frame_fieldsscroll, relief='flat')
        frame_fieldsscroll.window_create('insert', window=text_fields)
        
        tf = {}
        for f in range(31):
            #tf[f] = tk.Frame(text_fields)

            e_find = tk.Entry(text_fields, width=16, relief='flat')
            e_replace = tk.Entry(text_fields, width=16, relief='flat')

            e_find.insert(0, 'find'+str(f))
            e_replace.insert(0, 'replace'+str(f))

            e_find.grid(row=0, column=0)
            e_replace.grid(row=0, column=1)

            text_fields.window_create('insert', window=e_find)
            text_fields.window_create('insert', window=e_replace)
            
            text_fields.insert('end', '\n')
        
        scrollbar = tk.Scrollbar(frame_fieldsscroll, width=15)
        scrollbar.config(command=text_fields.yview)
        text_fields.config(yscrollcommand=scrollbar.set)
        
        frame_fieldsscroll.pack()
        scrollbar.pack(side='right', fill='y')
        text_fields.pack(fill='both')
        
        text_fields.configure(state='disabled')
        frame_fieldsscroll.configure(state='disabled')

            
        

    def create_buttons(self):
        """Frame for buttons"""
        button_objects = {}
        # Frames in this window
        frame_buttons = tk.Frame(self.window)
        # Buttons & menus
        button_array = [('save', print),
                        ('add', print),
                        ('remove', print)]
        for b, c in button_array:
            button_objects[b] = tk.Button(frame_buttons, 
                                          text=self.lng['button_%s' % b],
                                          command=c)
            button_objects[b].pack(side='left')
        #Menu button
        button_load = tk.Menubutton(frame_buttons, 
                                    text=self.lng['button_load'],
                                    relief=tk.RAISED,
                                    width=7)
        menu_load = tk.Menu(button_load, tearoff=0)
        # Standard exceptions
        menu_load.add_command(label=self.lng['button_standardsr'], command=print)
        # Other exceptions
        for i in range(5):
            menu_load.add_command(label='File name %s' % i, command=print)
        button_load.configure(menu=menu_load)
        button_load.pack()
        frame_buttons.pack(padx=10, pady=10)
