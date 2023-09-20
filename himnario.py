import tkinter as tk
from tkinter import ttk
import json

from player import *        

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.config = {
            "path": {
                "letras": "Assets/BetterLetras2K",
                "infohimnos": "Assets/infohimnos.json"
            },
        }

        self.title("Himnario Adventista")
        self.geometry("500x700")
        self.minsize(500,700)
        self.grid_columnconfigure((0,1), weight=1)

        self.get_listahimnos()

        self.button = ttk.Button(self, text="start player", command=self.start_player)
        self.button.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.setup_numberentry()

        self.playing = False
        self.player = None

    def setup_numberentry(self):
        self.numberentry = ttk.Entry(self)
        self.numberentry.grid(row=3, column=0, padx=20, sticky="nw", columnspan=1)

    def get_listahimnos(self):
        datafile = self.config["path"]["infohimnos"]
        fhandler = open(datafile, "r", encoding="utf-8")
        infohimnos = json.load(fhandler)
        self.himnos = {}
        for info in infohimnos:
            id = f"{info['numero']} - {info['titulo']}"
            self.himnos[id] = info

    
    def start_player(self):
        if self.player is None or not self.player.winfo_exists():
            self.player = Player(self.config, "SOLO LETRA", {
                "titulo": "Fue un milagro",
                "numero": "72",
                "ruta": "072 - Fue un milagro",
                "tiempos": "00:00:00|00:08:00|00:27:00|00:45:00|01:05:00|01:24:00|01:42:00|02:01:00|02:21:00|02:39:00"
            })