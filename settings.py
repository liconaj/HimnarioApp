import sv_ttk
import json
import os


SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "themes": ["light", "dark"],
    "theme": "light",
    "player": {
        "aspect_ratio": "keep",
        "geometry": "800x600",
        "fullscreen": False
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
        sv_ttk.set_theme(self.settings["theme"])
    
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
    
    def set_theme(self, theme):
        sv_ttk.set_theme(theme)
        self.settings["theme"] = theme
    
    def get_player_geometry(self):
        return self.settings["player"]["geometry"]
    
    def set_player_geometry(self, geometry):
        self.settings["player"]["geometry"] = geometry
    
    def get_player_fullscreen(self):
        return self.settings["player"]["fullscreen"]
    
    def set_player_fullscreen(self, fullscreen):
        self.settings["player"]["fullscreen"] = fullscreen
    
    def get_player_aspectratio(self):
        return self.settings["player"]["aspect_ratio"]
    
    def get_lyrics_path(self):
        return self.settings["path"]["lyrics"]
    
    def get_voice_path(self):
        return self.settings["path"]["voice"]
    
    def get_instrumental_path(self):
        return self.settings["path"]["instrumental"]
    
    def get_backgrounds_path(self):
        return self.settings["path"]["backgrounds"]
    
    def get_indexes_path(self):
        return self.settings["path"]["indexes"]