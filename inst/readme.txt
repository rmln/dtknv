Dtknv is a simple tool that converts files containing Serbian Cyrillic
alphabet into Serbian Latin alphabet and vice versa.

It converts DOCX and ODT files, as well as all text-based files, if
supported extensions are supplied.

The newest version (0.5 beta) has exception searches (search and
replace strings), but the option is available through the GUI only.

Help file is available on <http://serbian.languagebits.com/dtknv/doc/> 
(Serbian only).

How to run it:

python3 dtknv/cknv.py

Or:

python3 dtknv/cknv.py -g

=== PREREQUISITES =========

Windows: Python 3
Linux: python3 for console use; python3-tk for GUI

=== GUI ====================

python3 dtknv/cknv.py -g

=== IN ENGLISH ============

To swicth the inteface language to English:
"Opcije" > "Jezik sučelja" > "English"

=== CONSOLE ================

We advise you to use GUI interface.

    -i (--pathin)       Input directory of file.
    -o (--pathout)      Output directory.
    -e (--encoding)     Encoding (the default is utf-8).
    -n (--names)        Convert names.
    -r (--recursive)    Recursive conversion. Be careful!
    -v (--show)         Show report while running.
    -c (--conversionreportname) Conversion report name.
    -f (--nofailsafe)   Abort conversion on the first file failure.
    -m (--noram)        Unzip odt/docx files on disk, and not in RAM
                        (slower).
    -g (--gui)          Show graphical interface (overrides console commands).
    -s (--sameoutpath)  The out path same as input (a string is appended
       			onto the new file)
    -t (--text)         Convert text in console (must be of the same script)

Conslole examples:

(1)
cknv.py -i /home/me/Documents/myfiles -o /home/me/Documents/conv -r -n

This will convert all supported files in all directories in
myfiles. Also, file names will be converted if they are in the
Cyrillic script. A new folder will be created in conv for each run
(the names start with rcon-hour_min_sec).

(2)
cknv.py -i /home/me/Documents/myfiles -o /home/me/Documents/conv -e utf-16

Only files in myfiles will be converted; the utf-16 encoding will be
used to open files/log.

(3)
cknv.py -i /home/me/Documents/myfile.odt -o /home/me/Documents/conv

Convert myfile.odt and store it in conv.

(4)
cknv.py -g

Show a simple graphical interface.

(5)
$ cknv.py -t "Ovo je proba."

returns:
$ Ово је проба. 

=== ABOUT ==================

Beta version.
License GNU GPL 3.
<http://serbian.languagebits.com/dtknv/>

-- 
Cheers,
R.
