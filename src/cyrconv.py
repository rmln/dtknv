#! /usr/bin/python3
"""

Converts Cyrillic script to Latin.

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

__version__ = '1.0'

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

    def __init__(self, text='', mode="tolat"):
        "start the class"
        self.text = text
        self.mode = mode
        if mode == "tolat":
            self.charmap = cyr
        elif mode == "tocyr":
            self.charmap = dict([v,k] for k,v in cyr.items())
        else:
            raise KeyError("Unesite tolat ili tocyr za konverziju.")

    def convert(self):
        text = self.text
        self.result = self._charreplace(text)

    def _charreplace(self, text):
        "Replace cherecters in text"
        charkeys = self.charmap.keys()
        for letter in charkeys:
            if letter in text:
                text = text.replace(letter, self.charmap[letter])
        return text

    def get_converted(self):
        "Return the conversion."
        self.convert()
        return self.result
