import tkinter as tk
from tkinter import ttk
import json

from player import *

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        WIDTH=600
        HEIGHT=700
        self.config = {
            "path": {
                "letras": "Assets/Letras",
                "infohimnos": "Assets/infohimnos.json"
            },
        }

        self.title("Himnario Adventista")

        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.minsize(WIDTH, HEIGHT)
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)

        self.get_listahimnos()
        self.setup_search()

        self.playing = False
        self.player = None

        self.bind("<Button-1>", self._takeout_focus)

    def setup_search(self):
        self.playmode = None
        self.playmode_selector = ttk.Notebook(self)        
        self.playmode_selector.grid(row=0, column=1, padx=20, pady=10)
        self.playmode_tabs = {}
        self.playmode_tabs["Solo letra"] = SearchFrame(self.playmode_selector)
        self.playmode_tabs["Cantado"] = SearchFrame(self.playmode_selector)
        self.playmode_tabs["Instrumental"] = SearchFrame(self.playmode_selector)
        for k, v in self.playmode_tabs.items():
            self.playmode_selector.add(v, text=k)        
        self.playmode_selector.bind("<<NotebookTabChanged>>", self._on_change_playmode)

        self.search = SearchEntries(self.playmode_selector, self.titulos, self.numeros)
        self.search.bind("<Return>", self._start_player)

    def get_listahimnos(self):
        datafile = self.config["path"]["infohimnos"]
        fhandler = open(datafile, "r", encoding="utf-8")
        infohimnos = json.load(fhandler)
        self.titulos = {}
        self.numeros = {}
        for info in infohimnos:
            self.numeros[int(info["numero"])] = info
            self.titulos[info["titulo"]] = info

    
    def _start_player(self, _=None):
        number = self.search.getnumber()
        if number is None:
            return
        if self.player is not None and self.player.winfo_exists():
            self.player._exit()
        if self.player is None or not self.player.winfo_exists():
            infohimno = self.numeros[number]
            modo = self.playmode.upper()
            self.player = Player(self.config, modo, infohimno)
    
    def _on_change_playmode(self, _=None):
        id = self.playmode_selector.select()
        name = self.playmode_selector.tab(id, "text")
        self.playmode = name
        self.search.place_entries(self.playmode_tabs[name])
    
    def _takeout_focus(self, event=None):
        if event.widget == self:
            self.focus()
    


class SearchFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.columnconfigure((0,1), weight=1)

class SearchEntries():
    def __init__(self, master, titulos, numeros):
        self.master = master
        self.titulos = titulos
        self.numeros = numeros
        self.setup_numberentry()
        self.setup_titleentry()
        self.selected_number = None
        self.selected_title = None

    def place_entries(self, root):
        self.numberentry.grid(
            row=0, column=0,
            padx=(20,5), pady=20,
            sticky="ew", in_=root)
        self.titleentry.grid(
            row=0, column=1,
            padx=(5,20), pady=20,
            sticky="ew", in_=root)

    def setup_numberentry(self):
        self.numbertext = tk.StringVar()
        self.numberentry = PlaceholderEntry(self.master, "#")
        self.numberentry.config(justify="center", width=10,
            font="Arial 16 bold",
            textvariable=self.numbertext)
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
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

    def _clear_placeholder(self, _=None):
        self.delete("0", "end")

    def _add_placeholder(self, _=None):
        if not self.get():
            self.insert("0", self.placeholder)