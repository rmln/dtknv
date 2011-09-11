#! /usr/bin/python3

"""

Loads and saves the settings.

"""

import os
import json
import copy


from gui import language
from srpismo import cyrconv
import helpers

PATH = os.path.join( os.path.dirname(__file__),'..', 'resources', 'settings')

class Settings:
    
    JPATH = os.path.join(PATH, 'default.json')
    
    def __init__(self):
        """Loads the settings for GUI"""
        self.set_language = 'sr_cyr'
        self.load()
        self.apply()
        self.set_file = self.language['label_noselection']
        self.set_dir = self.language['label_noselection']
        self.set_dirout = self.language['label_noselection']
        self.set_recursive = 1
        self.set_convertnames = 0
        self.set_verbose = 1
        self.set_failsafe = 0
        self.set_noram = 0
        self.set_report = 1
        self.set_reportname = 'dtknv'
        self.set_update = 1
        self.set_reportpath = helpers.def_report_path()
        self.set_encoding = 'utf-8'
        self.set_warningmb = 100
        self.set_warningn = 100
        
        self.save()
        
        
    def apply(self):
        """Apply settings"""
        if self.set_language == 'sr_lat':
            self.language = self.latin()
        if self.set_language == 'sr_cyr':
            self.language = language.serbian_cyrillic
        
    def save(self):
        """Save settings in JSON file"""
        settings = self.setting_elements()
        with open(self.JPATH, mode='w', encoding='utf-8') as f:
            json.dump(settings, f)
    
    def setting_elements(self):
        """Get all attributes that contain settings"""
        settings = {}
        for i in dir(self):
            if i.startswith('set_'):
                settings[i] = getattr(self, i)
        return settings
             
                
    def load(self):
        """Load settings from JSON file."""
        with open(self.JPATH, mode='r', encoding='utf-8') as f:
            e = json.load(f)
         
        
    def latin(self):
        """Convert Cyrillic Serbian to Latin."""
        conv = cyrconv.CirConv(mode="tolat")
        source = copy.deepcopy(language.serbian_cyrillic)
        for i in source.keys():
             conv.text = source[i]
             source[i] = conv.get_converted()
        return source
             
Set = Settings()        