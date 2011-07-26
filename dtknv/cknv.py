#! /usr/bin/python3
"""

Dtknv is a simple tool that converts files containing Serbian Cyrillic
alphabet into Serbian Latin alphabet.

It converts DOCX and ODT files, as well as all text-based files, if
supported extensions are supplied.

PREREQUISITES

Windows: Python 3+
Linux: python3 for console use; python3-tk for GUI

=== CONSOLE ================

Use the following switches to run the program:

    -i (--pathin)       Input directory of file.
    -o (--pathout)      Output directory.
    -e (--encoding)     Encoding (the default is utf-8).
    -n (--names)        Convert names.
    -r (--recursive)    Recursive conversion. Be careful!
    -s (--show)         Show report while running.
    -c (--conversionreportname) Conversion report name.
    -f (--nofailsafe)   Abort conversion on the first file failure.
    -m (--noram)        Unzip odt/docx files on disk, and not in RAM
                        (slower).
    -g (--gui)          Show graphical interface (overrides console commands).

Conslole examples:

(1)
cknv.py -i /home/me/Documents/myfiles -o /home/me/Documents/conv -r -n

This will convert all supported files in all directories in myfiles. Also,
file names will be converted if they are in the Cyrillic script. A new folder
will be created in conv for each run (the names start with rcon-hour_min_sec).

(2)
cknv.py -i /home/me/Documents/myfiles -o /home/me/Documents/conv -e utf-16

Only files in myfiles will be converted; the utf-16 encoding will be used to
open files/log.

(3)
cknv.py -i /home/me/Documents/myfile.odt -o /home/me/Documents/conv

Convert myfile.odt and store it in conv.

(4)
cknv.py -g

Show a simple graphical interface.

=== GUI ====================

Double-click on rungui.py to start a simple graphical interface, or
type cknv.py -g in console.

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
    #Test ---------------------------------------------------------------------
    #Arguments, just for testing here, on both systems
    #if os.name == 'nt':
    #    args = '-r -i D:\\datastore\\tocyr\\in_files1f\\ -o D:\\datastore\\tocyr\\out_files'
    #    args = args + ' '
    #else:
    #    args = '-r -i /home/marw/Documents/testdtknv/test1f/otrvorenidokument-ispravno.odt -o /home/marw/Documents/testout'
    #    args = args + ' '
    #args = args.split()
    #Test ---------------------------------------------------------------------
    args = sys.argv[1:] # Uncomment if not testing!
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
        supplied, r = getopt.getopt(args, 'i:o:e:c:snrhfmg', ['pathin=',
                    'pathout=', 'encoding=', 'conversionreportname=', 'show',
                    'names', 'recursive', 'help', 'nofailsafe', 'noram', 'gui'])
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
        elif o in ('-s', '--show'):
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
            
    if SHOWGUI == True:
        del(c)
        from gui import gui
        gui.bootgui()
    else:
        c.run()