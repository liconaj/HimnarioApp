import _tkinter
import sys

import tkinter as tk
from tkinter import ttk

import Settings
import Finder


class App(tk.Tk):
    def __init__(self, data_dir: str):
        super().__init__()
        Settings.make_dpi_aware()
        width, height = 800, 700
        self.title("Himnario Adventista")
        self.geometry(f"{width}x{height}")
        self.minsize(width, height)
        try:
            self.iconbitmap(default=f"{data_dir}/icon.ico")
        except _tkinter.TclError:
            print("Archivo icon.ico faltante", file=sys.stderr)
        self.protocol("WM_DELETE_WINDOW", self._exit)
        self.settings = Settings.Settings(self, data_dir)
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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        DATA_DIR = sys.argv[1]
    else:
        DATA_DIR = "Data"
    app = App(DATA_DIR)
    app.mainloop()
