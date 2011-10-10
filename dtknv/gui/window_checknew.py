#! /usr/bin/python3

"""

Frame for plain text conversion..

"""

import os
import time
import tkinter as tk
import urllib.request

from gui.elements import Link

import version
import helpers

class NewVersion:

    URL = r'http://www.languagebits.com/dtknv/doc/version.txt'
    DLPAGE = r'http://www.languagebits.com/dtknv/'
    
    def __init__(self, master):
        self.master = master
        self.lng = self.master.lng
        self.window = tk.Toplevel(master)
        self.window.resizable(0,0)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.main = tk.Frame(self.window, height=100, width=300)
        self.main.pack(padx=0, pady=0, fill='both', expand=1)
        self.main.pack_propagate(0)
        self.buttons()
        self.widgets()
        self.check_version()
        

    def widgets(self):
        """Create a text field with a scroll bar"""
        self.update_text = tk.Label(self.main, 
                                    wraplength=250,
                                    justify='left')
        self.update_text.configure(text=self.lng['label_updatechecking'])
        self.update_text.pack(padx=5, pady=5, anchor='w')
        self.update_text.update()
        self.main.update()
        
        

    def check_version(self):
        """Compare current and new verison and show
        appropriate links, if a newer version is available.
        """
        utext = self.get_newversion()
        # The response if False (no new version)
        if not utext:
            text = self.lng['label_updatenonew'] % version.__version__
        # There was an error in getting in check
        elif utext == self.lng['label_updateerror']:
            text = utext
        # There is a new version.
        else:
            text = self.lng['label_updatenew']
            text = text % (utext['version'], utext['date'], utext['info'])
            # Direct download link
            Link(self.window, text=self.lng['label_updatdirect'],
                 link=utext['url'])
            # Download page
            Link(self.window, text=self.lng['label_updatepage'],
                 link=self.DLPAGE)

        self.update_text.configure(text=text)


    def get_newversion(self, *e):
        """Check if new version is available, and if yes
        show details / download link."""
        try:
            new_version = urllib.request.urlopen(self.URL).read()
            new_version = new_version.decode('utf-8').split('|')
            ver = {}
            ver['version'] =  new_version[0]
            ver['date'] =  new_version[1]
            ver['info'] =  new_version[2]
            #ver['version'] =  '0.5.5 beta'
            if os.name != 'posix':
                ver['url'] =  new_version[3]
            else:
                ver['url'] =  new_version[4]
            compared = helpers. get_version_comparison(v2=ver['version'])
        except:
            return self.lng['label_updateerror']

        if compared == 'lower':
            return ver
        else:
            return False

    
    def buttons(self):
        """Create buttons"""
        frame_buttons = tk.Frame(self.window)
        btn_close = tk.Button(frame_buttons, 
                                text=self.lng['button_close'], 
                                command=self.close)
        btn_close.pack(side='left', padx=3, pady=3)
        frame_buttons.pack(side='bottom')

    def close(self, *e):
        """Close this window"""
        self.master. windows_opened.remove('window_newversion')
        self.window.destroy()
