Dtknv is a simple tool that converts files containing Serbian Cyrillic
alphabet into Serbian Latin alphabet.

It converts DOCX and ODT files, as well as all text-based files, if the
extensions are supplied.

PREREQUISITES

Windows: Python 3+
Linux: python3 for console use; python3-tk for GUI

=== CONSOLE ================

This file is a console wrapper for tocyr.

Use the following switches to run the program:

    -i (--pathin)       Input directory of file.
    -o (--pathout)      Output directory.
    -e (--encoding)     Encoding (the default is utf-8).
    -n (--names)        Convert names.
    -r (--recursive)    Recursive conversion. Be careful!
    -s (--show)         Show report while running.
    -c (--conversionreportname) Conversion report name.

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

=== GUI ====================

Use DTKnv.py to start a simple graphical interface.

ABOUT
Alpha version.
License GNU GLP 3.
More, in Serbian: <http://digitalnitrg.blogspot.com/2011/03/dt-konvertor-datoteka-iz-cirilice-u.html>

-- 
Cheers,
R.
