#! /usr/bin/python3

"""

Exceptions interface for dtknv.

Exceptions are not errors, but any strings in the source text that are
not to be replaced by a regular Cyr > Lat conversion in the target
text. They function as search and replace.

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

import os
import tkinter as tk
from tkinter import messagebox
from functools import partial

import helpers
from gui.elements import ExcDropDownMenu
from srpismo.cyrconv import Replace
from gui.window_entry import MsgEntry
from gui.settings import Set

class Exceptions:
    """
    Class Exceptions is a GUI for managing JSON files that store
    find and replace strings.

    Some of the class elements:

    .allcells
    Alias for .entry_sr, and contains a dictonary
    with search and replace cells. 
    
    """
    def __init__(self, master):
        self.master = master
        self.set = Set
        # Path for exceptions
        self.PATH = self.set.DEFEXCPATH
        self.lng = self.master.lng
        self.window = tk.Toplevel(master)
        self.window.resizable(0,0)
        self.window.title(self.lng['window_exceptions'])
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.main = tk.Frame(self.window, height=300, width=300)
        self.main.pack(padx=0, pady=0, fill='both', expand=1)
        self.main.pack_propagate(0)
        # Create needed widgets
        self.create_cells()
        self.create_buttons()
        # Binds
        self.window.bind('<Control-d>', self.append_empty_cell)
        self.window.bind('<Control-n>', self.new_set)
        self.window.bind('<Control-s>', self.save_exc)
        self.window.bind('<Control-i>', self.delete_selected_cells)
        # Load default exception
        self.active_filename = self.set.set_defaultexc
        self.load_file_create_cells(self.active_filename)
        # Grab the window, so main program window
        # is not accessible
        self.window.grab_set()


    def load_file_create_cells(self, f):
        """
        Load f file and place items into cells.
        """
        self.frame_fieldsscroll.destroy()
        items = self.load_exc_file(f)
        self.create_cells(items)
        # Update the title
        self.window.title(self.lng['window_exceptions'] + ' (%s)' % \
                              self.active_filename)


    def read_cells(self, *e):
        """
        Read the content of cells and return a dictionary.
        """
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
            if (search != '') and (replace != ''):
                sr[search] = replace
        return sr

        
    def close(self, *event):
        """Actions upon window closing."""
        self.master.windows_opened.remove('window_exceptions')
        self.window.destroy()


    def load_exc_file(self, f):
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
            # Recreate the menu in settings menu:
            self.master.recreate_excetions_menu()
            # Recreate the menu in this wondow:
            self.create_dropdown_menu()


    def append_empty_cell(self, *e):
        """Add an empty cell to the list"""
        keys = values = ('',)
        self.draw_cells(keys, values, appendempty=True)
        #self.set_cell_focus()


    def draw_cells(self,  keys, values, appendempty=False):
        """
        Create new paris of cells. To add new cells at the end
        appendempty must be True, and key/values have the same
        number of empty items.
        """
        if appendempty:
            tf = self.allcells
        else:
            tf = {}
        # Master is inherited from the parent widget in
        # create_cells().
        master = self.text_fields
        for item in range(len(keys)):
            e_find = tk.Entry(master, width=16)
            e_replace = tk.Entry(master, width=16)
            e_find.insert(0, keys[item])
            e_replace.insert(0, values[item])
            e_find.grid(row=0, column=0)
            e_replace.grid(row=0, column=1)
            master.window_create('insert', window=e_find)
            master.window_create('insert', window=e_replace)
            # Put cell widgets into dictionary.
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
            master.insert('end', '\n')
        # self.entry_sr and self.entry_rs are the same
        # dictionary, but with swapped keys and values.
        # Ordered by search, replace
        self.entry_sr = tf
        # Ordered by replace, search
        self.entry_rs = {tf[i]: i for i in tf}
        self.allcells = tf
    

    def create_cells(self, exc=False):
        """
        Create cells for exception text, where exc can
        be False or contain a dictionary of values. False
        will create default 10 blank cell pairs.

        This method calls draw_cells(), where the cells are
        actually created by tk.
        """
        frame_fieldsscroll = tk.Text(self.main, relief='flat')
        self.frame_fieldsscroll = frame_fieldsscroll
        self.text_fields = tk.Text(frame_fieldsscroll, relief='flat')
        frame_fieldsscroll.window_create('insert', window=self.text_fields)
        
        if exc:
            keys = list(exc.keys())
            values = list(exc.values())
        else:
            keys = ('',) * 10
            values = ('',) * 10

        self.draw_cells(keys, values)
        # self.allcells contains all cells and it is accessible
        # throughout the class. This attribute is important in
        # draw_cells().
        tf = self.allcells
        # Add scrollbar and attach it to the text field that holds
        # the cells pairs.
        scrollbar = tk.Scrollbar(self.frame_fieldsscroll, width=15)
        scrollbar.config(command=self.text_fields.yview)
        self.text_fields.config(yscrollcommand=scrollbar.set)
        frame_fieldsscroll.pack()
        scrollbar.pack(side='right', fill='y')
        self.text_fields.pack(fill='both')
        # Don't allow any changes in parent text field.
        self.text_fields.configure(state='disabled')
        frame_fieldsscroll.configure(state='disabled')
        

    def selected_content(self, *w):
        """
        Determine  which cells are selected, and then
        format them by color:
        
        red      a warning to user that "find" string will
                 be deleted in the target text;

        orange   a warning to user that "find" string will
                 be deleted in the target text by blanks;

        gray     a warning to user that "find" and "replace"
                 were removed from the list and will be deleted
                 from the current exceptions file

        yellow   currently selected cells.
        
        """
        if w[1] == 'f':
            self.sel_find = w[0]
            self.sel_replace = self.entry_sr[w[0]]
        elif w[1] == 'r':
            self.sel_replace = w[0]
            self.sel_find = self.entry_rs[w[0]]
        else:
             raise ValueError("2nd value must be 'f' or 'r'")
        # Print content (debugging)
        #print('find: ', self.sel_find.get(), ' replace: ',
        #      self.sel_replace.get())
        # Configure
        if w[2] == 'select':
            self.cells_color('yellow')
        elif w[2] == 'reset':
            self.cells_color('white')
            # If there's no value in "find", gray out
            # the field
            if (self.sel_find.get().strip() and \
                    self.sel_replace.get().strip()) == '':
                self.cells_color('gray')
            # If values are same, gray the fields,
            # since that cells will not be saved.
            if (self.sel_find.get() == self.sel_replace.get()):
                self.cells_color('gray')
            # If "replace" string is blank, that
            # means that the "find" string will
            # be erased in the target text
            if self.sel_replace.get().strip() == '' and \
               self.sel_find.get().strip() != '':
                if ' ' in self.sel_replace.get():
                    self.cells_color('orange')
                else:
                    self.cells_color('red')
        else:
            raise ValueError("3rd value must be 'select' or 'reset'")


    def cells_color(self, color1, color2=False):
        """Set colors in the fields"""
        # If there's no argument for color2,
        # then both cells should have same
        # color.
        if not color2:
            color2 = color1
        self.sel_replace.configure(bg=color1)
        self.sel_find.configure(bg=color2)


    def delete_selected_cells(self, *e):
        """
        Delete the content of the active cells.
        """
        # This causes an error if user has not selected
        # a cell, so make sure .delete has  an object
        # to be called from:
        if 'sel_find' in dir(self):
            for field in (self.sel_find, self.sel_replace):
                field.delete(0, 'end')
        

    def create_buttons(self):
        """Frame for buttons"""
        # Frames in this window
        frame_buttons = tk.Frame(self.window)
        # Buttons & menus
        menu_array = [('newexcfile', self.new_set),
                      ('saveexc', self.save_exc),
                      ('separator',''),
                      ('addcells', self.append_empty_cell),
                      ('removecells', self.delete_selected_cells)
                      # Let's leave this for next version:
                      #('separator',''),
                      #('csv_import', print),
                      #('csv_export', print)
                      ]
        #Menu button actions ---------------
        button_actions = tk.Menubutton(frame_buttons, 
                                    text=self.lng['button_exc_commands'],
                                    relief=tk.RAISED,
                                    width=10)
        menu_actions = tk.Menu(button_actions, tearoff=0)
        # Commands in this menu:
        menu_objects = {}
        for b, c in menu_array:
            if b != 'separator':
                menu_objects[b] = menu_actions.add_command( \
                    label=self.lng['button_%s' % b],
                    command=c)
            else:
                menu_objects[b] = menu_actions.add_separator()
        button_actions.configure(menu=menu_actions)
        button_actions.pack(side='left', pady=3, padx=5)
        button_load = tk.Menubutton(frame_buttons, 
                                    text=self.lng['button_load'],
                                    relief=tk.RAISED,
                                    width=10)
        menu_load = tk.Menu(button_load, tearoff=0)
        # Make public instance of menu_load. This is needed
        # so menu is accessible outside this method, and used
        # when files are saved.
        self.menu_load = menu_load
        # Populate dropdown menu
        self.create_dropdown_menu()
        # Standard exceptions
        button_load.configure(menu=menu_load)
        button_load.pack(pady=3, padx=5)
        # Menu button end --------------
        frame_buttons.pack(padx=10, pady=10)


    def create_dropdown_menu(self):
        """
        Create a dropdown menu for the "load files"
        button.
        """
        ExcDropDownMenu(parent=self.menu_load,
                        path=self.PATH, 
                        lng=self.lng, src='from_exc',
                        main=self)


    def new_set(self, *e):
        """
        Create a blank sheet for values.
        """
        self.new_filename = self.get_filename()
        if self.new_filename:
            self.active_filename = self.new_filename + '.json'
            self.frame_fieldsscroll.destroy()
            self.create_cells()


    def get_filename(self, *e):
        """
        Show a message box and ask for a file name.
        """
        # Disable closing of the corrent windows
        # TODO: It is possible to close this window
        # while filename message is shown.
        filename = MsgEntry(master=self.master, lng=self.lng, 
                            text=self.lng['label_enterfilenameexc'],
                            path=self.PATH)
        self.window.wait_window(filename.window)
        return filename.entry
