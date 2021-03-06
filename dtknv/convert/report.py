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

__version__ = '0.3'
__url__ = "https://gitorious.org/dtknv"
__author__ = "Romeo Mlinar"
__license__ = "GNU General Public License v. 3"

import os
import sys
import codecs
import helpers
import version

class Report:
    """
    Class for creating reports of conversion, with some stats.
    """    
    def __init__(self, cn=False, reppath=None, flush=True):
        """
        Start Report() call.
        """
        if not cn:
            raise RuntimeError('Host class (cn) must be supplied.')
        else:
            self.cn = cn
            
        self.flush = flush
        reppath = self.cn.REPORTPATH
        if not os.path.exists(reppath):
            raise OSError("Report path does not exist.")
        if not os.path.isdir(reppath):
            raise ValueError("Report path must be a directory.")
        self.reppath = reppath

        self.dt = helpers.getdatetime(f='long')
        self.repopened = self._openfile()
        self._saveinitial()
        
    def _openfile(self):
        """
        Open the report file.
        """ 
        f = os.path.join(self.reppath, self._filename())
        if self.cn.SHOW:
            print('Izvjestaj o radu je u:\r\n', f)
        opened = codecs.open(f, mode='w', encoding=self.cn.ENC)
        self.file = f
        return opened 
    
    def _filename(self):
        """
        Return the filename.
        """
        return self.cn.REPORTNAME  + self.dt + '.txt'
    
    def _saveinitial(self):
        """
        Save the initial text.
        """
        t = 70*'-' + '\r\n'
        t = t + 'DTknv datoteka o radu\r\n'
        t = t + 70*'-' + '\r\n'
        t = t + 'Verzija programa: %s\r\n' % version.__version__
        t = t + 'Datum i vrijeme: %s\r\n' % self.dt
        if not self.cn.USERAM:
            t = t + 'Raspakivanje: Na disk (sporiji način, provjerite ' + \
                'podešavanja).\r\n'
        t = t + 70*'-' + '\r\n'
        self.write(t)
    
    def write(self, text):
        """
        Write into the file.
        """
        self.repopened.write(text)
        if self.flush:
            self.repopened.flush()
    
    def close(self):
        """
        Close the report file.
        """
        self.repopened.close()
