#! /usr/bin/python3
"""

This is a GUI wrapper for tocyr.

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

import threading
import webbrowser
import time
import os

import tkinter as tk
from tkinter import W, E, S, N
from tkinter import filedialog
from tkinter import messagebox
from functools import partial

from convert import tocyr
from convert.tocyr import ToCyr
from srpismo.cyrconv import CirConv

import version

__version__ = '0.3.1'
__url__ = "https://gitorious.org/dtknv"
__author__ = "Romeo Mlinar"
__license__ = "GNU General Public License v. 3"

class TocyrGui(tk.Frame):

    def __init__(self, master=None):
        self.settings = {}
        self.settings['pathin'] = None
        self.settings['pathout'] = None
        self.settings['conversiontype'] = None
        # The limits for the warnings:
        self.settings['warn_filesnumber'] = 1000
        self.settings['warn_filesize'] = 100
        self.tocyrclass = ToCyr()
        # For tracking file number and size
        self.filecalc = {}
        self.filecalc['path'] = 0
        self.filecalc['filecount'] = 0
        self.filecalc['filesize'] = 0
        # Initialise Tk stuff
        tk.Frame.__init__(self, master)
        self.grid()
        #Title
        self.master.title("DT Konvertor pisama")
        # Draw the widgets and update them
        self.create_widgets()
        self.updatestates()
        #Script conversion class
        self.tolatin = CirConv(mode='tolat')
        self.tocyrillic = CirConv(mode='tocyr')
        # Global binds
        self.bind_class('Text', '<Control-a>', self.ctext_selectall)


    def create_widgets(self):
        """Create GUI for the main window."""
        self.draw_dirsfiles2()

    def draw_dirsfiles2(self):
        """
        Draw a pane for files/directories conversion.
        It consists of 3 frames, fra_filesdir fra_filesdirifo,
        and fra_buttons:
        |----------------------------------------------------------|
        |fra_mainfilesdir               | fra_filesdir info        |
        |                               |
        ||--------------------------|   |
        ||fra_filesdir              |   |
        ||                          |   |
        |||-----------------------| |   |
        |||fra_buttons            | |   |
        |||-----------------------| |   |
        ||--------------------------|   |                          |
        |-------------------------info label-----------------------|

        """
        # The main frame for this mode of work
        fra_mainfilesdirs = tk.Frame(self)
        # -------------------------------------------------
        # GUI for files and directories operations
        # -------------------------------------------------
        # All frames in this window:
        fra_filesdirs = tk.Frame(fra_mainfilesdirs, padx=5, pady=5)
        fra_buttons = tk.Frame(fra_filesdirs)
        fra_filesdirsinfo = tk.Frame(fra_mainfilesdirs, padx=5)
        # -------------------------------------------------
        # GUI for files and directories operations
        # fra_filesdir & fra_buttons
        # -------------------------------------------------
        # Path entry in 0, 0
        self.txt_dirin = tk.Entry(fra_filesdirs, width=30)
        self.txt_dirin.grid(column=0, row=0)
        # Browse button in 1, 0
        self.btn_browsedir = tk.Button(fra_filesdirs, width=9)
        self.btn_browsedir.grid(column=1, row=0)
        self.btn_browsedir["text"] = "Fascikla..."
        self.btn_browsedir["command"] = command=partial(self.browse,
                                                     what = "dir")
        # Path entry in 0, 1
        self.txt_filein = tk.Entry(fra_filesdirs, width=30)
        self.txt_filein.grid(column=0, row=1)
        # Browse button in 1, 1
        self.btn_browsefile = tk.Button(fra_filesdirs, width=9)
        self.btn_browsefile.grid(column=1, row=1)
        self.btn_browsefile["text"] = "Datoteka..."
        self.btn_browsefile["command"] = command=partial(self.browse,
                                                     what = "files")
        # Path entry in 0, 2
        self.txt_dirout = tk.Entry(fra_filesdirs, width=30)
        self.txt_dirout.grid(column=0, row=2)
        # Browse button in 1, 2
        self.btn_browseoutdir = tk.Button(fra_filesdirs, width=9)
        self.btn_browseoutdir.grid(column=1, row=2)
        self.btn_browseoutdir["text"] = "Izlaz..."
        self.btn_browseoutdir["command"] = command=partial(self.browse,
                                                     what = "outdir")

        # Checkbutton recursive 0,3
        self.chk_recursive = tk.Checkbutton(fra_filesdirs)
        self.chk_recursive["text"] = "Rekurzivna konverzija"
        self.recursive = tk.IntVar()
        self.chk_recursive["variable"] = self.recursive
        self.recursive.set(0)
        self.chk_recursive["state"] = 'disabled'
        self.chk_recursive["command"] = self.updatestates
        self.chk_recursive.grid(column=0, row=3, sticky='w')
        # Checkbutton filenames 0,4
        self.chk_fnames = tk.Checkbutton(fra_filesdirs)
        self.chk_fnames["text"] = "Konvertuj imena datoteka."
        self.fnames = tk.IntVar()
        self.chk_fnames["variable"] = self.fnames
        self.chk_fnames.grid(column=0, row=4, sticky='w')
        self.chk_fnames["command"] = self.updatestates
        #Button for text conversion
        self.btn_text = tk.Button(fra_filesdirs)
        self.btn_text['text'] = 'Konverzija teksta...'
        self.btn_text['command'] = self.show_textconv
        self.btn_text.grid(column=0, row=5, sticky='we')      
        # Buttonz!
        # Run
        self.btn_run = tk.Button(fra_buttons, width=8)
        self.btn_run["text"] = "Konvertuj"
        self.btn_run["command"] =  self.run
        self.btn_run.grid(column=0, row=0, padx=2)
        # Quit
        self.QUIT = tk.Button(fra_buttons, width=8)
        self.QUIT["text"] = "Zatvori"
        self.QUIT["command"] =  self.quit
        self.QUIT.grid(column=1, row=0, padx=2)
        # About
        self.btn_about = tk.Button(fra_buttons, width=8)
        self.btn_about.grid(column=2, row=0, padx=2)
        self.btn_about["text"] = "Info"
        self.btn_about["command"] = command=partial(self.about)
        # -------------------------------------------------
        # GUI for info stuff
        # fra_filesdirinfo
        # -------------------------------------------------
        self.lbl_dirsfilesinfo = tk.Label(fra_filesdirsinfo, justify='left',
                                         relief='groove', anchor='w',
                                         wraplength=400)
        self.lbl_dirsfilesinfo['text'] = 'Informacije o radu programa'
        self.lbl_dirsfilesinfo.grid(column=0, row=0, columnspan=2)
        # HTTP links
        # Label help 5,0
        self.lbl_help = tk.Label(fra_filesdirsinfo, relief='groove')
        self.lbl_help["text"] = "Pomoć (onlajn)"
        self.lbl_help["fg"] = "blue"
        self.lbl_help["cursor"] = "hand1"
        self.lbl_help["font"] = 'helvetica', 8, 'underline italic'
        self.lbl_help.bind("<Button-1>", self.openbrowser_help)
        self.lbl_help.grid(column=0, row=1, sticky='wesn')
        # Label Visit website 6,1
        self.lbl_site = tk.Label(fra_filesdirsinfo, relief='groove')
        self.lbl_site["text"] = "Prijavite grešku!"
        self.lbl_site["fg"] = "blue"
        self.lbl_site["cursor"] = "hand1"
        self.lbl_site["font"] = 'console', 8, 'underline italic'
        self.lbl_site.bind("<Button-1>", self.show_mail)
        self.lbl_site.grid(column=1, row=1, sticky='wesn')
        # -------------------------------------------------
        # GUI for labels on the bottom of the main frame
        # -------------------------------------------------
        self.lbl_info = tk.Label(fra_mainfilesdirs)
        self.lbl_info["bg"] = "white"
        self.lbl_info["text"] = "Odaberite folder ili datoteku."
        self.lbl_info.grid(column=0, row=2, columnspan=2, sticky=W+E+S+N)
        # Pack the frames
        fra_filesdirs.grid(column=0, row=0)
        fra_buttons.grid(column=0, row=6, pady=5)
        fra_filesdirsinfo.grid(column=1, row=0, rowspan=2)
        fra_mainfilesdirs.grid()
        # Make them publically available
        self.fra_mainfilesdirs = fra_mainfilesdirs
    
    def draw_textentry(self):
        """Draw widgets for simple text conversion
        |-------------------------------------|
        |fra_textconv                         |
        |                                     |
        ||-----------------------------------||
        || fra_buttons2                      ||
        ||-----------------------------------||
        |-------------------------------------|
        """
        fra_textconv = tk.Frame(self)
        # Scroll bar
        scroll_txt=tk.Scrollbar(fra_textconv)
        # Text widget
        txt_text = tk.Text(fra_textconv, height=10, width=50,
                    yscrollcommand=scroll_txt.set, wrap='word')
        txt_text.grid(sticky='snew')
        # The binds for thw text widget
        #txt_text.bind('<Control-a>', self.ctext_selectall)
        scroll_txt.config(command=txt_text.yview)
        scroll_txt.grid(column=1, row=0, sticky='NESW')
        # Buttons
        # Frame:
        fra_buttons2 = tk.Frame(fra_textconv)
        # 1
        btn_converttext_2lat = tk.Button(fra_buttons2)
        btn_converttext_2lat['text'] = 'Konvertuj (ćir. > lat.)'
        btn_converttext_2lat['command'] = command=partial(self.dotext,
                                                     act = 'tolat')
        btn_converttext_2lat.grid(column=0, row=0, padx=2, pady=2)
        # 2
        btn_converttext_2cyr = tk.Button(fra_buttons2)
        btn_converttext_2cyr['text'] = 'Konvertuj (lat. > ćir.)'
        btn_converttext_2cyr['command'] = command=partial(self.dotext,
                                                     act = 'tocyr')
        btn_converttext_2cyr.grid(column=1, row=0, padx=2, pady=2)
        # 3
        btn_showfilesdirs = tk.Button(fra_buttons2)
        btn_showfilesdirs['text'] = 'Konvertuj datoteke...'
        btn_showfilesdirs['command'] = self.show_filesdirs
        btn_showfilesdirs.grid(column=0, row=2, columnspan=2, padx=2, pady=2, sticky='EW')
        
        # Pack frames
        fra_buttons2.grid(column=0, row=1)
        fra_textconv.grid(sticky='snew')
        # make stuff public
        self.txt_text = txt_text
        self.fra_textconv = fra_textconv
        
    def ctext_selectall(self, callback):
        """Select all text in the text widget"""
        self.txt_text.tag_add('sel', '1.0', 'end')
        
    
    def show_textconv(self):
        """Hide frame for files/dirs and show entry widget"""
        self.fra_mainfilesdirs.grid_remove()
        self.draw_textentry()
    
    def show_filesdirs(self):
        """Hide frame for text and show files/dirs"""
        self.fra_textconv.grid_remove()
        self.draw_dirsfiles2()
        self.updatestates()

    def browse(self, what):
        """
        Browse for a file/folder.
        
        The checks for a system type is because tkinter returns
        different types of values in the dialogues on nt/posix.
        
        """
        in_path = ""
        if what == "files":
            in_path = filedialog.askopenfilenames(multiple=False,
                      filetypes = self.filedesc())
            self.settings['conversiontype'] = 'files'
            self.chk_recursive["state"] = 'disabled'
            if os.name == 'nt':
                in_path = in_path.replace('{', '')
                in_path = in_path.replace('}', '')
                if in_path.strip() != '':
                    self.settings['pathin'] = in_path.strip()
            else:
                if len(in_path) != 0:
                    self.settings['pathin'] = in_path[0]

        elif what == "dir":
            in_path = filedialog.askdirectory()
            if os.name == 'nt':
                if in_path.strip() != '':
                    self.settings['pathin'] = in_path.strip()
            else:
                if len(in_path) != 0:
                    self.settings['pathin'] = in_path
            self.settings['conversiontype'] = 'dir'
            self.chk_recursive["state"] = 'active'
        elif what == "outdir":
            in_path = filedialog.askdirectory()
            self.settings['pathout'] = in_path

        self.updatestates()


    def filedesc(self):
        """File extensions for a dialogue."""
        t = []
        e = self.tocyrclass.EXT
        t.append(('Sve datoteke', '.*'))
        for i in e.keys():
            t.append((e[i], '*.%s' % i))
        return t

    def show_mail(self, event):
        """Open a window showing the email address."""
        text = 'Greške u radu programa ili predloge pošaljite na \n' + \
            'cheesepy@gmail.com \n\n Hvala! :)'
        messagebox.showinfo("Kontakt", text) 
        

    def openbrowser_help(self, event):
        "go to the website"
        browse = webbrowser.get()
        browse.open(r'http://digitalnitrg.blogspot.com/2011/03/' + \
                        'dt-konvertor-datoteka-iz-cirilice-u.html#uputstvo_gui')

    def about(self):
        """About dialog"""
        text =  "DT Konvertor pisama (dtknv)" + \
                "\n\nRazvojna verzija %s, jul 2011." % version.__version__ + \
                "\nVerzija konvertora: %s" % tocyr.__version__ + \
                "\nVerzija sučelja: %s" % __version__ + \
                "\nOS: %s" % os.name + \
                "\n\nNove verzije dostupne su na www.languagebits.com/dtknv/"
        messagebox.showinfo("O programu", text)
    
    def dotext(self, act='del'):
        """Misc operations for main text entry / conversion"""
        if (act == 'tocyr') or (act =='tolat'):
            text = self.txt_text.get(1.0, 'end')
            try:
            # convert text to Latin
                converted_text = self.get_converedtext(text, act)
            # delete text in text widget
                self.txt_text.delete(1.0, 'end')
            # insert converted text
                self.txt_text.insert(1.0, converted_text)
            except:
                print('Konverzija nije uspjela!')
    
    def get_converedtext(self, text, mode):
        """Return converted text"""
        if mode == 'tolat':
            self.tolatin.text = text
            return self.tolatin.get_converted()
        elif mode == 'tocyr':
            self.tocyrillic.text = text
            return self.tocyrillic.get_converted()
        else:
            raise ValueError('Mode can be only tolat or tocyr.')
    
    def get_abouttext(self):
        """Return text about the current setup"""
        # Recursive message
        dirin = self.settings['pathin']
        if self.settings['conversiontype'] == 'files':
            rec = '(nije moguća za konverziju datoteka)'
        elif self.settings['conversiontype'] == 'dir':
            if (self.filecalc['path'] != dirin) and self.recursive.get():
                # This here takes a long to calculate
                self.lbl_dirsfilesinfo['text'] = 'Trenutak, ' + \
                    'računanje u toku... Ako ste odabrali fasciklu\n' + \
                    'sa mnogo datoteka, računanje može potrajati.'
                self.lbl_dirsfilesinfo.update()
                self.filecalc['filecount'], self.filecalc['filesize'] = \
                    self.tocyrclass.calculatedirsize(dirin)
                self.filecalc['path'] = dirin
            if self.recursive.get():
                if self.settings['pathin'] == None:
                    rec = "uključena, odaberite ulaznu fasciklu za proračun."
                else:
                    size = '%0.2f' % self.filecalc['filesize']
                    rec = "uključena, prepoznatih datoteka: %s (%s MB)." \
                    % (self.filecalc['filecount'], size)
            else:
                rec = "isključena."
        else:
            rec = "isključena / nije podržana."

        if (self.settings['pathin'] or self.settings['pathin']) in (False, None):
            convertpath = 'nije odabrano.'
        else:
            convertpath = (self.settings['pathin'] or self.settings['pathin'])

        if not self.settings['pathout']:
            pathout = 'nije odabrano.'
        else:
            pathout = self.settings['pathout']

        #Name conversion
        if self.fnames.get():
            fnames = 'uključena'
        else:
            fnames = 'isključena'

        text =  "-Ulazna fascikla/datoteka: %s" % convertpath + \
                "\n-Izlazna fascikla: %s" % pathout + \
                "\n-Konverzija ćiriličnih naziva datoteka u lat: %s." \
                                                            % fnames + \
                "\n-Kodna stranica: %s." % self.tocyrclass.ENC + \
                "\n-Sve prepoznate ekstenzije: %s." % \
                                ', '.join(self.tocyrclass.EXT.keys()) + \
                "\n-Prepoznate tekstualne ekstenzije: %s." % \
                                ', '.join(self.tocyrclass.TEXTFILES) + \
                "\n-Rekurzivna konverzija: %s" % rec
        
        return text

    def runchecks(self):
        """Misc. checks"""
        #   In case the file number is too high:
        selected = self.filecalc['filecount']
        maxn = self.settings['warn_filesnumber']
        if  (selected > maxn) and (self.settings['conversiontype'] == 'dir'):
            ask = messagebox.askyesno(
                'Upozorenje: Veliki broj datoteka',
                'Broj datoteka za konverziju (%s) premašuje\n' % selected + \
                'gornju granicu za upozorenje df %s datoteka. \n\n Želite li '\
                % maxn + 'pokrenuti konverziju?')
            return ask

        # The size of the selected item(s)
        if self.settings['conversiontype'] == 'dir':
            # The whole dir
            selected = self.filecalc['filesize']
        else:
            # Just one file
            size = os.path.getsize(self.txt_filein.get())
            selected = (size/(1024*1024.0))
        maxsize = self.settings['warn_filesize']
        if  (selected > maxsize):
            ask = messagebox.askyesno(
            'Upozorenje: Veliki broj megabajta',
            'Broj megabajta za konverziju (%s MB) premašuje\n' \
            % ('%0.2f' % selected) + 'gornju granicu za upozorenje ' + \
            'od %s MB. ' % maxn  + '\n\n Želite li pokrenuti konverziju?')
            return ask
        
        # Same in/out file
        if self.settings['pathin'] == self.settings['pathout']:
            ask = messagebox.askyesno(
            'Upozorenje: Iste faskile',
            'Ulazna i izlazna fascikla se ne razlikuju. ' + \
            '\n\nŽelite li nastaviti sa konverzijom?')
            return ask

        return True


    def run(self):
        """Call the topyr.py and do the conversion."""
        if not self.runchecks():
            return 0
        self.lbl_info["text"] = "Konverzija..."
        self.lbl_info["bg"] = "yellow"
        # Disable run button
        self.btn_run["state"] =  "disabled"
        self.settings['running'] = True
        # Settings:
        self.tocyrclass.PATHIN = self.settings['pathin']
        self.tocyrclass.PATHOUT = self.settings['pathout']
        self.tocyrclass.FILES = self.settings['pathin']
        #self.tocyrclass.conversiontype = self.settings['conversiontype']
        self.tocyrclass.SHOW = False
        self.tocyrclass.RECURSIVE = self.recursive.get()
        self.tocyrclass.CONVERTFNAMES = self.fnames.get()
        self.tocyrclass.SHOWPERC = True
        self.tocyrclass.CALLEDFROM = 'DTKnv, v. %s' % __version__
        self.tocyrclass.FAILSAFE = True
        # Run
        self.th = threading.Thread(target = self.tocyrclass.run)
        self.th.start()
        while True:
            self.lbl_info["text"] = "Konverzija..."
            self.lbl_info["bg"] = "yellow"
            self.lbl_info.update()
            time.sleep(1)
            self.lbl_info["text"] = "Konverzija..."
            self.lbl_info["bg"] = "red"
            self.lbl_info.update()
            time.sleep(0.3)
            if not self.th.is_alive():
                try:
                    reptext = "Provjerite datoteke i izvještaj %s." % \
                    self.tocyrclass.report.file
                except AttributeError:
                    reptext = '(Bez izvještaja.)'
                #
                if self.tocyrclass.errors_during_work:
                    reptext = 'Završeno, uz greške. ' + reptext
                    repcol = "orange"
                else:
                    reptext = 'Završeno. ' + reptext
                    repcol = "green"
                self.lbl_info["text"] = reptext
                self.lbl_info["bg"] = repcol 
                self.btn_run["state"] =  "disabled"
                break

    def updatestates(self):
        """Update states of the buttons/checkboxes"""
        notsel = ('', None, False)
        # Delete text in the three entries, and make
        # them "normal".
        for i in ('txt_dirin', 'txt_dirout', 'txt_filein'):
            getattr(self, i).configure(state = 'normal')
            getattr(self, i).delete(0, 'end')
        # Don't allow to run until all conditions are met.
        if ((self.settings['pathin'] in notsel) or \
            (self.settings['pathin'] in notsel)) and \
            (self.settings['pathout'] in notsel):
            self.btn_run["state"] =  "disabled"
        else:
            self.btn_run["state"] =  "active"
        # Entries in case of none selected
        if (self.settings['pathin'] in notsel) and \
            (self.settings['pathin'] in notsel) :
            self.txt_dirin.insert(0, '(odaberite klikom na dugme)')
            self.txt_filein.insert(0, '(odaberite klikom na dugme)')
        # Checkboxes
        if self.settings['conversiontype'] == 'files':
            self.recursive.set(0)
            self.chk_recursive["state"] = 'disabled'
        else:
            self.chk_recursive["state"] = 'normal'
        # Labels in case dir/file is selected
        if self.settings['pathin'] or self.settings['pathin']:
            # The order of inserd/disable/normal bellow
            # is important.
            if self.settings['conversiontype'] == 'files':
                self.txt_filein.configure(state = 'normal')
                self.txt_filein.insert(0, self.settings['pathin'])
                self.txt_dirin.insert(0, '(datoteka već odabrana)')
                self.txt_dirin.configure(state = 'disabled')
            if self.settings['conversiontype'] == 'dir':
                self.txt_dirin.configure(state = 'normal')
                self.txt_filein.insert(0, '(fascikla već odabrana)')
                self.txt_dirin.insert(0, self.settings['pathin'])
                self.txt_filein.configure(state = 'disabled')
                #TODO: gray out the stuff
        # Labels for outdir
        if self.settings['pathout'] in notsel:
            self.txt_dirout.insert(0, "(odaberite klikom na dugme)")
        else:
            self.txt_dirout.insert(0, self.settings['pathout'])
        # Update the infotext
        self.lbl_dirsfilesinfo['text'] = self.get_abouttext()
                
def bootgui():
    root = tk.Tk()
    root.grid_rowconfigure(0,weight=1)
    root.grid_columnconfigure(0,weight=1)
    #root.resizable(0,0)
    app = TocyrGui(master=root)
    app.mainloop()
