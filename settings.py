import sv_ttk
import json
import os


SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "themes": ["light", "dark"],
    "theme": "light",
    "player": {
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
        sv_ttk.set_theme(self.theme)
    
    def reset(self):
        if os.path.exists(SETTINGS_FILE):
            os.remove(SETTINGS_FILE)
        sf = open(SETTINGS_FILE, 'w')
        json.dump(DEFAULT_SETTINGS, sf, indent=4)
        sf.close()
    
    def save(self):
        os.remove(SETTINGS_FILE)
        settings = self.settings.copy()
        settings["player"]["geometry"] = DEFAULT_SETTINGS["player"]["geometry"]
        settings["player"]["fullscreen"] = DEFAULT_SETTINGS["player"]["fullscreen"]
        sf = open(SETTINGS_FILE, "w", encoding="utf-8")
        json.dump(settings, sf, indent=4)
        sf.close()

    def get_theme(self):
        return self.settings["theme"]
    
    def get_player_geometry(self):
        return self.player.get("geometry", DEFAULT_SETTINGS["player"]["geometry"])
    
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
        return self.path.get("insturmental", DEFAULT_SETTINGS["path"]["instrumental"])
    
    def get_backgrounds_path(self):
        return self.path.get("backgrounds", DEFAULT_SETTINGS["path"]["backgrounds"])
    
    def get_indexes_path(self):
        return self.path.get("indexes", DEFAULT_SETTINGS["path"]["indexes"])

    def set_theme(self, theme):
        sv_ttk.set_theme(theme)
        self.settings["theme"] = theme
    
    def set_player_fullscreen(self, fullscreen):
        self.settings["player"]["fullscreen"] = fullscreen
        
    def set_player_geometry(self, geometry):
        self.settings["player"]["geometry"] = geometry