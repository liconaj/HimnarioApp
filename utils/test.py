import tkinter as tk
from src import music as msc, settings as st
import json
import glob
from PIL import Image
import pygame

pygame.init()
pygame.mixer.init()

root = tk.Tk()
settings = st.Settings(root)


def get_images(ruta, tema):
    imgfolder = f"{settings.get_lyrics_path()}/{ruta}"
    imgfiles = [fn for fn in glob.glob(f"{imgfolder}/*")]
    images = [Image.open(img) for img in imgfiles]
    bgfolder = f"{settings.get_backgrounds_path()}"
    bgimg1 = Image.open(f"{bgfolder}/{tema} - 1.jpg")
    bgimg2 = Image.open(f"{bgfolder}/{tema} - 2.jpg")


def play_music(ruta, modo):
    musicpath = ""
    if modo == "Cantado":
        musicpath = settings.get_voice_path()
    elif modo == "Instrumental":
        musicpath = settings.get_instrumental_path()
    musicfile = f"{musicpath}/{ruta}.mp3"
    msc.load(musicfile)
    msc.unload()


def get_listahimnos():
    datafile = settings.get_indexes_path()
    fhandler = open(datafile, "r", encoding="utf-8")
    infohimnos = json.load(fhandler)
    titulos = {}
    numeros = {}
    for info in infohimnos["lista"]:
        numeros[int(info["numero"])] = info
        titulos[info["titulo"]] = info
    temas = infohimnos["temas"]
    for tema in temas:
        nombretema = tema["nombre"]
        if tema["hassubs"]:
            for sub in tema["subtemas"]:
                nombresub = f'{nombretema} - {sub["nombre"]}'
                rango = sub["rango"]
                for numero in range(rango[0], rango[1] + 1):
                    numeros[numero]["tema"] = nombresub
        else:
            rango = tema["rango"]
            for numero in range(rango[0], rango[1] + 1):
                numeros[numero]["tema"] = nombretema
    return numeros, titulos

numeros, titulos = get_listahimnos()
for n in numeros:
    infohimno = numeros[n]
    tema = infohimno["tema"]
    ruta = infohimno["ruta"]
    tema = tema.replace("á", "a")
    tema = tema.replace("ó", "o")
    tema = tema.replace("í", "i")
    tema = tema.replace("ñ", "n")
    try:
        get_images(ruta, tema)
    except Exception as e:
        print("\n\nIMAGEN:")
        print(e)
    try:
        play_music(ruta, "Cantado")
    except Exception as e:
        print("\n\nCANTADO:")
        print(e)
    try:
        play_music(ruta, "Instrumental")
    except Exception as e:
        print("\n\nINSTRUMENTAL:")
        print(e)
