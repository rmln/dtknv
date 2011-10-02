#! /usr/bin/python3
"""
Converts Cyrillic script to Latin.

Use:

cyrillic_text = 'На ливади коњ ућустечен и расћустечен!'

converted = CirConv(text=cyrillic_text, stats=True)
latin_text =  converted.get_converted()

print(latin_text)
> Na livadi konj ućustečen i rasćustečen!

print('Characters in original text: ', converted.stats_char_original)
> Characters in original text:  38

print('Characters in replaced text: ', converted.stats_char_replaced)
> Characters in replaced text:  39
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

RESPATH = os.path.join(os.path.dirname(__file__), '..', 
                       'resources', 'cyrlatdiff')

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
{"\u0438\u043d\u0458\u0435\u043a\u0446\u0438": "injekci", 
"\u043d\u0430\u0434\u0436\u0438\u0432\u0459": "nad\u017eivlj", 
"\u043a\u043e\u043d\u0458\u0443\u0433\u0430": "konjuga", 
"\u043f\u043e\u0434\u0436\u045a\u0435\u0442\u0438": "pod\u017enjeti", 
"\u043e\u0434\u0436\u0438\u0432\u0459\u0435\u043d": "od\u017eivljen", 
"\u043d\u0430\u0434\u0436\u045a\u0435": "nad\u017enje", 
"\u043e\u0434\u0436\u0438\u0432\u0459": "od\u017eivlj"
}
"""

class Replace:
    """Loads and saves strings that need to have different
    conversion rules"""

    DEFAULT = 'standarni-izuzeci.json'
    
    def __init__(self, f=False):
        """Load and save file strings"""
        pass

    def load(self, f):
        """Load a JSON file"""
        with open(f, mode='r', encoding='utf-8') as f:
            c = json.load(f)
        return(c)

    def save(self, f, exc):
        """Save a JSON file"""
        with open(f, mode='w', encoding='utf-8') as f:
            json.dump(exc, f)


class CirConv:
    """Converts Cyrillic script to Latin."""
        
    stats = {}
        
    def __init__(self, text='', mode="tolat", stats=False):
        """Initiate the class."""
        self.text = text
        self.mode = mode
        self.calc_stats = stats
        self.stats['char_original'] = self.calc_stats
        self.stats['char_replaced'] = self.calc_stats
        
        # Raise TypeError if 'text' is not a character
        # object.
        if not isinstance(text, str):
            raise TypeError('CirConv accepts text only, %s is rejected.' \
                                % type(text))
        
    def _load_latdif(self):
        """Load cirlatdif.txt file."""
        fcyr = os.path.join(RESPATH, 'cyr_cyrlatdiff.txt')
        flat = os.path.join(RESPATH, 'lat_cyrlatdiff.txt')
        cyr_words = codecs.open(fcyr, mode='r', 
                                   encoding='utf-8').readlines()
        lat_words = codecs.open(flat, mode='r', 
                                   encoding='utf-8').readlines()
        if not len(lat_words) == len(cyr_words):
            raise ValueError('Cyrlatdiff lists do not match.')
        # Clean the words from spaces and breaks.
        cyr_words = [c.strip() for c in cyr_words]
        lat_words = [c.strip() for c in lat_words]
        return [cyr_words, lat_words]

    
    def _make_variants(self, words):
        """Make variants of the words."""
        variants = []
        for word in words:
            variants.append(word.upper())
            variants.append(word.capitalize())
        return variants


    def convert_to_latin(self):
        """Convert the text and place it into .result. No return."""
        # Make character maps.
        self._make_charkeys()
        # Conversion to Cyrillic needs some preparations
        self.result = self._charreplace(self.text, mode='tolat')


    def convert_to_cyrillic(self):
        """Convert the text and place it into .result. No return."""
        # Make character maps.
        self._make_charkeys()
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
    
    def _custom_words(self, text):
        """Replace custom selected words"""
        w_number = len(self.lat_latdiff)
        for i in range(w_number):
            if self.lat_latdiff[i] in text:
                text = text.replace(self.lat_latdiff[i], self.cyr_latdiff[i])
        return text


    def _charreplace(self, text, mode):
        """Replace characters in the input text."""
        if self.calc_stats: # Don't bother with len() if no stats are needed
            len_in = len(text)
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
        # Stats needed?
        if self.calc_stats:
            self._stats(len_in, len(text)) 
        return text

    
    def _stats(self, len_in, len_out):
        """Stats about conversion"""
        self.stats['char_original'] = len_in
        self.stats['char_replaced'] = len_out


    def get_converted(self):
        """"Return the converted text."""
        self.convert()
        return self.result
