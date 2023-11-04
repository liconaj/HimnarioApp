import _tkinter

import sys

import tkinter as tk
from tkinter import ttk

import Source.Settings as Settings
import Source.Finder as Finder


class App(tk.Tk):
    def __init__(self, data_path: str):
        super().__init__()
        Settings.make_dpi_aware()
        width, height = 800, 700
        self.title("Program Adventista")
        self.geometry(f"{width}x{height}")
        self.minsize(width, height)
        try:
            self.iconbitmap(default=f"{data_path}/icon.ico")
        except _tkinter.TclError:
            print("Archivo icon.ico faltante", file=sys.stderr)
        self.protocol("WM_DELETE_WINDOW", self._exit)
        self.settings = Settings.Settings(self, data_path)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.finder = Finder.Finder(self.settings)
        self.finder.pack(fill="both", expand=True)
        self.settingsui = Settings.SettingsUI(self, self.settings)
        self.notebook.add(self.finder, text="Buscar")
        self.notebook.add(self.settingsui, text="Ajustes")

    def _exit(self) -> None:
        self.settings.save()
        self.quit()
