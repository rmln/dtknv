#! /usr/bin/python3
"""

Dtknv je jednostavna alatka za konverziju datoteka sa ćiriličnim
sadržajem u latinični. Moguće je konvertovati tekstualne datoteke, ali
i Libreofis (Openofis) i Vord dokumenta (samo DOCX). Grafički
interfejs podržava i prebacivanje latinice u ćirilicu, ali za sada samo
u ograničenom tekstualnom modu.

Komande:

    -i (--pathin)
	Ulazna putanja (fascila ili datoteka).
    -o (--pathout)
	Izlazna putanja.
    -e (--encoding)     
	Kodna strana (standardno utf-8).
    -n (--names)
	Konvertuj nazive datoteka.
    -r (--recursive)
	Rekurzivna konverzija. Pažljivo!
    -v (--verbose)
	Prikazuj izvještaj prilikom rada.
    -c (--conversionreportname) 
	Naziv datoteke za izvještaj.
    -f (--nofailsafe)
	Obustavi konverziju prilikom prve greške.
    -m (--noram)
	Raspakuj odt/docx na disk (standardno RAM) 
    -g (--gui)
	Prikaži sučelje (zanemaruje ostale komande).
    -s (--sameoutpath)
	Izlazna putanja ista kao ulazna (dodaje se novi 
        nastavak na naziv datoteke).
        
"""

#
# A checklist before deployment:
#
#    - zip mode on?
#    - failsafe on?
#    - testing args commented?
#    - readme updated?
#    - info about changes updated?
#    - runs on Linux?
#

__url__ = "https://gitorious.org/dtknv"
__author__ = "Romeo Mlinar"
__license__ = "GNU General Public License v. 3"

import os
import sys
import getopt

__version__ = '0.3.1'

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

def usage():
    """Print help"""
    print(__doc__)
    
if __name__ == '__main__':
    """Execute the script.

    1. See if ToCyr() can be initialised.
    2. Check if command line arguments are supplied.
    3. Run!

    """
    args = sys.argv[1:]
    # If nothing is supplied, show help and exit:
    if len(args) == 0:
        usage()
        sys.exit(2)
    # Try initialising the class:
    try:
        from convert.tocyr import ToCyr
        c = ToCyr()
        c.SHOW = False
        c.RECURSIVE = False
    except:
        raise RuntimeError('Could not initialise TocCyr.')
    # Gui variable can override command calls
    SHOWGUI = False
    # Command line arguments
    try:
        supplied, r = getopt.getopt(args, 'i:o:e:c:vnrhfmgs', ['pathin=',
                    'pathout=', 'encoding=', 'conversionreportname=', 'verbose',
                    'names', 'recursive', 'help', 'nofailsafe', 'noram', 'gui', 'sameoutpath'])
    except:
        usage()
        sys.exit(2)
    for o, a in supplied:
        if o in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif o in ('-i', '--pathin'):
            c.PATHIN = a
        elif o in ('-o', '--pathout'):
            c.PATHOUT = a
        elif o in ('-e', '--encoding'):
            c.ENC = a
        elif o in ('-v ', ' --verbose'):
            c.SHOW = True
        elif o in ('-n', '--names'):
            c.CONVERTFNAMES = True
        elif o in ('-r', '--recursive'):
            c.RECURSIVE = True
        elif o in ('-c', '--conversionreportname'):
            c.REPORT = a
        elif o in ('-f', '--nofailsafe'):
            c.FAILSAFE = False
        elif o in ('-m', '--noram'):
            c.USERAM = False
        elif o in ('-g', '--gui'):
            SHOWGUI = True
        elif o in ('-s', '--sameouthpath'):
            c.SAMEOUTPATH = True
            
    if SHOWGUI == True:
        del(c)
        from gui import gui
        gui.bootgui()
    else:
        c.run()
