#! /usr/bin/python3
"""

Module for creating reports for tocyr converter.

"""

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

__version__ = '0.1'
__url__ = "https://gitorious.org/dtknv"
__author__ = "Romeo Mlinar"
__license__ = "GNU General Public License v. 3"

import os
import codecs
import helpers
import version

class Report:
    
    def __init__(self, cn=False, reppath='..', flush=True):
        """Start Report() call"""
        if not cn:
            raise RuntimeError('Host class (cn) must be supplied.')
        else:
            self.cn = cn
        self.flush = flush
        self.reppath = reppath
        self.dt = helpers.getdatetime(f='long')
        self.repopened = self._openfile()
        self._saveinitial()
        
    def _openfile(self):
        """Open the report file."""
        f = os.path.join('..', self._filename())
        #if self.cn.SHOW:
        if True:
            print('Izvjestaj o radu je u:\r\n', f)
        opened = codecs.open(f, mode='w', encoding=self.cn.ENC)
        return opened 
    
    def _filename(self):
        """Return filename"""
        return self.cn.REPORT + '_' + self.dt + '.txt'
    
    def _saveinitial(self):
        """Save initial text"""
        if self.cn.USERAM:
            mode = 'RAM (brži način).\r\n'
        else:
            mode = 'Na disk (sporiji način, provjerite podešavanja).\r\n'
        t = 70*'-' + '\r\n'
        t = t + 'DTknv datoteka o radu\r\n'
        t = t + 70*'-' + '\r\n'
        t = t +'Verzija programa: %s\r\n' % version.__version__
        t = t +'Datum/vrijeme: %s\r\n' % self.dt
        t = t + 'Raspakivanje: %s' % mode
        t = t + 70*'-' + '\r\n'
        self.write(t)
    
    def write(self, text):
        """Write into the file"""
        self.repopened.write(text)
        if self.flush:
            self.repopened.flush()
    
    def close(self):
        """Close the report file"""
        self.repopened.close()