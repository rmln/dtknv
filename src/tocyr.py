#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""

Main convertor in Dtknv program.

See cknv.py for help.

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
import codecs
import zipfile
import shutil
import tempfile

from cyrconv import CirConv
from helpers import *

__version__ = "0.5"
__url__ = "https://gitorious.org/dtknv"
__author__ = "Romeo Mlinar"
__license__ = "GNU General Public License v. 3"

class ToCyr:
    """Converts textual content files from Cyrillic to Latin alphabet."""

    # File types that are listed in the open file dialogue.

    EXT = {'txt':'Neformatiran tekst',
           'html':'Hipertekst',
           'php':'PHP skripta',
           'xml':'Proširivi metajezik',
           'docx':'MS Word 2007+',
           'odt':'Open Ofis Pisac'}
            
    # Files that will be treated as plain text files.

    TEXTFILES = ["txt", "html", "php", "htm", "xml"]

    # Paths
    PATHIN = None
    PATHOUT = None
    
    # DIRTMP is debugging only. It actually runs faster when the temp
    # dir is cusom, rather than system.
    
    #DIRTMP = r'..\_tmp'

    # Default encoding.
    ENC = 'utf-8'
    # Mode of working.
    FILES = False
    # True if file nemes are converted.
    CONVERTFNAMES = False
    # Go into all directories.
    RECURSIVE = True
    # Show percentage counter while running.
    COUNTER = True
    # Show info about conversion while running. On Windows this causes an
    # error if messages are in UTF.
    SHOW = False
    # Not implemented yet: from Lat to Cyr or vice versa.
    MODE = 'tolat'
    # Show percentage counter while running.
    SHOWPERC = True
    # For debugging, to see how the script was called (GUI or console).
    CALLEDFROM = 'script'
    # A switch to prevent too much partying by the script.
    FAILSAFE = True
    # Default file name for simple report after the conversion.
    REPORT = 'dtknt-pregled-konverzije'
    

    def __init__(self):
        """Convert between Latin and Cyrillic scripts."""
        self.convertor = CirConv()
        self.conversiontype = None


    def run(self):
        """Start the conversion."""
        # Set temporary directory and add it the affix.
        # TODO: Add a check upon each start to see if
        # a file was left undeleted due to a crash.
        self.DIRTMP = tempfile.mkdtemp(prefix='dtknv_')
        
        # Percentage counter based on file sizes, to indicate
        # the conversion progress.
        self.pcounter = {'p':0, 'f':None, 'i':0}
        
        if os.path.isdir(self.PATHIN):
            self.conversiontype = 'dir'
        elif os.path.isfile(self.PATHIN):
            self.conversiontype = 'files'
        else:
            print('No file or directory as input. Aborting.')
            sys.exit(0)
        
        # Select file(s) or the whole directory and then
        # call the loop for conversion.
        if self.conversiontype == 'files':
            self.files_space = os.path.getsize(self.PATHIN)
            # Open lf log file, try converting and save
            # the report.
            lf = self._initreport()
            try:
                self._convertfile(self.PATHIN)
                msg = 'Konvertovana datoteka %s' % self.PATHIN
            except:
                msg = 'Greška, nije konvertovano: %s' % self.PATHIN
            print(msg)
            lf.write(msg)
        elif self.conversiontype == 'dir':
            self._convertdir()
        else:
            print('ConversionNotDefinedError')
            
        if self.SHOW:
            print('Konverzija zavrsena.')
        # Delete the tempdir.
        try:
            shutil.rmtree(self.DIRTMP)
        except:
            print('Could not remove tmp dir. Gracefully ignoring this...')


    def _initreport(self):
        """Initiate the report file and return the handle."""
        d = getdatetime(f='long')
        self.repfilename = self.REPORT + '_' + d + '_.txt'
        f = os.path.join(self._apppath(), self.repfilename)
        repfile = codecs.open(f, mode='w', encoding=self.ENC)
        repfile.write('DTknv datoteka o radu\r\n')
        repfile.write('Verzija programa: %s\r\n' % __version__)
        repfile.write('Datum/vrijeme: %s\r\n' % d)
        repfile.write('-----------------------------------\r\n\r\n')
        return repfile


    def _outpathrec(self, f):
        """Compile path where content will be saved."""
        if self.conversiontype == 'dir':
            # PATHIN = r'c:\\foo\\foo1'
            # f = r'c:\\foo\\foo1\\foo2\\bar.txt'
            path = f.split(self.PATHIN)[1]
            # The problem is that we have absolute path:
            # f = '\\foo2\\bar.txt'
            # Therefore, correct it:
            if 'posix' in os.name: # linux
                path = path.strip('/')
            else: # windows
                path = path.strip('\\')
            # Now, return the correct out path:
            final = os.path.join(self.PATHOUT, path)
            return final
        elif self.conversiontype == 'files':
            final = os.path.join(self.PATHOUT, filename(f))
            return final
        else:
            print('Unrecognized conversion type. Aborting.')
            sys.exit(0)


    def _checkife(self, f):
        """Check if the file f exists; if yes, add an underscore to the name."""
        i = 0
        while i < 50:
            if os.path.exists(f):
                i = i + 1
                path, fn = os.path.split(f)
                f = os.path.join(path, '_%s' % fn)
            else:
                return f
        sys.exit(0)


    def _renameresfiles(self, f):
        """Rename for media files in unzipped DOCX/ODT files."""
        if os.path.isdir(f):
            for i in self._getallfiles(f):
                os.rename(i, self._converttext(i))


    def _convertfile(self, f):
        """Convert the file content. Accept all defined file types."""
        # Compile the save path.
        outpath = self._outpathrec(f)
        # See if the filename needs conversion.
        outpath = self._converfname(outpath)
        # Create recursively the out dir.
        if self.RECURSIVE:
            makefullpath(outpath)
        # Deal with text files separately.
        self.extension = getext(f)
        if self.extension in self.TEXTFILES:
            try:
                text = self._load_txt(f)
                converted_text = self._converttext(text)
                self._save_txt(outpath, converted_text, check=True)
            except UnicodeEncodeError:
                print('ERROR reading in ._load_txt: %s' % f.encode(self.ENC))
                return('Error in conversion!')

        # Open Office / Libre Office Writer document.
        elif self.extension == 'odt':
            self._unzip(f)
            files = self._filterfiles(self.unzipped, 'xml')
            for odtxml in files:
                text = self._load_odt(odtxml)
                self._save_odt(odtxml, self._converttext(text))
            self._zip(outpath)

        # MS Office Word document.
        elif self.extension == 'docx':
            self._unzip(f)
            files = self._filterfiles((os.path.join(self.unzipped,
                    'word')), 'xml')
            for wordxml in files:
                text = self._load_docx(wordxml)
                self._save_docx(wordxml, self._converttext(text))
            self._zip(outpath)
        #Update the percentage counter.
        self._updatecounter(f)


    def _convertdir(self):
        """
        Calculate if there's enough free space.
        List files and call conversion function.
        """
        if self.conversiontype == 'dir':
            self.PATHOUT = getstampnewdir(self.PATHOUT)
            if self.RECURSIVE:
                # Map all files and folders
                loopover = get_paths('files', self.PATHIN)
            else:
                # Map only files (first level only).
                loopover = getallfiles(self.PATHIN)
        else:
            loopover = self.FILES
            
        # Filter out files with unsupported extensions.
        loopover = self._filtersupported(loopover)
        self.pcounter['all'] = len(loopover)
        
        # Calculate the size of all files for conversion:
        self.files_space = getfilesizes(loopover)
        free_space = getfreespace(self.PATHOUT)
        if self.files_space >= free_space:
            # No enough free space. Abort.
            print('Nema dovoljno slobodnog prostora na disku.')
            print('Kraj rada.')
            sys.exit()
        # Finally, convert the files.
        self._conversionloop(loopover)


    def calculatedirsize(self, path):
        """Calculate size of all supported files. Depends on RECURSIVE.

        If RECURSIVE = True, then it returns the size of all files in the
        tree; if False, then it returns only files in current folder.

        The size is formated with '%0.2f'.

        """
        if self.RECURSIVE:
            files = self._filtersupported(get_paths('files', path))
        else:
            files = self._filtersupported(getallfiles(path))
        size = getfilesizes(files)
        return (len(files),  size/(1024*1024.0))


    def _converfname(self, path):
        """Sees if filename/dirname needs conversion, and converts if yes."""
        if self.CONVERTFNAMES:
            path, f = os.path.split(path)
            cf = self._converttext(f)
            is_same = (cf == f)
            if not is_same:
                if self.SHOW:
                    print('Naziv datoteke prebacen u latinicu...')
            return os.path.join(path, cf)
        else:
            return path


    def _conversionloop(self, loopover):
        """Iterate over items and convert."""
        # Convert all files in the loop:
        if self.FAILSAFE:
            repfile = self._initreport()
        for f in loopover:
            if self.SHOW:
                print('Ucitava se %s' % f.encode(self.ENC))
            if self.FAILSAFE:
                try:
                    self._convertfile(f)
                    repfile.write('OK: %s\r\n' % f)
                except:
                    print('\tOps, greska! Ova datoteka nije konvertovana...')
                    repfile.write('GREŠKA: %s\r\n' % f)
            else:
                self._convertfile(f)
        print('Konverzija zavsena. Provjerite izvjestaj.')


    def _updatecounter(self, f):
        """Update the percentage counter."""
        size = os.path.getsize(f)
        if not size == 0:
            self.pcounter['p'] += (size/self.files_space)*100
        self.pcounter['f'] = filename(f)
        self.pcounter['i'] += 1
        if self.SHOWPERC and (self.conversiontype != 'files'):
            pround = round(self.pcounter['p'], 2)
            print('Datoteka %s od %s. Ukupno konvertvano %s%% bajtova.' % \
                                                (self.pcounter['i'],
                self.pcounter['all'], pround))
                


    def _converttext(self, text):
        """Convert the text to Latin and return it."""
        self.convertor.text = text
        self.convertor.convert()
        return self.convertor.result


    def _filterfiles(self, d, ext):
        """Return only files of the extension specified."""
        return [i for i in os.listdir(d) if getext(i) == ext]


    def _filtersupported(self, fs):
        """Return files with supported extensions."""
        return [i for i in fs if getext(i) in self.EXT.keys()]


    def _outpath(self, f):
        """Return out path."""
        return os.path.join(self.PATHOUT, filename(f))


    def _load_txt(self, f):
        """Load and return plain text based files."""
        return codecs.open(f, encoding = self.ENC, mode="r").read()


    def _load_odt(self, f):
        """Load and return content file of ODT."""
        return self._load_txt(os.path.join(self.unzipped, f))


    def _load_docx(self, f):
        """Load and return content file of DOCX."""
        return self._load_txt(os.path.join(self.unzipped, 'word', f))


    def _save_txt(self, f, text, check=False):
        """Saves text based files.
        
        Check if the file already exists. This applies only
        to saving text-based files. In ODT/DOCX they are
        automatically overwritten.
        """
        if check:
            f = self._checkife(f)
        codecs.open(f, encoding=self.ENC, mode="w").write(text)


    def _save_odt(self, f, text):
        """Save content ODT file."""
        self._save_txt(os.path.join(self.unzipped, f), text)


    def _save_docx(self, f, text):
        """Save file member of DOCX."""
        self._save_txt(os.path.join(self.unzipped, 'word', f), text)


    def _checkifexists(self, f):
        """Check if path exists. If yes, add the underscore."""
        #TODO: Is this a repeated piece of code?
        if os.path.isfile(f):
            split = os.path.split(f)
            return os.path.join(split[0], '_' + split[1])
        else:
            return f


    def _unzip(self, f):
        """Unzip file content into temporary folder."""
        # Convert the script of the filename (датотека.txt > datoteka.txt)
        # This has to  be done here, or the program will not find the path.
        #fname = self._converfname(filename(f))
        fname = filename(f)
        # Unzipped is the path to the temp subfolder where the file
        # is to be unzipped.
        maketmpdir(self.DIRTMP)
        self.unzipped = makesubdir(self.DIRTMP, fname)
        z = zipfile.ZipFile(f)
        z.extractall(self.unzipped)


    def _zip(self, path):
        """Zip file the path points to."""
        if self.conversiontype == 'files':
            path = self._checkife(path)
        # Store current working dir so it can be restored later.
        cwdu = os.getcwd()
        z = zipfile.ZipFile(path, 'w')
        os.chdir(self.unzipped)
        for r, d, files in os.walk('.'):
            for fz in files:
                z.write(os.path.join(r, fz))
        z.close()
        # Restore working dir.
        os.chdir(cwdu)
        shutil.rmtree(self.unzipped)


    def _apppath(self):
        """Return application path without 'src' part."""
        return os.getcwd().split('src')[0]