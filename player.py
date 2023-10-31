import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import settings as st
import screeninfo
import music as msc

import glob


class Player(tk.Toplevel):
    def __init__(self, settings: st.Settings, modo: str, infohimno: dict, music=None):
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

    def setup_window(self):
        self.minsize(800, 600)
        self.configure(background="black")
        self.fullscreen = self.settings.get_player_fullscreen()
        if self.fullscreen:
            self.activate_fullscreen()
        else:
            self.geometry(self.settings.get_player_geometry())
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.config(cursor="none")
        self.iconbitmap("Assets/icon.ico")
        self.focus_force()
        self.lift()

    def play_music(self):
        musicpath = ""
        self.playingmusic = False
        if self.modo == "Solo letra":
            return
        elif self.modo == "Cantado":
            musicpath = self.settings.get_voice_path()
        elif self.modo == "Instrumental":
            musicpath = self.settings.get_instrumental_path()
        self.musicfile = f"{musicpath}/{self.ruta}.mp3"
        msc.load(self.musicfile)
        msc.play()
        self.playingmusic = True
        self.synchronize()

    def synchronize(self):
        if self.slideindex < len(self.tiempos) - 1:
            nexttime = self.tiempos[self.slideindex + 1]
            if self.music.get_time() > nexttime:
                self.change_slide("next")
        if self.music.has_ended() and self.settings.get_player_exit_on_finish():
            self.after(0, self._exit)
        self.after(10, self.synchronize)

    def set_infohimno(self, infohimno):
        self.titulo = infohimno['titulo']
        self.numero = infohimno['numero']
        self.tema = infohimno['tema']
        self.ruta = infohimno['ruta']
        self.tiempos = []
        for time in infohimno["tiempos"].split("|"):
            mm, ss, dd = (int(t) for t in time.split(":"))
            tiempoms = dd * 10 + ss * 1000 + mm * 60 * 1000
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

    def change_slide(self, direction, inposed=False):
        oldindex = self.slideindex
        if direction == "prev" and self.slideindex > 0:
            self.slideindex -= 1
        elif direction == "next" and self.slideindex < len(self.images) - 1:
            self.slideindex += 1
        if self.slideindex != oldindex:
            if inposed and self.playingmusic:
                self.music.set_time(self.tiempos[self.slideindex])
            if self.settings.get_player_aspectratio():
                if self.slideindex == 0:
                    self.bgimg = self.bgimg1
                else:
                    self.bgimg = self.bgimg2
            if self.settings.get_player_transitions():
                self.transalpha = 0.0
                self.image1 = self.image.copy()
                self.image2 = self.images[self.slideindex]
                self.transition()
            else:
                self.image = self.images[self.slideindex]
                self.set_slide()

    def transition(self):
        if self.killed:
            return
        if self.transalpha < 1.0:
            self.image = Image.blend(self.image1, self.image2, self.transalpha)
            self.transalpha += 0.5
            self.set_slide()
            self.after(5, self.transition)
        else:
            self.image = self.image2
            self.set_slide()
            self.transalpha = 0

    def set_slide(self):
        nwidth = self.width
        nheight = self.height
        if self.settings.get_player_aspectratio():
            if nwidth > nheight * 4 / 3:
                nwidth = int(nheight * 4 / 3)
            else:
                nheight = int(nwidth * 3 / 4)
        if nwidth == 0 or nheight == 0:
            return
        if self.settings.get_player_aspectratio():
            bgimg = self.bgimg.resize((self.width, self.height))
            image = self.image.resize((nwidth, nheight))
            x = int((self.width - nwidth) / 2)
            y = int((self.height - nheight) / 2)
            bgimg.paste(image, (x, y))
            self.slide = ImageTk.PhotoImage(bgimg)
        else:
            image = self.image.resize((nwidth, nheight))
            self.slide = ImageTk.PhotoImage(image)
        self.update_canvas()

    def get_images(self):
        imgfolder = f"{self.settings.get_lyrics_path()}/{self.ruta}"
        imgfiles = [fn for fn in glob.glob(f"{imgfolder}/*")]
        self.images = [Image.open(img) for img in imgfiles]
        self.image1 = None
        self.image2 = None
        self.transalpha = 0
        self.image = self.images[0]

        bgfolder = f"{self.settings.get_backgrounds_path()}"
        tema = self.tema
        tema = tema.replace("á", "a")
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

    def _on_next(self, _=None):
        if self.transalpha != 0:
            self.after(1, self._on_next)
            return
        if self.changed:
            return
        self.changed = True
        self.change_slide("next", True)

    def _on_prev(self, _=None):
        if self.transalpha != 0:
            self.after(1, self._on_prev)
            return
        if self.changed:
            return
        self.changed = True
        self.change_slide("prev", True)

    def activate_fullscreen(self):
        self.fullscreen = True
        self.old_geometry = self.geometry()
        x, y = self.winfo_x(), self.winfo_y()
        for m in screeninfo.get_monitors():
            if m.x <= x <= m.width and m.y <= y <= m.height:
                self.overrideredirect(True)
                self.geometry(f"{m.width}x{m.height}+{m.x}+{m.y}")
                break

    def deactivate_fullscreen(self):
        self.fullscreen = False
        self.geometry(self.old_geometry)
        self.overrideredirect(False)

    def _allow_change(self, _=None):
        self.changed = False

    def _toggle_fullscreen(self, _=None):
        if self.fullscreen:
            self.deactivate_fullscreen()
        else:
            self.activate_fullscreen()

    def _toggle_pause(self, _=None):
        self.music.toggle_pause()

    def _exit(self, _=None):
        self.settings.set_player_fullscreen(self.fullscreen)
        self.settings.set_player_geometry(self.geometry())
        self.killed = True
        self.music.quit()
        self.destroy()
        self.update()
