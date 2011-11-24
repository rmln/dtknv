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
import copy

import tkinter as tk
from tkinter import messagebox
from functools import partial

import helpers
from gui.elements import ExcDropDownMenu
from srpismo.cyrconv import Replace
from gui.window_entry import MsgEntry


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
        """
        1. Draw widgets.
        2. Load file.
        3. Wait for an input.
        """
        self.master = master
        self.set = self.master.main_settings
        # Path for exceptions
        self.PATH = self.set.DEFEXCPATH
        self.lng = self.master.lng
        self.window = tk.Toplevel(master)
        #self.window.resizable(0,0)
        self.window.title(self.lng['window_exceptions'])
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.main = tk.Frame(self.window, height=300, width=300)
        self.main.pack(padx=0, pady=0, fill='both', expand=1)
        self.main.pack_propagate(0)
        self.create_buttons()
        # Binds
        self.window.bind('<Control-d>', self.append_empty_cell)
        self.window.bind('<Control-n>', self.new_set)
        self.window.bind('<Control-s>', self.save_exc)
        self.window.bind('<Control-i>', self.delete_selected_cells)
        # Load last edited exception file.
        self.active_filename = self.set.set_last_excfile
        self.load_file_create_cells(self.active_filename, initial=True)
        #self.colorise()
        # Grab the window, so main program window
        # is not accessible
        self.window.grab_set()


    def load_file_create_cells(self, f=False, initial=False):
        """
        Load f file and place items into cells.
        """
        # Just a lame way to pass some lame code
        self.SAVINGBLOCKED = False
        # These are not available during the first
        # load, so not point in calling the destroy
        # attributes.
        if not initial:
            self.see_if_cells_are_changed()
            self.canvas.destroy()
            self.vsb.destroy()
        # Create canvas
        self.create_cells_container()
        # Load search and replace strings
        if f:
            # Call the method for loading the jsnon files
            # and see if it will fail
            try:
                items = self.load_exc_file(f)
                # Set this file as the last edited one
                self.set.set_last_excfile = f
            except:
                # Oops, an error. Inform the user and prevent from
                # saving, or the corrupt file may be overwritten (which
                # may or may not be a good idea, but it's up to the 
                # user's choice)
                messagebox.showwarning(self.lng['label_error_loadingexc'],
                                   self.lng['label_error'])
                items = False
                self.menu_actions.entryconfigure(1, state='disabled')
                self.SAVINGBLOCKED = True
        else:
            items = False
            self.menu_actions.entryconfigure(1, state='normal')
        # Create a copy of items, so it is possible
        # to chek later if the items are changed
        self.items_orig = copy.deepcopy(items)
        # Place cells in the canvas
        self.draw_cells(exc=items)
        # Colorise the cells if needed
        self.colorise()
        # Update the title
        self.window.title(self.lng['window_exceptions'] + ' (%s)' % \
                              helpers.filename(self.active_filename))
        # Hide the frame if there was an error in loading the file:
        if self.SAVINGBLOCKED:
            self.canvas.pack_forget()
        

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
        """
        Actions upon window closing.
        """
        if not self.SAVINGBLOCKED:
            self.see_if_cells_are_changed()    
        self.master.windows_opened.remove('window_exceptions')
        self.window.destroy()

    
    def see_if_cells_are_changed(self):
        """
        Check if cells are saved, and if yes,
        offer to save them.
        """
        if self.items_orig != self.read_cells():
            ask = messagebox.askyesno(self.lng['label_save'], 
                                      self.lng['msg_savechanges'])
            if ask:
                self.save_exc()
        

    def load_exc_file(self, f):
        """Load replacement strings."""
        f = os.path.join(self.PATH, f)
        self.active_filename = f
        exceptions = Replace().load(f)
        return(exceptions)


    def save_exc(self, *e):
        """Save replacement strings."""
        strings = self.read_cells()
        if strings:
            f = os.path.join(self.PATH, self.active_filename)
            Replace().save(f, strings)
            # Recreate the menu in settings menu.
            self.master.recreate_excetions_menu()
            # Recreate the menu in this window.
            self.create_dropdown_menu()
            # This here is needed so see_if_cells_are_changed()
            # would not bother user.
            self.items_orig = strings


    def append_empty_cell(self, *e):
        """Add an empty cell to the list"""
        self.draw_cells({'':''}, appendempty=True)
        self.canvas.event_generate('<Configure>')


    def draw_cells(self, exc=False, appendempty=False):
        """
        Create new paris of cells. To add new cells at the end
        appendempty must be True, and key/values have the same
        number of empty items.
        """
        if exc:
            keys = list(exc.keys())
            values = list(exc.values())
        else:
            keys = ('',) * 10
            values = ('',) * 10

        if appendempty:
            tf = self.allcells
            cells_number = range(len(keys))
        else:
            cells_number = range(len(keys))
            tf = {}

        # Master is inherited from the parent widget in
        # create_cells_container().
        master = self.container

        for item in cells_number:

            e_find = tk.Entry(master)
            e_replace = tk.Entry(master)

            e_find.insert(0, keys[item])
            e_replace.insert(0, values[item])

            e_find.grid(row=len(tf)+1, column=0, sticky='ew')
            e_replace.grid(row=len(tf)+1, column=1, sticky='ew')

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
        # self.entry_sr and self.entry_rs are the same
        # dictionary, but with swapped keys and values.
        # Ordered by search, replace
        self.entry_sr = tf
        # Ordered by replace, search
        self.entry_rs = {tf[i]: i for i in tf}
        self.allcells = tf
        #
        # self.allcells contains all cells and it is accessible
        # throughout the class. This attribute is important in
        # draw_cells().
        tf = self.allcells
    

    def create_cells_container(self):
        """
        Create cells for exception text, where exc can
        be False or contain a dictionary of values. False
        will create default 10 blank cell pairs.

        This method calls draw_cells(), where the cells are
        actually created by tk.

        This part of code was initially written by using Text widget,
        but since it was impossible to scale Entries properly, it
        needed a redesign. I would like to thank Bryan Oakley from
        stackoverflow.com for helping me writting the code by
        using Canvas widget (he actually wrote down the whole idea
        and OnCanvasConfigure method, and what you see here is more
        or less copy/paste).
        
        """
        self.canvas = tk.Canvas(self.main, width=200, highlightthickness=0)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.vsb = tk.Scrollbar(self.main, orient="vertical",
                                command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.container = tk.Frame(self.canvas, borderwidth=0, 
                                  highlightthickness=0)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.canvas.create_window((0,0), anchor="nw", 
                                  window=self.container, tags="container")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        
        
    def on_canvas_configure(self, event):
        """
        Reconfigure the widget.
        """
        self.canvas.itemconfigure("container", width=event.width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))     
        

    def selected_content(self, *w):
        """
        Determine  which cells are selected.
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
            self.set_cells_color(self.sel_find, self.sel_replace,
                                 color1='yellow')
        elif w[2] == 'reset':
            self.deterimine_cells_color(self.sel_find, self.sel_replace)
        else:
            raise ValueError("3rd value must be 'select' or 'reset'")


    def set_cells_color(self, find, replace, color1='green', color2=False):
        """
        Set colors in the fields.
        
        If only the first cell color is supplied, then use
        the same color for the second cell.
        """
        # If there's no argument for color2,
        # then both cells should have same
        # color.
        if not color2:
            color2 = color1
        # Configure the colors
        replace.configure(bg=color1)
        find.configure(bg=color2)


    def deterimine_cells_color(self, find, replace):
        """
        Return conditional colors.

        
        red      a warning to user that "find" string will
                 be deleted in the target text;

        orange   a warning to user that "find" string will
                 be deleted in the target text by blanks;

        gray     a warning to user that "find" and "replace"
                 were removed from the list and will be deleted
                 from the current exceptions file

        yellow   currently selected cells.
        """
        # TODO: This can be optimised by replacing
        # repetitive replace.get()
        # First, reset them to white:
        self.set_cells_color(find, replace, color1='white')
        # Then, mark them if they contain white space:
        if ' ' in find.get():
            self.set_cells_color(find, replace, color1='green')
        if ' ' in replace.get():
            self.set_cells_color(find, replace, color1='green')
       
        # If there's no value in "find", gray out
        # the field.
        if (find.get().strip() and replace.get().strip()) == '':
            self.set_cells_color(find, replace, color1='gray')
        # If values are same, gray out the fields,
        # since that cells will not be saved.
        if (find.get() == replace.get()):
            self.set_cells_color(find, replace, color1='gray')
        # If "replace" string is blank, that
        # means that the "find" string will
        # be erased in the target text
        if find.get() != '' and replace.get().strip() == '':
            self.set_cells_color(find, replace, color1='red')
            if ' ' in replace.get():
                self.set_cells_color(find, replace, color1='red',
                                     color2='orange')


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
        # Make menu_actions public, so it's accessible from
        # load_file_create_cells().
        self.menu_actions = menu_actions


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
            self.load_file_create_cells(f=False)


    def colorise(self):
        """
        Colorise cells. Iterate over the ___ and call 
        deterimine_cells_color. Thi method is called after
        a JSON exception file is loaded / cells created.
        """
        for search in self.allcells.keys():
            self.deterimine_cells_color(search, self.allcells[search]) 


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
