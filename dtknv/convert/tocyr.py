#! /usr/bin/python3

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

from srpismo.cyrconv import CirConv 
from formats.formats import OfficeZIP
from convert.report import Report

import helpers
from helpers import *
import version

__version__ = "0.6.3.5"
__url__ = "https://gitorious.org/dtknv"
__author__ = "Romeo Mlinar"
__license__ = "GNU General Public License v. 3"

class ToCyr:
    """Converts textual content files from Cyrillic to Latin alphabet."""

    # File types that are listed in the open file dialogue.

    EXT = ('txt', 'html','docx', 'odt')
            
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
    REPORT = 'dtknv-'
    # Unpack type
    USERAM = True
    # Suffix added to the converted file where
    # in and out paths are the same.
    CONVSUFFIX = '_konv'
    # In and out paths are the same?
    SAMEOUTPATH = True
    # Path to save reports
    REPORTPATH = helpers.def_report_path()

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
        
        # Remains false if no error occurs during
        # conversion.
        self.errors_during_work = False
        
        if os.path.isdir(self.PATHIN):
            self.conversiontype = 'dir'
        elif os.path.isfile(self.PATHIN):
            self.conversiontype = 'files'
        else:
            # "Input file/directory was not find." 
            print('Ulazna fasickla/datoteka nije nadjena.')
            sys.exit(0)
        
        # Select file(s) or the whole directory and then
        # call the loop for conversion.
        if self.conversiontype == 'files':
            self.files_space = os.path.getsize(self.PATHIN)
            # Open lf log file, try converting and save
            # the report.
            self.report = Report(cn=self)
            try:
                self._convertfile(self.PATHIN)
                msg = 'Konvertovana datoteka %s' % self.PATHIN
            except:
                self.errors_during_work = True
                msg = 'Greska, nije konvertovano: %s' % self.PATHIN
                if self.SHOW:
                    print(msg)
            self.report.write(msg)
        elif self.conversiontype == 'dir':
            self._convertdir()
        else:
            # "Conversion must be 'files' or 'dir'"
            raise ValueError('Konverzija mora biti "files" ili "dir".')
            
        if self.SHOW:
            # "Conversion finished."
            print('Konverzija zavrsena.')
        # Delete the tempdir.
        try:
            shutil.rmtree(self.DIRTMP)
        except:
            #'Could not remove tmp dir. Gracefully ignoring this...'
            print("Tmp fasickla nije mogla bit uklonjena. Psssssst!")


    def _outpathrec(self, f):
        """Compile path where content will be saved."""
        # The out path is the same as in path, so
        # just add self.CONVSUFFIX to filename, ie:
        # bar.txt > bar_cir.txt
        if self.SAMEOUTPATH:
            split_path = os.path.splitext(f)
            outpath = os.path.join(split_path[0] + \
                      self.CONVSUFFIX + split_path[1])
            return outpath
        
        # In and out paths are not the same, so continue.      
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
            #'Unrecognized conversion type. Aborting.'
            print('Nepoznata vrsta konverzije. Prekid rada.')
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
        raise ValueError('Prekoracen broj provjera za isti  naziv.')


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
        # See if the file already exists, if yes, add an underscore.
        outpath = self._checkife(outpath)
        # Create recursively the out dir.
        if self.RECURSIVE:
            makefullpath(outpath)
        # Deal with text files separately.
        self.extension = getext(f)
        if self.extension in self.TEXTFILES:
            try:
                text = self._load_txt(f, nomem=True)
                converted_text = self._converttext(text)
                self._save_txt(outpath, converted_text, check=True, nomem=True)
            except UnicodeEncodeError:
                # 'ERROR reading in ._load_txt: %s' % f.encode(self.ENC)
                print('GRESKA u funkciji  ._load_txt: %s' % f.encode(self.ENC))
                # 'Error in conversion!'
                return('Greska u konverziji!')
            
        
        if self.extension in ('odt', 'docx'):
            self._unzip(f)
            if self.USERAM:
                self._newzip(outpath)
            files = self._filterfiles(self.unzipped, 'xml')
            for xmlfile in files:
                text = self._load_office(xmlfile)
                self._save_office(xmlfile, self._converttext(text))
            self._zip(outpath)

        self._updatecounter(f)


    def _convertdir(self):
        """
        Calculate if there's enough free space.
        List files and call conversion function.
        """
        if self.conversiontype == 'dir':
            if self.SAMEOUTPATH:
                self.PATHOUT = self.PATHIN
            else:
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
                    # "File name converted to Latin."
                    print('Naziv datoteke prebacen u latinicu...')
            return os.path.join(path, cf)
        else:
            return path


    def _conversionloop(self, loopover):
        """Iterate over items and convert."""
        # Convert all files in the loop:
        if self.FAILSAFE:
            self.report = Report(cn=self)
        for f in loopover:
            if self.SHOW:
                # "Loading %s"
                print('Ucitava se %s' % f.encode(self.ENC))
            if self.FAILSAFE:
                try:
                    self._convertfile(f)
                    self.report.write('OK: %s\r\n' % f)
                except:
                    # "Ooops! This file was not converted..."
                    print('\tOps, greska! Ova datoteka nije konvertovana...')
                    # "ERROR: "
                    self.report.write('GREŠKA: %s\r\n' % f)
                    self.errors_during_work = True
            else:
                self._convertfile(f)
        # "Conversion done. Check report, if on."
        print('Konverzija zavsena. Provjerite izvjestaj, ako je ukljucen.')
        
        try:
            self.report.close()
        except:
            pass


    def _updatecounter(self, f):
        """Update the percentage counter."""
        size = os.path.getsize(f)
        if not size == 0:
            self.pcounter['p'] += (size/self.files_space)*100
        self.pcounter['f'] = filename(f)
        self.pcounter['i'] += 1
        if self.SHOWPERC and (self.conversiontype != 'files'):
            pround = round(self.pcounter['p'], 2)
            # "File %s of %s. Total converted %s%%."
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
        if self.USERAM:
            toconvert = []
            self.zipother = []
            for i in self.unzipped.zip.filelist:
                if os.path.splitext(i.filename)[1] == '.xml':
                    toconvert.append(i.filename)
                else:
                    self.zipother.append(i.filename)
            return toconvert
        else:
            return [i for i in os.listdir(d) if getext(i) == ext]


    def _filtersupported(self, fs):
        """Return files with supported extensions."""
        return [i for i in fs if getext(i) in self.EXT]


    def _outpath(self, f):
        """Return out path."""
        return os.path.join(self.PATHOUT, filename(f))


    def _load_txt(self, f, nomem=False):
        """Load and return plain text based files."""
        if self.USERAM and not nomem:
            z = self.unzipped.zip.open(f)
            encread = codecs.EncodedFile(z, self.ENC, self.ENC).read()
            ecodedtext = encread.decode(self.ENC)
            return ecodedtext
        else:
            return codecs.open(f, encoding = self.ENC, mode="r").read()

    def _load_office(self, f):
        """Load file and return textual content."""
        if self.USERAM:
            return self._load_txt(f)
        else:
            return self._load_txt(os.path.join(self.unzipped, f))
            

    def _save_txt(self, f, text, check=False, nomem=False):
        """Saves text based files.
        
        Check if the file already exists. This applies only
        to saving text-based files. In ODT/DOCX they are
        automatically overwritten.
        """
        if self.USERAM and not nomem:
            pass
        else:
            if check: 
                f = self._checkife(f)
            codecs.open(f, encoding=self.ENC, mode="w").write(text)

    def _save_office(self, f, text):
        """Save an office file."""
        if self.USERAM:
            self.zipout.writestr(f, text.encode(self.ENC))
        else:
            self._save_txt(os.path.join(self.unzipped, f), text)


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
        fname = helpers.filename(f)
        if self.USERAM:
            self.unzipped = OfficeZIP(f)
        else:
            # Unzipped is the path to the temp subfolder where the file
            # is to be unzipped.
            maketmpdir(self.DIRTMP)
            self.unzipped = makesubdir(self.DIRTMP, fname)
            z = zipfile.ZipFile(f)
            z.extractall(self.unzipped)
    
    def _newzip(self, outpath):
        """Create new zip object"""
        self.zipout = zipfile.ZipFile(outpath, mode='w')


    def _zip(self, path):
        """Zip file the path points to."""
        if self.USERAM:
            # Save into zip the files that did not
            # need the conversion, to complete the
            # output zip.
            for i in self.zipother:
                content = self.unzipped.zip.read(i)
                self.zipout.writestr(i, content)
            self.zipout.close()
        else:
            if self.conversiontype == 'files':
                path = self._checkife(path) # TODO: Check this in ZIP mode
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
