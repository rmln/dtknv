@echo off
echo ----------------------------------------------------------------
echo Dist skripta za dtknv, v. 1.0
echo ----------------------------------------------------------------

set /p dir=Ime za novi folder? 

echo Dio 1: Arhiviranje izvornog koda.

echo Pravi se folder %dir%... 
md D:\apps\portablepy\dist\%dir%

echo Prave se folderi...
md D:\apps\portablepy\dist\%dir%\dtknv
md D:\apps\portablepy\dist\%dir%\dtknv\convert
md D:\apps\portablepy\dist\%dir%\dtknv\formats
md D:\apps\portablepy\dist\%dir%\dtknv\gui

REM echo Brisanje setup.py datoteke
REM del D:\code\dtknv\src\setup.py

echo Kopiranje datoteka txt u dtknv...
copy D:\code\dtknv\inst\changes.txt D:\apps\portablepy\dist\%dir%
copy D:\code\dtknv\inst\gpl.txt D:\apps\portablepy\dist\%dir%
copy D:\code\dtknv\inst\readme.txt D:\apps\portablepy\dist\%dir%

echo Kopiranje pokrenime.bat datoteke...
copy D:\code\dtknv\inst\pokrenime.bat D:\apps\portablepy\dist\%dir%

echo Kopiranje py datoteka u dtknv...
copy D:\code\dtknv\dtknv\*.py D:\apps\portablepy\dist\%dir%\dtknv

echo Kopiranje py datoteka u convert...
copy D:\code\dtknv\dtknv\convert\*.py D:\apps\portablepy\dist\%dir%\dtknv\convert

echo Kopiranje py datoteka u formats...
copy D:\code\dtknv\dtknv\formats\*.py D:\apps\portablepy\dist\%dir%\dtknv\formats

echo Kopiranje py datoteka u gui...
copy D:\code\dtknv\dtknv\gui\*.py D:\apps\portablepy\dist\%dir%\dtknv\gui

echo Zipovanje...
D:\apps\7za920\7za.exe a -tzip D:\apps\portablepy\dist\%dir%c.zip D:\apps\portablepy\dist\%dir%\dtknv
D:\apps\7za920\7za.exe u -tzip D:\apps\portablepy\dist\%dir%c.zip D:\apps\portablepy\dist\%dir%\*.txt
echo Arhiviranje skripte zavrseno.

REM =====================================

echo Dio 2: Arhiviranje zip arhive.
set "ext=.zip"
set "fname=%dir%%ext%"
echo Naziv je %fname%

echo Kopira se python...
copy D:\apps\portablepy\python.zip D:\apps\portablepy\dist
echo Uklanjanje read-only atributa
attrib -r D:\apps\portablepy\dist\python.zip

echo Azuriranje python.zip arhive...
D:\apps\7za920\7za.exe u -tzip D:\apps\portablepy\dist\python.zip D:\apps\portablepy\dist\%dir%\dtknv
D:\apps\7za920\7za.exe u -tzip D:\apps\portablepy\dist\python.zip D:\apps\portablepy\dist\%dir%\*.txt
D:\apps\7za920\7za.exe u -tzip D:\apps\portablepy\dist\python.zip D:\apps\portablepy\dist\%dir%\pokrenime.bat

echo Promjena naziva u %fname%
ren D:\apps\portablepy\dist\python.zip %fname%

echo Azuriranje zavrseno.

REM echo Dio 3: Brisanje foldera D:\apps\portablepy\dist\%dir%\dtknv
REM rd /S D:\apps\portablepy\dist\%dir%\dtknv


echo Kraj skripte.
pause