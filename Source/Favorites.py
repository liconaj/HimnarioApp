import json
import os

import Source.Settings as Settings


def reset(settings: Settings.Settings) -> None:
    favorites_file = settings.get_favorites_path()
    with open(favorites_file, "w", encoding="utf-8") as sf:
        json.dump([], sf, indent=4)
        sf.close()


def get(settings: Settings.Settings) -> list:
    favorites_file = settings.get_favorites_path()
    if not os.path.exists(favorites_file):
        reset(settings)
    with open(favorites_file, "r", encoding="utf-8") as sf:
        favorites = json.load(sf)
        sf.close()
    return favorites


def save(settings: Settings.Settings, favorites: list) -> None:
    favorites_file = settings.get_favorites_path()
    with open(favorites_file, "w", encoding="utf-8") as sf:
        json.dump(favorites, sf, indent=4)
        sf.close()


class FavoritesUI:
    def __init__(self):
        pass
