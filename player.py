import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

import glob

class Player(tk.Toplevel):
    def __init__(self, config, modo, infohimno):
        super().__init__()
        self.set_infohimno(infohimno)

        self.config = config
        self.modo = modo
        self.infohimno = infohimno
        self.changed = False
        self.slideindex = 0
    
        self.width = self.winfo_width()
        self.height = self.winfo_height()

        self.killed = False

        self.get_images()
        self.set_slide()

        self.setup_window()
        self.setup_canvas()
        self.set_slide()
        self.keybindings()


    def set_infohimno(self, infohimno):
        self.titulo = infohimno['titulo']
        self.numero = infohimno['numero']
        self.ruta = infohimno['ruta']
        self.tiempos = infohimno['tiempos'].split("|")


    def setup_canvas(self):
        self.canvas = ttk.Label(self)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.bind('<Configure>', self._on_resize)
    
    def update_canvas(self):
        if self.killed:
            return
        self.canvas.config(image=self.slide)

    def setup_window(self):
        self.title(f"Himnario Adventista Player | {self.numero} - {self.titulo} | {self.modo}")
        self.geometry("800x600")
        self.minsize(800,600)
        self.configure(background="black")
        self.fullscreen = False
    
    def keybindings(self):
        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("f", self._toggle_fullscreen)
        self.bind("<Right>", self._on_next)
        self.bind("<Left>", self._on_prev)
        self.bind("<KeyRelease-Right>", self._allow_change)
        self.bind("<KeyRelease-Left>", self._allow_change)
        self.bind("<Escape>", self._exit)
        
    def change_slide(self, dir=""):
        oldindex = self.slideindex
        if dir=="prev" and self.slideindex>0:
            self.slideindex -= 1
        elif dir=="next" and self.slideindex<len(self.images)-1:
            self.slideindex += 1
        if self.slideindex != oldindex:            
            self.transalpha = 0.0
            self.image1 = self.image.copy()
            self.image2 = self.images[self.slideindex]
            self.transition()
            self.set_slide()
    
    def transition(self):
        if self.transalpha < 1.0:
            self.image = Image.blend(self.image1, self.image2, self.transalpha)
            self.transalpha += 0.334
            self.set_slide()
            self.update_canvas()
            self.after(1, self.transition)
        else:
            self.image = self.image2
            self.set_slide()
            self.update_canvas()
            self.transalpha = 0
    
    def set_slide(self):
        image = self.image.resize((self.width, self.height))
        self.slide = ImageTk.PhotoImage(image)

    def get_images(self):
        imgfolder = f"{self.config['path']['letras']}/{self.ruta}"
        imgfiles = [fn for fn in glob.glob(f"{imgfolder}/*")]
        self.images = [Image.open(img) for img in imgfiles]
        self.image1 = None
        self.image2 = None
        self.transalpha = 0
        self.image = self.images[0]
    
    def _on_resize(self, event=None):
        self.width = event.width
        self.height = event.height
        self.set_slide()
        self.update_canvas()
    
    def _on_next(self, _=None):
        if self.transalpha != 0:
            self.after(1, self._on_next)
            return
        if self.changed: return
        self.changed = True
        self.change_slide("next")
        self.update_canvas()
    
    def _on_prev(self, _=None):
        if self.transalpha != 0:
            self.after(1, self._on_prev)
            return
        if self.changed: return
        self.changed = True
        self.change_slide("prev")
        self.update_canvas()
    
    def _allow_change(self, _=None):
        self.changed = False
    
    def _toggle_fullscreen(self, _=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
    
    def _exit(self, _=None):
        self.killed = True
        self.destroy()
        self.update()
