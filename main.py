import tkinter as tk
from tkinter import ttk


import settings
from finder import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        WIDTH=700
        HEIGHT=700
        self.title("Himnario Adventista")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.minsize(WIDTH, HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self._exit)

        self.settings = settings.Settings()
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.finder = Finder(self.settings)
        self.finder.pack(fill="both", expand=True)
        self.notebook.add(self.finder, text="Inicio")
    
    def _exit(self):
        self.settings.save()
        self.quit()

if __name__ == "__main__":
    app = App()
    app.mainloop()