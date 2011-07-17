#! /usr/bin/python3
"""

Read a zip file and return the object.

"""

__url__ = "https://gitorious.org/dtknv"
__author__ = "Romeo Mlinar"
__license__ = "GNU General Public License v. 3"

import os
import io
import codecs
import zipfile


class OfficeZIP:
    """Returned ZIP object"""
    def __init__(self, infile):
        """Open and return zip file"""
        self.infile = infile
        self.zip = zipfile.ZipFile(self.infile, mode='r')
    
    def _unzip(self):
        """Unzip a file"""
        return zipfile.ZipFile(self.infile, mode='r')