import sv_ttk
import json
import os
import tkinter as tk
from tkinter import ttk
from copy import deepcopy

SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "themes": ["light", "dark"],
    "theme": "light",
    "player": {
        "remember_geometry": True,
        "exit_on_finish": True,
        "transitions": False,
        "aspect_ratio": True,
        "geometry": "800x600",
        "fullscreen": False,
    },
    "path": {
        "lyrics": "Assets/Letras",
        "voice": "Assets/Musica/Cantado",
        "instrumental": "Assets/Musica/instrumental",
        "backgrounds": "Assets/Fondos",
        "indexes": "Assets/indices.json"
    }
}


class Settings():
    def __init__(self) -> None:
        if not os.path.exists(SETTINGS_FILE):
            self.reset()           
        sf = open(SETTINGS_FILE, "r", encoding="utf-8")
        self.settings = json.load(sf)
        sf.close()

        self.themes = self.settings.get("themes", DEFAULT_SETTINGS["themes"])
        self.theme = self.settings.get("theme", DEFAULT_SETTINGS["theme"])
        self.player = self.settings.get("player", DEFAULT_SETTINGS["player"])
        self.path = self.settings.get("path", DEFAULT_SETTINGS["path"])
        self._on_update = list()
        sv_ttk.set_theme(self.theme)
    
    def reset(self):
        if os.path.exists(SETTINGS_FILE):
            os.remove(SETTINGS_FILE)
        sf = open(SETTINGS_FILE, 'w')
        json.dump(DEFAULT_SETTINGS, sf, indent=4)
        sf.close()
    
    def update(self):
        for func in self._on_update:
            func()
    
    def save(self):
        os.remove(SETTINGS_FILE)
        settings = deepcopy(self.settings)
        settings["player"]["geometry"] = DEFAULT_SETTINGS["player"]["geometry"]
        #settings["player"]["fullscreen"] = DEFAULT_SETTINGS["player"]["fullscreen"]
        sf = open(SETTINGS_FILE, "w", encoding="utf-8")
        json.dump(settings, sf, indent=4)
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

    def set_theme(self, theme):
        sv_ttk.set_theme(theme)
        self.settings["theme"] = theme
        self.update()
    
    def set_player_fullscreen(self, fullscreen):
        self.settings["player"]["fullscreen"] = fullscreen
        
    def set_player_geometry(self, geometry):
        self.settings["player"]["geometry"] = geometry


class SettingsUI(ttk.Frame):
    def __init__(self, root, settings: Settings) -> None:
        super().__init__(root)
        self.columnconfigure((0), weight=1)
        self.rowconfigure((0,1,2,3), weight=1)
        self.settings = settings
        self.set_old_settings()
        self.setup_themesel()
        self.setup_playerconf()
        self.setup_savereset_button()
    
    def setup_themesel(self):
        self.themesel = ttk.LabelFrame(self, text="Tema") #style="Card.TFrame"
        self.themesel.rowconfigure(2, weight=0)
        self.themesel.grid(row=0, column=0, padx=20, pady=(20,0), sticky="new")
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
        self.buttonlight.grid(row=0, column=0, padx=20, pady=(20,5), sticky="w")
        self.buttondark.grid(row=1, column=0, padx=20, pady=(5,20), sticky="w")
    
    def change_theme(self, _=None):
        theme = self.theme.get()
        self.settings.set_theme(theme)
        self.check_changes()
    
    def change_playerconf(self, _=None):
        for var in self.playervars:
            value = self.playervars[var].get()
            self.settings.settings["player"][var] = value
        self.check_changes()
    
    def setup_playerconf(self):
        self.playerconf = ttk.LabelFrame(self, text="Reproductor de letras") #style="Card.TFrame"
        self.rowconfigure((1,2,3,4), weight=1)
        self.playerconf.grid(row=1, column=0, padx=(20,20), pady=(10,10), sticky="new")
        # variables
        self.playervars = {
            "remember_geometry": tk.BooleanVar(self.playerconf, value=self.settings.get_player_remember_geometry()),
            "aspect_ratio": tk.BooleanVar(self.playerconf, value=self.settings.get_player_aspectratio()),
            "transitions": tk.BooleanVar(self.playerconf, value=self.settings.get_player_transitions()),
            "exit_on_finish": tk.BooleanVar(self.playerconf, value=self.settings.get_player_exit_on_finish())
        }
        # remember geometry
        self.remember_geometry = ttk.Checkbutton(self.playerconf, text="Recordar último tamaño y posición al cerrar", command=self.change_playerconf, variable=self.playervars["remember_geometry"])
        self.remember_geometry.state(["!alternate"])
        self.remember_geometry.grid(row=1, column=0, sticky="nsw", padx=20, pady=(10,0))
        # aspect ratio
        self.aspect_ratio = ttk.Checkbutton(self.playerconf, text="Mantener relación de aspecto", command=self.change_playerconf, variable=self.playervars["aspect_ratio"])
        self.aspect_ratio.grid(row=2, column=0, sticky="nsw", padx=20, pady=(10,0))
        self.aspect_ratio.state(["!alternate"])
        # transitions
        self.transitions = ttk.Checkbutton(self.playerconf, text="Mostrar transiciones (EXPERIMENTAL)", command=self.change_playerconf, variable=self.playervars["transitions"])
        self.transitions.grid(row=3, column=0, sticky="nsw", padx=20, pady=(10,0))
        self.transitions.state(["!alternate"])
        # exit on finish
        self.exit_on_finish = ttk.Checkbutton(self.playerconf, text="Cerrar ventana al finalizar", command=self.change_playerconf, variable=self.playervars["exit_on_finish"])
        self.exit_on_finish.grid(row=4, column=0, sticky="nsw", padx=20, pady=(10,20))
        self.exit_on_finish.state(["!alternate"])

    def _validate_number(self, text):
        number = text.get()
        if not number.isdigit():
            text.set(number[:-1])
    
    def set_old_settings(self):
        self.old_settings = deepcopy(self.settings.settings)

    def check_changes(self):
        if self.settings.settings != self.old_settings:
            self.save_button.config(style="Accent.TButton")
        else:
            self.save_button.config(style="TButton")

    
    def save_changes(self):
        self.set_old_settings()
        self.settings.save()
        self.save_button.config(style="TButton")
    
    def reset_changes(self):
        if self.settings.settings != DEFAULT_SETTINGS:
            self.old_settings()
            self.save_button.config(style="Accent.TButton")
            self.settings.settings = DEFAULT_SETTINGS
            self.theme.set(self.settings.get_theme())
            self.change_theme()
    
    def setup_savereset_button(self):
        self.savereset_frame = ttk.Frame(self)
        self.savereset_frame.columnconfigure((0,1), weight=0)
        self.savereset_frame.grid(row=4, sticky="es")
        self.save_button = ttk.Button(self.savereset_frame,text="Guardar", command=self.save_changes)
        self.reset_button = ttk.Button(self.savereset_frame,text="Restablecer", command=self.reset_changes)
        self.save_button.config(style="TButton")
        self.save_button.grid(row=0,column=1,sticky="se",padx=(10,20),pady=20)
        self.reset_button.grid(row=0,column=0,sticky="se",padx=(20,10),pady=20)