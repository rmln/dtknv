Dtknv is a simple tool that converts files containing Serbian Cyrillic
alphabet into Serbian Latin alphabet.

It converts DOCX and ODT files, as well as all text-based files, if
supported extensions are supplied.

Basic Latin to Cyrillic conversion is supported for plain text, 
in GUI only. Launch the window (rungui.py) and hit the "Konverzija
teksta" button.

=== PREREQUISITES =========

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


=== ABOUT ==================

Beta version.
License GNU GLP 3.
More, in Serbian: <http://digitalnitrg.blogspot.com/2011/03/dt-konvertor-datoteka-iz-cirilice-u.html>

-- 
Cheers,
R.
