import tkinter as tk
from tkinter import ttk
import json

from player import *
from music import *

class Finder(ttk.Frame):
    def __init__(self, settings) -> None:
        super().__init__()
        self.settings = settings

        self.mixer = Music()
        self.playing = False
        self.player = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.get_listahimnos()
        self.setup_modeselector()
        self.setup_search()

        self.bind("<Button-1>", self._takeout_focus)
    
    def setup_modeselector(self):
        self.modeselector = PlayModeSelector(self)
        self.modeselector.config(width=50)
        self.modeselector.grid(row=0, column=0, padx=20, pady=20)


    def setup_search(self):
        self.searchframe = ttk.Frame(self, style="Card.TFrame", width=50)
        self.searchframe.grid(row=1, column=0, padx=20, ipady=0)
        self.searchframe.columnconfigure(2, weight=1)
        self.searchframe.rowconfigure(0, weight=1)

        self.search = SearchEntries(self.searchframe, self.titulos, self.numeros)
        self.search.bind("<Return>", self._start_player)

    def get_listahimnos(self):
        datafile = self.settings.get_indexes_path()
        fhandler = open(datafile, "r", encoding="utf-8")
        infohimnos = json.load(fhandler)
        self.titulos = {}
        self.numeros = {}
        for info in infohimnos["lista"]:
            self.numeros[int(info["numero"])] = info
            self.titulos[info["titulo"]] = info
        self.temas = infohimnos["temas"]
        for tema in self.temas:
            nombretema = tema["nombre"]
            if tema["hassubs"]:
                for sub in tema["subtemas"]:
                    nombresub = f'{nombretema} - {sub["nombre"]}'
                    rango = sub["rango"]
                    for numero in range(rango[0], rango[1]+1):
                        self.numeros[numero]["tema"] = nombresub
            else:
                rango = tema["rango"]
                for numero in range(rango[0], rango[1]+1):
                    self.numeros[numero]["tema"] = nombretema

    
    def _start_player(self, _=None):
        number = self.search.getnumber()
        infohimno = self.numeros[number]
        modo = self.modeselector.getmode()
        if number is None:
            return
        if self.player is not None and self.player.winfo_exists():
            self.player.new_song(modo, infohimno)
        else:
            self.player = Player(self.settings, modo, infohimno, self.mixer)
    
    def _on_change_playmode(self, _=None):
        id = self.searchframe.select()
        name = self.searchframe.tab(id, "text")
        self.playmode = name
        self.search.place_entries(self.playmode_tabs[name])
    
    def _takeout_focus(self, event=None):
        if event.widget == self:
            self.focus()
    
class PlayModeSelector(ttk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.columnconfigure(3, weight=1)
        self.mode = tk.IntVar(value=1)
        self.modes = ["Solo letra", "Cantado", "Instrumental"]
        self.addmode(0)
        self.addmode(1)
        self.addmode(2)
    
    def addmode(self, value):
        text = self.modes[value]
        button = ttk.Radiobutton(self,
            text=text,
            variable=self.mode,
            value=value,
            style="Toggle.TButton",
            width=12)
        button.grid(row=0, column=value, padx=5, pady=5)
        #self.modes[text] = button
    
    def getmode(self):
        return self.modes[self.mode.get()]

class SearchFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.columnconfigure((0,1), weight=1)

class SearchEntries():
    def __init__(self, root, titulos, numeros):
        self.master = root
        self.titulos = titulos
        self.numeros = numeros
        self.setup_numberentry()
        self.setup_titleentry()
        self.selected_number = None
        self.selected_title = None    
        

    def setup_numberentry(self):
        self.numbertext = tk.StringVar()
        self.numberentry = PlaceholderEntry(self.master, "#")
        self.numberentry.config(justify="center", width=8,
            font="Arial 16 bold",
            textvariable=self.numbertext)
        self.numberentry.grid(
            row=0, column=0,
            padx=(20,5), pady=20,
            sticky="ew")
        self.numbertext.trace("w", lambda *args: self._validate_number())
    
    def bind(self, sequence, func):
        self.numberentry.bind(sequence, func)
        self.titleentry.bind(sequence, func)
    
    def getnumber(self):
        return self.selected_number
    
    def setup_titleentry(self):
        self.titletext = tk.StringVar()
        self.titleentry = PlaceholderEntry(self.master, "Título del himno")
        self.titleentry.config(justify="center", width=40,
            font="Arial 16 bold",
            textvariable=self.titletext)        
        self.titleentry.grid(
            row=0, column=1,
            padx=(5,20), pady=20,
            sticky="ew",
            columnspan=2)
        self.titletext.trace("w", lambda *args: self._validate_title())
    
    def _validate_number(self):
        number = self.numbertext.get()

        if number == "#":
            return

        maxdigits = 3
        maxnumber = 614

        if not number.isdigit():
            self.numbertext.set(number[:-1])
        elif len(number) > maxdigits:
            self.numbertext.set(number[:maxdigits])
        elif len(number)>0 and int(number) > maxnumber:
            self.master.after(100, lambda *args: self.numbertext.set(maxnumber))
        
        if not number:
            #self.titletext.set("")
            self.selected_number = None
        elif number.isdigit() and int(number) in range(1,maxnumber+1):
            titulo = self.numeros[int(number)]["titulo"]
            self.titletext.set(titulo)
            self.selected_number = int(number)

    def _validate_title(self):
        allowedchars = "abcdefghijklmnñopqrstuvwxyáéíóúü"
        allowedchars += allowedchars.upper()
        allowedchars += " ,¡!¿?"
        titulo = self.titletext.get()
        if (len(titulo) > 0 and not titulo[-1] in allowedchars):
            self.titletext.set(titulo[:-1])

class PlaceholderEntry(ttk.Entry):
    def __init__(self, container, placeholder, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.placeholder = placeholder
        self.insert("0", self.placeholder)
        #self.bind("<FocusIn>", self._clear_placeholder)
        #self.bind("<FocusOut>", self._add_placeholder)

    def _clear_placeholder(self, _=None):
        self.delete("0", "end")

    def _add_placeholder(self, _=None):
        if not self.get():
            self.insert("0", self.placeholder)