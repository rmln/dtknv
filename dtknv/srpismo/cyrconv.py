#! /usr/bin/python3
"""
Converts Cyrillic script to Latin.

Use:

cyrillic_text = 'На ливади коњ ућустечен и расћустечен!'

converted = CirConv(text=cyrillic_text)
converted.convert_to_latin()

# Also: converted.convert_to_cyrillic()

print(converted.result)
> Na livadi konj ućustečen i rasćustečen!

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

__version__ = '1.5'
__url__ = "https://gitorious.org/dtknv"
__author__ = "Romeo Mlinar"
__license__ = "GNU General Public License v. 3"

import os
import codecs
import json

cyr = {'А':'A', 'Б':'B', 'В':'V', 'Г':'G', 'Д':'D', 'Е':'E',
       'Ж':'Ž', 'З':'Z', 'И':'I', 'Ј':'J', 'К':'K', 'Л':'L',
       'М':'M', 'Н':'N', 'Њ':'Nj','О':'O', 'П':'P', 'Р':'R',
       'С':'S', 'Т':'T', 'Ћ':'Ć', 'У':'U', 'Ф':'F', 'Х':'H',
       'Ц':'C', 'Ч':'Č', 'Џ':'Dž','Ш':'Š', 'Ђ':'Đ', 'Љ':'Lj',
       'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 'е':'e',
       'ж':'ž', 'з':'z', 'и':'i', 'ј':'j', 'к':'k', 'л':'l',
       'љ':'lj','м':'m', 'н':'n', 'њ':'nj', 'о':'o', 'п':'p',
       'р':'r', 'с':'s', 'т':'t', 'ћ':'ć', 'у':'u', 'ф':'f',
       'х':'h', 'ц':'c', 'ч':'č', 'џ':'dž','ш':'š', 'ђ':'đ'}

lat_resolutions = {'NJ':'Њ',
                   'Nj':'Њ',
                   'nJ':'нЈ',
                   'LJ':'љ',
                   'Lj':'љ',
                   'lJ':'лЈ',
                   'DŽ':'Џ',
                   'Dž':'Џ',
                   'dŽ':'дЖ',}
standard_exc = \
"""
{"injekci": "\u0438\u043d\u0458\u0435\u043a\u0446\u0438", 
"nad\u017eivlj": "\u043d\u0430\u0434\u0436\u0438\u0432\u0459", 
"konjuga": "\u043a\u043e\u043d\u0458\u0443\u0433\u0430", 
"pod\u017enjeti": "\u043f\u043e\u0434\u0436\u045a\u0435\u0442\u0438", 
"od\u017eivljen": "\u043e\u0434\u0436\u0438\u0432\u0459\u0435\u043d", 
"nad\u017enje": "\u043d\u0430\u0434\u0436\u045a\u0435", 
"od\u017eivlj": "\u043e\u0434\u0436\u0438\u0432\u0459"
}
"""

class Replace:
    """
    Loads and saves strings that need to have different
    conversion rules.
    """
    
    def __init__(self, f=False):
        """Load and save file strings"""
        pass


    def load(self, f):
        """Load a JSON file"""
        return(self._load(f))
        

    def _load(self, f):
        """Load a JSON file"""
        # TODO: Add more elaborate check and
        # introduce a warning.
        with open(f, mode='r', encoding='utf-8') as f:
            c = json.load(f)
        return(c)

    def save(self, f, exc):
        """Save a JSON file"""
        with open(f, mode='w', encoding='utf-8') as f:
            json.dump(exc, f)


class CirConv:
    """
    Converts Cyrillic script to Latin.
    TODO: Remove repetitions.
    """
        
    def __init__(self, text='', stats=False, exception_files=[], variants=False,
                 path=False):
        """
        text       - text to be converted
        stats      - true if statistics is to be calaculated
        exceptions - list of files with the exception strings
        """
        # Raise TypeError if 'text' is not a character
        # object.
        if not isinstance(text, str):
            raise TypeError('CirConv accepts text only, %s is rejected.' \
                            % type(text))
        # Variables
        self.path = path
        self.text = text
        self.exception_elements = []
        # Exceptions strings. Don't load if path is
        # not present.
        if path and len(exception_files):
            self.load_exceptions(exception_files)
        # Variants?
        if variants and len(exception_files):
            self._make_variants()
        # Make character maps.
        self._make_charkeys()
        

    def load_exceptions(self, flist):
        """
        Load exceptions strings from flist files.
        """
        self.exception_elements = []
        if isinstance(flist, str):
            f = os.path.join(self.path, flist)
            exc_content = self._load_exc_file(f)
            if exc_content:
                self.exception_elements.append(exc_content)
        else:
            paths = [os.path.join(self.path, i) for i in flist]
            for f in paths:
                exc_content = self._load_exc_file(f)
                if exc_content:
                    self.exception_elements.append(exc_content)
           
     
    def _load_exc_file(self, f):
        """
        Load exception file or return false if
        there was an error.
        """
        try:
            exc_content = Replace().load(f)
        except:
            exc_content = False
        
        return(exc_content)
        
    
    def _make_variants(self):
        """Make variants of the words.
        
        TODO: finish this

        """
        pass
        # variants = []
        # for word in words:
        #     variants.append(word.upper())
        #     variants.append(word.capitalize())
        # return variants


    def convert_to_latin(self):
        """Convert the text and place it into .result. No return."""
        self.result = self._charreplace(self.text, mode='tolat')


    def convert_to_cyrillic(self):
        """Convert the text and place it into .result. No return."""
        self.result = self._charreplace(self.text, mode='tocyr')

    
    def _make_charkeys(self):
        """
        Make dictionaries for character replacement.
        """
        self.charmap_tolat = cyr
        self.charmap_tocyr = dict([v,k] for k,v in cyr.items())
        

    def _prepare_cyrillic(self, text):
        """Prepare text for conversion to Cyrillic"""
        lat_keys = lat_resolutions.keys()
        for letter in lat_keys:
            if letter in text:
                text = text.replace(letter, lat_resolutions[letter])
        return text

    
    def _excreplace(self, text):
        """
        Replace custom strongs.
        """
        # Go throught self.exceptions list, that holds
        # all dictionaries correspondng to files loaded
        # by Replace in __init__.
        for exception_dictionary in self.exception_elements:
            # Go through all keys of a dictionary.
            for string_search in exception_dictionary.keys():
                # If key is found in text, replace it
                # by the corresponding value.
                if string_search in text:
                    text = text.replace(string_search, 
                           exception_dictionary[string_search])
        return text


    def _charreplace(self, text, mode):
        """Replace characters in the input text."""
        # Replace custom strings ("exceptions")
        text = self._excreplace(text)
        # Create lists and dictionary
        if mode == 'tocyr':
            charkeys = self.charmap_tocyr.keys()
            charmap = self.charmap_tocyr
        elif mode == 'tolat':
            charkeys = self.charmap_tolat.keys()
            charmap = self.charmap_tolat
        else:
            raise ValueError("Mode must be 'tocyr' or 'tolat'.")
        # Replace the characters
        for letter in charkeys:
            if letter in text:
                text = text.replace(letter, charmap[letter])
        return text

