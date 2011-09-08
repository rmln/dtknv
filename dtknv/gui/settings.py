#! /usr/bin/python3

"""

Loads and saves the settings.

"""

import os
import json
import copy


from gui import language
from srpismo import cyrconv

PATH = os.path.join( os.path.dirname(__file__),'..', 'resources', 'settings')

class Settings:
    
    JPATH = os.path.join(PATH, 'default.json')
    
    def __init__(self):
        """Loads the settings for GUI"""
        self.set_language = 'sr_cyr'
        self.apply()
        self.save()
        self.load()
        
    def apply(self):
        """Apply settings"""
        if 'sr_lat':
            self.language = self.latin()
        if 'sr_cyr':
            self.language = language.serbian_cyrillic
        
    def save(self):
        """Save settings in JSON file"""
        settings = {}
        for i in dir(self):
            if i.startswith('set_'):
                settings[i] = getattr(self, i)
                
        with open(self.JPATH, mode='w', encoding='utf-8') as f:
            json.dump(settings, f)
       
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