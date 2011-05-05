@echo off
echo ----------------------------------------------------------------
echo Dist skripta za dtknv, v. 1.0
echo ----------------------------------------------------------------

set /p dir=Ime za novi folder? 

echo Dio 1: Arhiviranje izvornog koda.

echo Pravi se folder %dir%... 
md D:\apps\portablepy\dist\%dir%

echo Pravi se src folder...
md D:\apps\portablepy\dist\%dir%\src

echo Brisanje setup.py datoteke
del D:\code\dtknv\src\setup.py

echo Kopiranje py datoteka...
copy D:\code\dtknv\src\*.py D:\apps\portablepy\dist\%dir%\src

echo Kopiranje txt datoteka...
copy D:\code\dtknv\inst\*.txt D:\apps\portablepy\dist\%dir%

echo Kopiranje pokrenime.bat datoteke...
copy D:\code\dtknv\inst\pokrenime.bat D:\apps\portablepy\dist\%dir%

echo Zipovanje...
D:\apps\7za920\7za.exe a -tzip D:\apps\portablepy\dist\%dir%c.zip D:\apps\portablepy\dist\%dir%\src\
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
D:\apps\7za920\7za.exe u -tzip D:\apps\portablepy\dist\python.zip D:\apps\portablepy\dist\%dir%\src\
D:\apps\7za920\7za.exe u -tzip D:\apps\portablepy\dist\python.zip D:\apps\portablepy\dist\%dir%\*.txt
D:\apps\7za920\7za.exe u -tzip D:\apps\portablepy\dist\python.zip D:\apps\portablepy\dist\%dir%\pokrenime.bat

echo Promjena naziva u %fname%
ren D:\apps\portablepy\dist\python.zip %fname%

echo Azuriranje zavrseno.

echo Dio 3: Brisanje foldera D:\apps\portablepy\dist\%dir%
rd /S D:\apps\portablepy\dist\%dir%


echo Kraj skripte.
pause