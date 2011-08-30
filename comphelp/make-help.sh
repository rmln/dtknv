#! /usr/bin/env bash
echo Brisanje...
rm ~/code/dtknv/comphelp/dtknv.html
rm -rf slike

echo Kompajliranje..
xsltproc -o ~/code/dtknv/comphelp/dtknv.html /usr/share/xml/docbook/stylesheet/nwalsh/xhtml/docbook.xsl /home/marw/code/dtknv/doc/text/dtknv.xml

echo Kopiranje slika...
mkdir slike
cp ~/code/dtknv/doc/img/*.png ~/code/dtknv/comphelp/slike/

echo Otvaranje...
google-chrome /home/marw/code/dtknv/comphelp/dtknv.html &
