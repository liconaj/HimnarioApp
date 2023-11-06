import _tkinter
import json

import sys

import tkinter as tk
from tkinter import ttk

import Source.Settings as Settings
import Source.Finder as Finder
import Source.Indexes as Indexes


class Himnario(tk.Tk):
    def __init__(self, data_path: str):
        super().__init__()
        Settings.make_dpi_aware()
        width, height = 1080, 700
        self.title("Program Adventista")
        self.geometry(f"{width}x{height}")
        self.minsize(width, height)
        try:
            self.iconbitmap(default=f"{data_path}/icon.ico")
        except _tkinter.TclError:
            print("Archivo icon.ico faltante", file=sys.stderr)
        self.protocol("WM_DELETE_WINDOW", self._exit)
        self.settings = Settings.Settings(self, data_path)
        self.indices = self.get_infohimnos()
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        self.setup_finder()
        self.setup_indexes()
        self.setup_settingsui()

    def setup_finder(self):
        self.finder = Finder.Finder(self.settings, self.indices)
        self.notebook.add(self.finder, text="Buscar")

    def setup_settingsui(self):
        self.settingsui = Settings.SettingsUI(self.settings)
        self.notebook.add(self.settingsui, text="Ajustes")

    def setup_indexes(self):
        self.indexes = Indexes.Indexes(self.indices)
        self.notebook.add(self.indexes, text="Indices")

    def _exit(self) -> None:
        self.settings.save()
        self.quit()

    def get_infohimnos(self) -> dict:
        datafile = self.settings.get_indexes_path()
        fhandler = open(datafile, "r", encoding="utf-8")
        indices = json.load(fhandler)
        indices["numeros"] = dict()
        indices["titulos"] = dict()
        indices["palabras"] = dict()
        for info in indices["lista"]:
            indices["numeros"][int(info["numero"])] = info
            indices["titulos"][info["titulo"]] = info
            palabras = info.get("palabras", None)
            if palabras is not None:
                indices["palabras"][palabras] = info
        for tema in indices["temas"]:
            nombretema = tema["nombre"]
            if tema["hassubs"]:
                for sub in tema["subtemas"]:
                    nombresub = f'{nombretema} - {sub["nombre"]}'
                    rango = sub["rango"]
                    for numero in range(rango[0], rango[1] + 1):
                        indices["numeros"][numero]["tema"] = nombresub
            else:
                rango = tema["rango"]
                for numero in range(rango[0], rango[1] + 1):
                    indices["numeros"][numero]["tema"] = nombretema
        return indices
