#! /usr/bin/python3
"""

Help functions for tocyr3.

"""

__version__ = '0.2.1'
__url__ = "https://gitorious.org/dtknv"
__author__ = "Romeo Mlinar"
__license__ = "GNU General Public License v. 3"


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
import ctypes
from time import strftime

import version

def get_version(v=version.__version__):
    """Separate the version tag into tuple numbers
    and string description"""
    ver = v.split(" ")
    vtag = ver[1]
    vnum = [int(i) for i in ver[0].split('.')]
    return(vnum, vtag)

def get_version_comparison(v1=None, v2=None):
    """Return lower, higher or same
    version, when compared v1 to v2."""
    # If v1 is None, then compare to the corrent version
    if v1 == None:
        v1 = get_version()[0]
    else:
        v1 = get_version(v1)[0]
    v2 = get_version(v2)[0]
    # calculate version differences
    if v1[0] > v2[0]:
        return('higher')
    elif v1[0] == v2[0]:
        if v1[1] > v2[1]:
            return('higher')
        if v1[1] < v2[1]:
            return('lower')
        if v1[1] == v2[1]:
            if v1[2] == v2[2]:
                return("same")
            if v1[2] > v2[2]:
                return("higher")
            if v1[2] < v2[2]:
                return("lower")
    else:
        return("lower")
                

def def_report_path():
    """Return the default report path"""
    if os.name == 'nt':
        return(getwindoc())
    else:
        return(os.getenv("HOME"))


def getwindoc():
    """Get Windows document folder

    From Josh Purvis on <http://stackoverflow.com/
    questions/3927259/how-do-you-get-the-exact-path-to-my-documents>

    via

    <http://bugs.python.org/issue1763#msg62242>
    
    """
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(300)
    dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False)
    return(buf.value)

def getstampnewdir(path):
    """Get time/date stamped name"""
    d = 'rkonv-%s' % getdatetime()
    d = os.path.join(path, d)
    os.mkdir(d)
    return d

def build_directory_tree(dirin, dirout):
    """Build directory tree in DIROUT, based on DIRIN"""
    # We won't allow making directories in the
    # DIROUT directory, but in newly created one.
    # This is to prevent possible deletion.
    timestapped = 'rkonv-%s' % getdatetime()
    three_path = os.path.join(dirout, timestapped)
    os.mkdir(three_path)
    # Finally, make some dirs!
    for p in get_paths('directories', dirin):
        dir_to_make = os.path.join(three_path,
                      p[len(dirin)+1:])
        try:
            os.mkdir(dir_to_make)
        except:
            print('Prekid. Greska u stvaranju mape foldera.')
            sys.exit()
    # Change DIROUT to point to a newly created dir:
    dirout = three_path

def getallfiles(path, ext=False):
    """Get all files paths from a directory."""
    paths = []
    for i in os.listdir(path):
        # Select files only, filter out folders:
        fullpath = os.path.join(path, i)
        if os.path.isfile(fullpath):
            # Is there filtering?
            if ext:
                if getext(fullpath) == ext:
                    paths.append(os.path.join(path, i))
            else:
                paths.append(os.path.join(path, i))
    return paths

def getfilesizes(files):
    """Calculate size of the files"""
    filessize = 0
    for i in files:
        filessize = filessize + os.path.getsize(i)
    return filessize

def getfreespace(path):
    """Get free space of a drive path points to."""
    # Code by Frankovskyi Bogdan
    # at: <http://stackoverflow.com/questions/51658/
    #     cross-platform-space-remaining-on-volume-using-python>
    if os.name == 'nt':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(path),
            None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        # This dows not work with the rest of the
        # logic in the programme:
        return os.statvfs(path).f_bfree * os.statvfs(path).f_bsize

def getext(f):
    """Return the extension."""
    return os.path.splitext(f)[1].lower()[1:]


def filename(f):
    """Return filename."""
    return os.path.split(f)[1]


def getdatetime(f='short'):
    """Return current date and time"""
    if f == 'short':
        return strftime("%H_%M_%S")
    elif f == 'long':
        return strftime("%Y-%m-%d-%H-%M")
    else:
        raise()


def maketmpdir(tempdir):
    """See if temporary file exists, and if not, make it."""
    if not os.path.exists(tempdir):
        os.mkdir(tempdir)


def makesubdir(tpmdir, add):
    """Make subdirectory in temporary folder."""
    dir = os.path.join(tpmdir, add)
    if not os.path.exists(dir):
        os.mkdir(dir)
    return dir

def makefullpath(path):
    """Make full path. MUST BE A PATH TO A FILE."""
    try:
        os.makedirs(os.path.split(path)[0])
    except:
        pass


def get_paths(what, path):
    """Get all files or directory paths in path.
    Thanks to jerub at
    http://stackoverflow.com/questions/120656/directory-listing-in-python
    """
    paths = []
    for dirname, dirnames, filenames in os.walk(path):
        if what == 'directories':
            for subdirname in dirnames:
                paths.append(os.path.join(dirname, subdirname))
        if what == 'files':
            for filename in filenames:
                paths.append(os.path.join(dirname, filename))
    return paths
