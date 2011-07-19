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

__version__ = '1.3'
__url__ = "https://gitorious.org/dtknv"
__author__ = "Romeo Mlinar"
__license__ = "GNU General Public License v. 3"

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

class CirConv:
    """Converts Cyrillic script to Latin."""
        
    def __init__(self, text='', mode="tolat", stats=False):
        """Initiate the class."""
        self.text = text
        self.mode = mode
        self.calc_stats = stats
        self.stats_char_original = self.calc_stats
        self.stats_char_replaced = self.calc_stats
        
        # Raise TypeError if 'text' is not a character
        # object.
        if not isinstance(text, str):
            raise TypeError('CirConv accepts text only, %s is rejected.' % type(text))
        # Make character maps.
        self._make_charkeys()


    def convert(self):
        """Convert the text and place it into .result. No return."""
        self.result = self._charreplace(self.text)

    
    def _make_charkeys(self):
        """Make dictionary for character replacement"""
        if self.mode == "tolat":
            self.charmap = cyr
        elif self.mode == "tocyr":
            self.charmap = dict([v,k] for k,v in cyr.items())
        else:
            raise KeyError
        self.charkeys = self.charmap.keys() 


    def _charreplace(self, text):
        """Replace characters in the input text."""
        if self.calc_stats: # Don't bother with len() if no stats are needed
            len_in = len(text)
        # Replace the characters
        for letter in self.charkeys:
            if letter in text:
                text = text.replace(letter, self.charmap[letter])
        # Stats needed?
        if self.calc_stats:
            self._stats(len_in, len(text)) 
        return text

    
    def _stats(self, len_in, len_out):
        """Stats about conversion"""
        self.stats_char_original = len_in
        self.stats_char_replaced = len_out


    def get_converted(self):
        """"Return the converted text."""
        self.convert()
        return self.result