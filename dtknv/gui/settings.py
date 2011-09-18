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

# Default settings

_default_settings = """
{
"set_file": "None", 
"set_dirout": "None", 
"set_dir": "None", 
"set_sameinout": "0",
"set_language": "lngcyr",
"set_recursive": "0",
"set_convertnames": "0",
"set_verbose": "1",
"set_failsafe": "0",
"set_noram": "0",
"set_report": "1",
"set_reportname": "dtknv",
"set_update": "1",
"set_reportpath": "default",
"set_encoding": "utf-8",
"set_warningmb": "100",
"set_warningn": "100",
"set_extensions": "docx,odt,txt,htm,html"
}
"""

PATH = os.path.join( os.path.dirname(__file__),'..', 'resources', 'settings')

class Settings:
    
    JPATH = os.path.join(PATH, 'default.json')
    JPATH = os.path.join(helpers.def_report_path(),
                         '.dtknvtestinstall/settings/default.json')
    
    def __init__(self):
        """Loads the settings for GUI"""
        self.numeric  = ('set_failsafe', 'set_recursive', 'set_convertnames', 
                         'set_verbose', 'set_noram', 'set_report', 'set_update',
                         'set_warningmb', 'set_warningn', 'set_sameinout')
        self.checkpaths = ('set_file', 'set_dir', 'set_dirout')
        # This marks "none" for paths 
        self.NOP = "(?)"
        # This is just to track the prevously selected folder
        # to prevent long size/number calculation in 
        # window_filesdir.update_gui
        self.previous_folder = self.NOP
        self.settings_exist()
        self.load()
        self.load_language()
        # Multilanguage messages
        self.multilanguage = language.multilanguage

    def settings_exist(self):
        """Check if the settings file exists. If not,
        create the path and save default settings"""
        if not os.path.exists(self.JPATH):
            # Take settings path and remove the
            # file name.
            path = os.path.split(self.JPATH)[0]
            # Does it exist?
            try:
                os.makedirs(path)
            except OSError:
                # Folder is already there, so
                # skipp the creation.
                pass
            self.reset_settings(path=os.path.join(path, 'default.json'))
            
            

    def reset_settings(self, path='', default=False):
        """Reset the settings"""
        if default:
            path = self.JPATH
        f = open(path, encoding='utf-8', 
                     mode='w')
        f.write(_default_settings)
        f.close()
                
    def load_language(self):
        """Apply settings"""
        if self.set_language == 'lnglat':
            self.language = self.latin()
        if self.set_language == 'lngcyr':
            self.language = language.serbian_cyrillic

        
    def save(self):
        """Save settings in JSON file"""
        settings =  self.settings_elements_get()
        with open(self.JPATH, mode='w', encoding='utf-8') as f:
            json.dump(settings, f)

    
    def settings_elements_get(self):
        """Get all attributes that contain settings"""
        settings = {}
        for i in dir(self):
            if i.startswith('set_'):
                settings[i] = getattr(self, i)
        return settings

                
    def load(self):
        """Load settings from JSON file."""
        with open(self.JPATH, mode='r', encoding='utf-8') as f:
            settings = json.load(f)
        for i in settings.keys():
            value = settings[i]
            # Values for the check boxes must be numeric
            # to pass a validation in settings window. 
            if i in self.numeric:
                value = int(settings[i])
            # The report path defaults to home folder
            if i == 'set_reportpath':
                if value.strip() == 'default':
                    value = helpers.def_report_path()
            # A note that nothing is selected for paths
            if i in self.checkpaths:
                if not os.path.exists(value):
                    value = self.NOP
            setattr(self, i, value)
        # Place the extensions
        self.get_extensions()
 
    
    def get_extensions(self):
        """Format extensions"""
        self.extensions =   self.set_extensions.split(",")
        if '' in self.extensions: 
            self.extensions.remove('')
 
 
    def latin(self):
        """Convert Cyrillic Serbian to Latin."""
        conv = cyrconv.CirConv(mode="tolat")
        source = copy.deepcopy(language.serbian_cyrillic)
        for i in source.keys():
             conv.text = source[i]
             source[i] = conv.get_converted()
        return source

    def reload(self):
        """Save and load settings"""
        self.save()
        self.load()
             
Set = Settings()        
