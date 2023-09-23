import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import screeninfo

import glob

class Player(tk.Toplevel):
    def __init__(self, settings, modo, infohimno, music=None):
        super().__init__()
        self.music = music
        self.settings = settings
        self.modo = modo
        self.changed = False
        self.slideindex = 0

        self.killed = False
        self.protocol("WM_DELETE_WINDOW", self._exit)
        
        self.set_infohimno(infohimno)
        self.setup_window()
        self.setup_canvas()
        self.keybindings()

        self.get_images()
        self.play_music()
        self.set_slide()


    def new_song(self, modo, infohimno):
        self.modo = modo
        self.changed = False
        self.slideindex = 0
        self.music.quit()
        self.set_infohimno(infohimno)
        self.get_images()
        self.play_music()
        self.set_slide()
        self.update_canvas()

    def setup_window(self):
        self.keep_aspect_ratio = self.settings["keep_aspect_ratio"]
        self.geometry(self.settings["player"]["geometry"])
        self.minsize(800,600)
        self.configure(background="black")
        self.fullscreen = self.settings["player"]["fullscreen"]
        if self.fullscreen:
            self.activate_fullscreen()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.config(cursor="none")
        self.monitors = screeninfo.get_monitors()
    

    def play_music(self):
        self.playingmusic = False
        if self.modo != "Solo letra":
            musicpath = self.settings["path"][self.modo.lower()]
            self.musicfile = f"{musicpath}/{self.ruta}.mp3"
            self.music.load(self.musicfile)
            self.music.play()
            self.playingmusic = True
            self.synchronize()
    
    def synchronize(self):
        if self.slideindex < len(self.tiempos)-1:
            nexttime = self.tiempos[self.slideindex+1]
            if self.music.get_time() > nexttime:
                self.change_slide("next")
        if self.music.has_ended():
            self.after(0, self._exit)
        self.after(10, self.synchronize)

    def set_infohimno(self, infohimno):
        self.titulo = infohimno['titulo']
        self.numero = infohimno['numero']
        self.tema = infohimno['tema']
        self.ruta = infohimno['ruta']
        self.tiempos = []
        for time in infohimno["tiempos"].split("|"):
            mm,ss,dd = (int(t) for t in time.split(":"))
            tiempoms = dd*10 + ss*1000 + mm*60*1000
            self.tiempos.append(tiempoms)
        self.title(f"Himnario Adventista Player | {self.numero} - {self.titulo} | {self.modo.upper()}")

    def setup_canvas(self):
        self.canvas = ttk.Label(self)
        self.canvas.pack(fill="both", expand=True, anchor="center")        
        self.canvas.bind('<Configure>', self._on_resize)
    
    def update_canvas(self):
        if self.killed:
            return
        self.canvas.config(image=self.slide, anchor="center")        

    def keybindings(self):
        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("f", self._toggle_fullscreen)
        self.bind("<Right>", self._on_next)
        self.bind("<Left>", self._on_prev)
        self.bind("<KeyRelease-Right>", self._allow_change)
        self.bind("<KeyRelease-Left>", self._allow_change)
        self.bind("<Escape>", self._exit)
        self.bind("<space>", self._toggle_pause)
        
    def change_slide(self, dir="", inposed=False):
        oldindex = self.slideindex
        if dir=="prev" and self.slideindex>0:
            self.slideindex -= 1
        elif dir=="next" and self.slideindex<len(self.images)-1:
            self.slideindex += 1
        if self.slideindex != oldindex:
            if inposed and self.playingmusic:
                self.music.set_time(self.tiempos[self.slideindex])
            if self.keep_aspect_ratio:
                if self.slideindex == 0:
                    self.bgimg = self.bgimg1
                else:
                    self.bgimg = self.bgimg2
            self.transalpha = 0.0
            self.image1 = self.image.copy()
            self.image2 = self.images[self.slideindex]
            self.transition()
            #self.image = self.images[self.slideindex]
            #self.set_slide()
            #self.update_canvas()
    
    def transition(self):
        if self.killed:
            return
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
        nwidth = self.width
        nheight = self.height
        if self.keep_aspect_ratio:
            if nwidth > nheight * 4/3:
                nwidth = int(nheight * 4/3)
            else:
                nheight = int(nwidth * 3/4)
        if nwidth==0 or nheight==0:
            return
        if self.keep_aspect_ratio:
            bgimg = self.bgimg.resize((self.width, self.height))
            image = self.image.resize((nwidth, nheight))
            x = int((self.width - nwidth)/2)
            y = int((self.height - nheight)/2)
            bgimg.paste(image, (x,y))
            self.slide = ImageTk.PhotoImage(bgimg)
        else:
            image = self.image.resize((nwidth, nheight))
            self.slide = ImageTk.PhotoImage(image)

    def get_images(self):
        imgfolder = f"{self.settings['path']['letras']}/{self.ruta}"
        imgfiles = [fn for fn in glob.glob(f"{imgfolder}/*")]
        self.images = [Image.open(img) for img in imgfiles]
        self.image1 = None
        self.image2 = None
        self.transalpha = 0
        self.image = self.images[0]

        bgfolder = f"{self.settings['path']['fondos']}"
        tema = self.tema
        tema = tema.replace("ó", "o")
        tema = tema.replace("í", "i")
        tema = tema.replace("ñ", "n")
        self.bgimg1 = Image.open(f"{bgfolder}/{tema} - 1.jpg")
        self.bgimg2 = Image.open(f"{bgfolder}/{tema} - 2.jpg")
        self.bgimg = self.bgimg1
    
    def _on_resize(self, event=None):
        self.width = event.width
        self.height = event.height
        self.set_slide()
        self.update_canvas()
    
    def _on_next(self, event=None):
        if self.transalpha != 0:
            self.after(1, self._on_next)
            return
        if self.changed: return
        self.changed = True
        self.change_slide("next",True)
        #self.update_canvas()
    
    def _on_prev(self, _=None):
        if self.transalpha != 0:
            self.after(1, self._on_prev)
            return
        if self.changed: return
        self.changed = True
        self.change_slide("prev",True)
        #self.update_canvas()
    
    def activate_fullscreen(self):
        self.fullscreen = True
        self.old_geometry = self.geometry()
        self.overrideredirect(True)
        self.state("zoomed")
    
    def deactivate_fullscreen(self):
        self.fullscreen = False
        self.state("normal")
        self.geometry(self.old_geometry)
        self.overrideredirect(False)
    
    def _allow_change(self, _=None):
        self.changed = False
    
    def _toggle_fullscreen(self, _=None):
        if self.fullscreen:
            self.deactivate_fullscreen()
        else:
            self.activate_fullscreen()
        #self.fullscreen = not self.fullscreen
        #self.attributes("-fullscreen", self.fullscreen)
    
    def _toggle_pause(self, _=None):
        self.music.toggle_pause()
    
    def _exit(self, _=None):
        self.settings["player"]["geometry"] = self.geometry()
        self.settings["player"]["fullscreen"] = self.fullscreen
        self.killed = True
        self.music.quit()
        self.destroy()
        self.update()
