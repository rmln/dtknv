#! /usr/bin/python3

"""

Loads and saves the settings. The class is instantiated once on the 
runtime and used extensively by the program. 

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
import sys
import json
import copy


from gui import language
from srpismo import cyrconv
import helpers

# Default settings that is written to disk on the
# first run. All values beginning with 'set_' are
# dynamically set as attributes of the class. 

_default_settings = """
{
"set_file": "(?)", 
"set_dirout": "(?)", 
"set_dir": "(?)", 
"set_sameinout": "0",
"set_language": "lnglat",
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
"set_extensions": "docx,odt,txt,htm,html",
"set_extensions_tocyr": "txt",
"set_exc_files": "standardni-izuzeci.json",
"set_convmode": "tolat",
"set_defaultexc": "standardni-izuzeci.json",
"set_last_dirin":"(?)",
"set_last_dirout":"(?)",
"set_last_filepath":"(?)",
"set_last_excfile":"standardni-izuzeci.json"
}
"""


class Settings:
    
    def __init__(self):
        """
        Loads the settings for GUI.
        """
        # This URL path is called when About > Help is selected
        self.URL_HELP = \
            r'http:\\serbian.languagebits.com\dtknv\doc\uputstvo.php'
        # Loacal help files should be in self.APPDIR\doc 
        self.APPDIR = os.path.split(sys.argv[0])[0]
        # The settings directory
        self.SET_DIR = '.dtknv'
        # The settings directory in home
        self.PATH = os.path.join(helpers.def_report_path(), self.SET_DIR)
        # Full path to the settings file
        self.SETPATH = os.path.join(self.PATH, 'settings', 'default.json')
        # The path where search and replace files are located
        self.DEFEXCPATH = os.path.join(self.PATH, 'exceptions')
        # These items are the integer values
        self.numeric  = ('set_failsafe', 'set_recursive', 'set_convertnames', 
                         'set_verbose', 'set_noram', 'set_report', 
                         'set_warningmb', 'set_warningn', 'set_sameinout')
        self.checkpaths = ('set_file', 'set_dir', 'set_dirout')
        # This marks "none" for paths 
        self.NOP = "(?)"
        # This is just to track the prevously selected folder
        # to prevent long size/number calculation in 
        # window_filesdir.update_gui
        self.previous_folder = self.NOP
        self.settings_exist()
        self.standard_exceptions_exist()
        self.load()
        self.load_language()
        # Multilanguage messages
        self.multilanguage = language.multilanguage


    def standard_exceptions_exist(self):
        """
        Check if standard exceptions file exists, and if
        not, create it.
        """
        if not os.path.exists(self.DEFEXCPATH):
            # Take settings path and remove the
            # file name.
            # Does it exist?
            try:
                os.makedirs(self.DEFEXCPATH)
            except OSError:
                # Folder is already there, so
                # skipp the creation.
                pass
        f = open(os.path.join(self.DEFEXCPATH, 'standardni-izuzeci.json'), 
                     encoding='utf-8', mode='w')
        f.write(cyrconv.standard_exc)


    def settings_exist(self):
        """
        Check if the settings file exists. If not,
        create the path and save default settings.
        """
        if not os.path.exists(self.SETPATH):
            # Take settings path and remove the
            # file name.
            path = os.path.split(self.SETPATH)[0]
            # Does it exist?
            try:
                os.makedirs(path)
            except OSError:
                # Folder is already there, so
                # skipp the creation.
                pass
            self.reset_settings(path=os.path.join(path, 'default.json'))
            
            
    def reset_settings(self, path='', default=False):
        """
        Reset the settings.
        """
        if default:
            path = self.SETPATH
        f = open(path, encoding='utf-8', 
                     mode='w')
        f.write(_default_settings)
        f.close()

                
    def load_language(self):
        """
        Load the language strings.
        """
        if self.set_language == 'lnglat':
            self.language = self.latin()
        if self.set_language == 'lngcyr':
            self.language = language.serbian_cyrillic
        if self.set_language == 'lngeng':
            self.language = language.english

        
    def save(self):
        """
        Save settings in JSON file.
        """
        settings =  self.settings_elements_get()
        with open(self.SETPATH, mode='w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4)

    
    def settings_elements_get(self):
        """
        Get all attributes that contain the settings
        string.
        """
        settings = {}
        for i in dir(self):
            if i.startswith('set_'):
                settings[i] = getattr(self, i)
        return settings

                
    def load(self):
        """
        Load settings from JSON file.
        """
        with open(self.SETPATH, mode='r', encoding='utf-8') as f:
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
            # Verifications of paths (does they exist, are they
            # paths at all).
            if i in self.checkpaths:
                # This is to deal with instances where tk sends an
                # empty list, so os.path.exists fails.
                if isinstance(value ,list) and len(value) == 0:
                    value = self.NOP
                if isinstance(value, list):
                    if not os.path.exists(value):
                        value = self.NOP
            setattr(self, i, value)
        # Place the extensions
        self.get_extensions()
 
    
    def get_extensions(self):
        """
        Format extensions.
        """
        self.extensions = self._format_extensions(self.set_extensions)
        self.extensions_tocyr = \
            self._format_extensions(self.set_extensions_tocyr)


    def _format_extensions(self, what):
        """
        Return neat extension list.
        """
        what = what.split(",")
        if '' in what: 
            what.remove('')
        return what
 
 
    def latin(self):
        """Convert Cyrillic Serbian to Latin."""
        conv = cyrconv.CirConv()
        source = copy.deepcopy(language.serbian_cyrillic)
        for i in source.keys():
             conv.text = source[i]
             conv.convert_to_latin()
             source[i] = conv.result
        return source


    def reload(self):
        """Save and load settings"""
        self.save()
        self.load()
