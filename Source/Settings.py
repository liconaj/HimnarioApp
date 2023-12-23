import ctypes
import json
import os
import sys
import tkinter as tk
from tkinter import ttk

import sv_ttk

SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "theme": "light",
    "player": {
        "remember_geometry": False,
        "exit_on_finish": True,
        "transitions": False,
        "aspect_ratio": True,
        "fullscreen_geometry": None,
        "normal_geometry": "800x600",
        "fullscreen": False,
    },
    "path": {
        "lyrics": "Letras",
        "voice": "Musica/Cantado",
        "instrumental": "Musica/Instrumental",
        "backgrounds": "Fondos",
        "icons": "Iconos",
        "indexes": "indices.json",
        "favorites": "favoritos.json"
    }
}


def make_dpi_aware() -> None:
    if sys.platform.startswith("win"):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # solo funciona en Windows desde la versión 8.1
        except Exception as err:
            print(f"\n\nDpiAwareness: versión de Windows incompatible: {err}", file=sys.stderr)


class Settings:
    def __init__(self, root: tk.Tk, data_dir: str) -> None:
        self.root = root
        self.data_dir = data_dir
        self.settings_file = f"{data_dir}/{SETTINGS_FILE}"
        if not os.path.exists(self.settings_file):
            self.reset()
        sf = open(self.settings_file, "r", encoding="utf-8")
        self.settings = json.load(sf)
        sf.close()
        self.theme = self.settings.get("theme", DEFAULT_SETTINGS["theme"])
        self.player = self.settings.get("player", DEFAULT_SETTINGS["player"])
        self.path = self.settings.get("path", DEFAULT_SETTINGS["path"])
        if not self.get_player_remember_geometry():
            self.set_player_fullscreen(DEFAULT_SETTINGS["player"]["fullscreen"])
            self.set_player_normal_geometry(DEFAULT_SETTINGS["player"]["normal_geometry"])
            self.set_player_fullscreen_geometry(DEFAULT_SETTINGS["player"]["fullscreen_geometry"])
        self.on_update = list()
        self.set_theme(self.theme)

    def reset(self) -> None:
        if os.path.exists(self.settings_file):
            os.remove(self.settings_file)
        sf = open(self.settings_file, 'w', encoding="utf-8")
        json.dump(DEFAULT_SETTINGS, sf, indent=4)
        sf.close()

    def update(self) -> None:
        for func in self.on_update:
            func()

    def save(self) -> None:
        if os.path.exists(self.settings_file):
            os.remove(self.settings_file)
        sf = open(self.settings_file, "w", encoding="utf-8")
        json.dump(self.settings, sf, indent=4)
        sf.close()

    def get_theme(self) -> str:
        return self.settings["theme"]

    def get_player_normal_geometry(self) -> str:
        return self.player.get("normal_geometry", DEFAULT_SETTINGS["player"]["normal_geometry"])

    def get_player_fullscreen_geometry(self) -> str:
        return self.player.get("fullscreen_geometry", DEFAULT_SETTINGS["player"]["fullscreen_geometry"])

    def get_player_size(self) -> tuple:
        if self.get_player_fullscreen():
            geom = self.get_player_fullscreen_geometry()
        else:
            geom = self.get_player_normal_geometry()
        size = geom.split("+")[0]
        size = size.split("x")
        return int(size[0]), int(size[1])

    def get_player_remember_geometry(self) -> bool:
        return self.player.get("remember_geometry", DEFAULT_SETTINGS["player"]["remember_geometry"])

    def get_player_fullscreen(self) -> bool:
        return self.player.get("fullscreen", DEFAULT_SETTINGS["player"]["fullscreen"])

    def get_player_transitions(self) -> bool:
        return self.player.get("transitions", DEFAULT_SETTINGS["player"]["transitions"])

    def get_player_exit_on_finish(self) -> bool:
        return self.player.get("exit_on_finish", DEFAULT_SETTINGS["player"]["exit_on_finish"])

    def get_player_aspectratio(self) -> bool:
        return self.player.get("aspect_ratio", DEFAULT_SETTINGS["player"]["aspect_ratio"])

    def get_lyrics_path(self) -> str:
        lyrics = self.path.get("lyrics", DEFAULT_SETTINGS["path"]["lyrics"])
        return f"{self.data_dir}/{lyrics}"

    def get_voice_path(self) -> str:
        voice = self.path.get("voice", DEFAULT_SETTINGS["path"]["voice"])
        return f"{self.data_dir}/{voice}"

    def get_icons_path(self) -> str:
        icons = self.path.get("icons", DEFAULT_SETTINGS["path"]["icons"])
        return f"{self.data_dir}/{icons}"

    def get_instrumental_path(self) -> str:
        instrumental = self.path.get("instrumental", DEFAULT_SETTINGS["path"]["instrumental"])
        return f"{self.data_dir}/{instrumental}"

    def get_backgrounds_path(self) -> str:
        backgrounds = self.path.get("backgrounds", DEFAULT_SETTINGS["path"]["backgrounds"])
        return f"{self.data_dir}/{backgrounds}"

    def get_indexes_path(self) -> str:
        indexes = self.path.get("indexes", DEFAULT_SETTINGS["path"]["indexes"])
        return f"{self.data_dir}/{indexes}"

    def get_favorites_path(self) -> str:
        favorites = self.path.get("favorites", DEFAULT_SETTINGS["path"]["favorites"])
        return f"{self.data_dir}/{favorites}"

    def set_theme(self, theme: str) -> None:
        sv_ttk.set_theme(theme)
        self.settings["theme"] = theme
        self.root.update()
        self._windows_set_titlebar_color(theme)
        self.update()

    def set_player_fullscreen(self, fullscreen: bool) -> None:
        self.settings["player"]["fullscreen"] = fullscreen

    def set_player_normal_geometry(self, geometry: str) -> None:
        self.settings["player"]["normal_geometry"] = geometry

    def set_player_fullscreen_geometry(self, geometry: str | None) -> None:
        self.settings["player"]["fullscreen_geometry"] = geometry

    def _windows_set_titlebar_color(self, color_mode: str) -> None:
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
                print(f"\n\nWindowAttribute Modo Oscure: Versión de Windows incompatible: {err}", file=sys.stderr)


class SettingsUI(ttk.Frame):
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.settings = settings
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)
        self.setup_themesel()
        self.setup_playerconf()
        self.setup_reset_button()

    def setup_themesel(self) -> None:
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

    def change_theme(self, _=None) -> None:
        theme = self.theme.get()
        self.settings.set_theme(theme)

    def change_playerconf(self, _=None) -> None:
        for var in self.playervars:
            value = self.playervars[var].get()
            self.settings.settings["player"][var] = value

    def setup_playerconf(self) -> None:
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
                                           text="Mostrar transiciones",
                                           command=self.change_playerconf, variable=self.playervars["transitions"])
        self.transitions.grid(row=3, column=0, sticky="nsw", padx=20, pady=(10, 0))
        self.transitions.state(["!alternate"])
        # exit on finish
        self.exit_on_finish = ttk.Checkbutton(self.playerconf, text="Cerrar ventana al finalizar",
                                              command=self.change_playerconf,
                                              variable=self.playervars["exit_on_finish"])
        self.exit_on_finish.grid(row=4, column=0, sticky="nsw", padx=20, pady=(10, 20))
        self.exit_on_finish.state(["!alternate"])

    def reset_changes(self) -> None:
        if self.settings.settings != DEFAULT_SETTINGS:
            self.settings.settings = DEFAULT_SETTINGS
            self.theme.set(self.settings.get_theme())
            self.change_theme()
        for var in self.playervars:
            self.playervars[var].set(self.settings.settings["player"][var])

    def setup_reset_button(self) -> None:
        self.reset_button = ttk.Button(self, text="Restablecer", command=self.reset_changes)
        self.reset_button.grid(row=4, sticky="sw", padx=20, pady=20)
