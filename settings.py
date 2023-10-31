import sv_ttk
import json
import os
import sys
import tkinter as tk
from tkinter import ttk
import ctypes

DATA_DIR = "Data"
SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "version": "0.0.7",
    "themes": ["light", "dark"],
    "theme": "light",
    "player": {
        "remember_geometry": False,
        "exit_on_finish": True,
        "transitions": False,
        "aspect_ratio": True,
        "geometry": "800x600",
        "fullscreen": False,
    },
    "path": {
        "lyrics": f"{DATA_DIR}/Letras",
        "voice": f"{DATA_DIR}/Musica/Cantado",
        "instrumental": f"{DATA_DIR}/Musica/Instrumental",
        "backgrounds": f"{DATA_DIR}/Fondos",
        "indexes": f"{DATA_DIR}/indices.json"
    }
}


def reset():
    if os.path.exists(SETTINGS_FILE):
        os.remove(SETTINGS_FILE)
    sf = open(SETTINGS_FILE, 'w')
    json.dump(DEFAULT_SETTINGS, sf, indent=4)
    sf.close()


class Settings:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        if not os.path.exists(SETTINGS_FILE):
            reset()
        sf = open(SETTINGS_FILE, "r", encoding="utf-8")
        self.settings = json.load(sf)
        sf.close()
        if self.settings.get("version", "undefined") != DEFAULT_SETTINGS["version"]:
            self.settings = DEFAULT_SETTINGS
            reset()
        self.themes = self.settings.get("themes", DEFAULT_SETTINGS["themes"])
        self.theme = self.settings.get("theme", DEFAULT_SETTINGS["theme"])
        self.player = self.settings.get("player", DEFAULT_SETTINGS["player"])
        self.path = self.settings.get("path", DEFAULT_SETTINGS["path"])
        if not self.get_player_remember_geometry():
            self.set_player_fullscreen(DEFAULT_SETTINGS["player"]["fullscreen"])
            self.set_player_geometry(DEFAULT_SETTINGS["player"]["geometry"])
        self.on_update = list()
        self.set_theme(self.theme)

    def update(self):
        for func in self.on_update:
            func()

    def save(self):
        if os.path.exists(SETTINGS_FILE):
            os.remove(SETTINGS_FILE)
        sf = open(SETTINGS_FILE, "w", encoding="utf-8")
        json.dump(self.settings, sf, indent=4)
        sf.close()

    def get_theme(self):
        return self.settings["theme"]

    def get_player_geometry(self):
        return self.player.get("geometry", DEFAULT_SETTINGS["player"]["geometry"])

    def get_player_size(self):
        geom = self.get_player_geometry()
        size = geom.split("+")[0]
        size = size.split("x")
        return int(size[0]), int(size[1])

    def get_player_remember_geometry(self):
        return self.player.get("remember_geometry", DEFAULT_SETTINGS["player"]["remember_geometry"])

    def get_player_fullscreen(self):
        return self.player.get("fullscreen", DEFAULT_SETTINGS["player"]["fullscreen"])

    def get_player_transitions(self):
        return self.player.get("transitions", DEFAULT_SETTINGS["player"]["transitions"])

    def get_player_exit_on_finish(self):
        return self.player.get("exit_on_finish", DEFAULT_SETTINGS["player"]["exit_on_finish"])

    def get_player_aspectratio(self):
        return self.player.get("aspect_ratio", DEFAULT_SETTINGS["player"]["aspect_ratio"])

    def get_lyrics_path(self):
        return self.path.get("lyrics", DEFAULT_SETTINGS["path"]["lyrics"])

    def get_voice_path(self):
        return self.path.get("path", DEFAULT_SETTINGS["path"]["voice"])

    def get_instrumental_path(self):
        return self.path.get("instrumental", DEFAULT_SETTINGS["path"]["instrumental"])

    def get_backgrounds_path(self):
        return self.path.get("backgrounds", DEFAULT_SETTINGS["path"]["backgrounds"])

    def get_indexes_path(self):
        return self.path.get("indexes", DEFAULT_SETTINGS["path"]["indexes"])

    def set_theme(self, theme: str):
        sv_ttk.set_theme(theme)
        self.settings["theme"] = theme
        self.root.update()
        self._windows_set_titlebar_color(theme)
        self.update()

    def set_player_fullscreen(self, fullscreen: bool):
        self.settings["player"]["fullscreen"] = fullscreen

    def set_player_geometry(self, geometry: str):
        self.settings["player"]["geometry"] = geometry

    def _windows_set_titlebar_color(self, color_mode: str):
        window = self.root
        if sys.platform.startswith("win"):
            if color_mode.lower() == "dark":
                value = 1
            elif color_mode.lower() == "light":
                value = 0
            else:
                return
            try:
                hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19
                # try with DWMWA_USE_IMMERSIVE_DARK_MODE
                if ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                                                              ctypes.byref(ctypes.c_int(value)),
                                                              ctypes.sizeof(ctypes.c_int(value))) != 0:
                    # try with DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20h1
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1,
                                                               ctypes.byref(ctypes.c_int(value)),
                                                               ctypes.sizeof(ctypes.c_int(value)))
            except Exception as err:
                print(err)


class SettingsUI(ttk.Frame):
    def __init__(self, root: tk.Tk, settings: Settings) -> None:
        super().__init__(root)
        self.root = root
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)
        self.settings = settings
        self.setup_themesel()
        self.setup_playerconf()
        self.setup_reset_button()

    def setup_themesel(self):
        self.themesel = ttk.LabelFrame(self, text="Tema")
        self.themesel.rowconfigure(2, weight=0)
        self.themesel.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="new")
        self.theme = tk.StringVar(value=self.settings.get_theme())
        self.buttonlight = ttk.Radiobutton(self.themesel,
                                           text="Claro",
                                           variable=self.theme,
                                           value="light",
                                           command=self.change_theme)
        self.buttondark = ttk.Radiobutton(self.themesel,
                                          text="Oscuro",
                                          variable=self.theme,
                                          value="dark",
                                          command=self.change_theme)
        self.buttonlight.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        self.buttondark.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="w")

    def change_theme(self, _=None):
        theme = self.theme.get()
        self.settings.set_theme(theme)

    def change_playerconf(self, _=None):
        for var in self.playervars:
            value = self.playervars[var].get()
            self.settings.settings["player"][var] = value

    def setup_playerconf(self):
        self.playerconf = ttk.LabelFrame(self, text="Reproductor de letras")
        self.rowconfigure(4, weight=1)
        self.playerconf.grid(row=1, column=0, padx=(20, 20), pady=(10, 10), sticky="new")
        # variables
        self.playervars = {
            "remember_geometry": tk.BooleanVar(self.playerconf, value=self.settings.get_player_remember_geometry()),
            "aspect_ratio": tk.BooleanVar(self.playerconf, value=self.settings.get_player_aspectratio()),
            "transitions": tk.BooleanVar(self.playerconf, value=self.settings.get_player_transitions()),
            "exit_on_finish": tk.BooleanVar(self.playerconf, value=self.settings.get_player_exit_on_finish())
        }
        # remember geometry
        self.remember_geometry = ttk.Checkbutton(self.playerconf, text="Recordar configuración de ventana",
                                                 command=self.change_playerconf,
                                                 variable=self.playervars["remember_geometry"])
        self.remember_geometry.grid(row=1, column=0, sticky="nsw", padx=20, pady=(10, 0))
        self.remember_geometry.state(["!alternate"])
        # aspect ratio
        self.aspect_ratio = ttk.Checkbutton(self.playerconf, text="Mantener relación de aspecto",
                                            command=self.change_playerconf, variable=self.playervars["aspect_ratio"])
        self.aspect_ratio.grid(row=2, column=0, sticky="nsw", padx=20, pady=(10, 0))
        self.aspect_ratio.state(["!alternate"])
        # transitions
        self.transitions = ttk.Checkbutton(self.playerconf,
                                           text="Mostrar transiciones (Advertencia: puede llegar a ser lento)",
                                           command=self.change_playerconf, variable=self.playervars["transitions"])
        self.transitions.grid(row=3, column=0, sticky="nsw", padx=20, pady=(10, 0))
        self.transitions.state(["!alternate"])
        # exit on finish
        self.exit_on_finish = ttk.Checkbutton(self.playerconf, text="Cerrar ventana al finalizar",
                                              command=self.change_playerconf,
                                              variable=self.playervars["exit_on_finish"])
        self.exit_on_finish.grid(row=4, column=0, sticky="nsw", padx=20, pady=(10, 20))
        self.exit_on_finish.state(["!alternate"])

    def reset_changes(self):
        if self.settings.settings != DEFAULT_SETTINGS:
            self.settings.settings = DEFAULT_SETTINGS
            self.theme.set(self.settings.get_theme())
            self.change_theme()
        for var in self.playervars:
            self.playervars[var].set(self.settings.settings["player"][var])

    def setup_reset_button(self):
        self.reset_button = ttk.Button(self, text="Restablecer", command=self.reset_changes)
        self.reset_button.grid(row=4, sticky="sw", padx=20, pady=20)
