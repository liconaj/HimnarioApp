import json
import re

import unicodedata

from music import *
from player import *


class Finder(ttk.Frame):
    def __init__(self, settings: st.Settings) -> None:
        super().__init__()
        self.settings = settings

        self.mixer = Music()
        self.playing = False
        self.player = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.set_listahimnos()
        self.setup_modeselector()
        self.setup_search()

        self.bind("<Button-1>", self._takeout_focus)

    def setup_modeselector(self) -> None:
        self.modeselector = PlayModeSelector(self)
        self.modeselector.config(width=50)
        self.modeselector.grid(row=0, column=0, padx=20, pady=(20, 10))

    def setup_search(self) -> None:
        self.search = SearchEntries(self)
        self.search.grid(row=1, column=0, padx=0, pady=10)
        self.search.columnconfigure(2, weight=1)
        self.search.rowconfigure(2, weight=1)

    def set_listahimnos(self) -> None:
        datafile = self.settings.get_indexes_path()
        fhandler = open(datafile, "r", encoding="utf-8")
        infohimnos = json.load(fhandler)
        self.titulos = {}
        self.numeros = {}
        for info in infohimnos["lista"]:
            self.numeros[int(info["numero"])] = info
            self.titulos[info["titulo"]] = info
        self.temas = infohimnos["temas"]
        for tema in self.temas:
            nombretema = tema["nombre"]
            if tema["hassubs"]:
                for sub in tema["subtemas"]:
                    nombresub = f'{nombretema} - {sub["nombre"]}'
                    rango = sub["rango"]
                    for numero in range(rango[0], rango[1] + 1):
                        self.numeros[numero]["tema"] = nombresub
            else:
                rango = tema["rango"]
                for numero in range(rango[0], rango[1] + 1):
                    self.numeros[numero]["tema"] = nombretema

    def start_player(self, _=None) -> None:
        number = self.search.getnumber()
        if number is None:
            return
        infohimno = self.numeros[number]
        modo = self.modeselector.getmode()
        if self.player is not None and self.player.winfo_exists():
            self.player.new_song(modo, infohimno)
        else:
            self.player = Player(self, self.settings, modo, infohimno, self.mixer)

    def _takeout_focus(self, event=None) -> None:
        if event.widget == self:
            self.focus()


class PlayModeSelector(ttk.Frame):
    def __init__(self, root: Finder, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.columnconfigure(3, weight=1)
        self.mode = tk.IntVar(value=1)
        self.modes = ["Solo letra", "Cantado", "Instrumental"]
        self.addmode(0)
        self.addmode(1)
        self.addmode(2)

    def addmode(self, value: int) -> None:
        text = self.modes[value]
        button = ttk.Radiobutton(self, text=text, variable=self.mode, value=value, style="Toggle.TButton", width=12)
        button.grid(row=0, column=value, padx=5, pady=5)

    def getmode(self) -> str:
        return self.modes[self.mode.get()]


class SearchEntries(ttk.Frame):
    def __init__(self, root: Finder):
        super().__init__(root)
        self.root = root
        self.settings = root.settings
        self.titulos = root.titulos
        self.numeros = root.numeros
        self.start_player = root.start_player
        self.columnconfigure(3, weight=1)
        self.rowconfigure(2, weight=1)
        self.setup_numberentry()
        self.setup_titleentry()
        self.setup_playbutton()
        self.setup_resultslist()
        self.mybind("<Return>", self.start_player)

    def setup_numberentry(self) -> None:
        self.numbertext = tk.StringVar()
        self.numberentry = PlaceholderEntry(self, self.numbertext, "#")
        self.numberentry.config(justify="center", width=5, font="Arial 16 bold", textvariable=self.numbertext)
        self.numberentry.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        self.numbertext.trace("w", lambda *args: self._validate_number())
        self.add_on_updatesettings(self.numberentry.update_placeholder)

    def setup_titleentry(self) -> None:
        self.titletext = tk.StringVar()
        self.titleentry = PlaceholderEntry(self, self.titletext, "Título del himno")

        self.titleentry.config(justify="center", width=39, font="Arial 16 bold", textvariable=self.titletext)
        self.titleentry.grid(row=0, column=1, padx=(5, 5), sticky="ew")
        self.titletext.trace("w", lambda *args: self._validate_title())
        self.titleentry.bind("<Tab>", self._on_focus_result)
        self.titleentry.bind("<Down>", self._on_focus_result)
        self.add_on_updatesettings(self.titleentry.update_placeholder)

    def setup_playbutton(self) -> None:
        self.playimg = {"dark": ImageTk.PhotoImage(Image.open(f"{st.DATA_DIR}/Iconos/play_dark.png")),
                        "light": ImageTk.PhotoImage(Image.open(f"{st.DATA_DIR}/Iconos/play_light.png")),
                        "dark_ready": ImageTk.PhotoImage(Image.open(f"{st.DATA_DIR}/Iconos/play_dark_ready.png")),
                        "light_ready": ImageTk.PhotoImage(Image.open(f"{st.DATA_DIR}/Iconos/play_light_ready.png"))}
        self.playbutton = ttk.Button(self, command=self.start_player)
        self.update_playbutton()
        self.playbutton.grid(row=0, column=2, padx=(5, 0), sticky="nsw")
        self.add_on_updatesettings(self.update_playbutton)

    def update_playbutton(self) -> None:
        theme = self.settings.get_theme()
        ready = self.getnumber() is not None
        playimg = theme
        if ready:
            playimg += "_ready"
        self.playbutton.config(image=self.playimg[playimg])

    def setup_resultslist(self) -> None:
        self.results = ttk.Frame(self)
        self.results.grid(row=1, column=0, columnspan=3, pady=10)
        self.results.columnconfigure(2, weight=1)
        self.scrollbar = ttk.Scrollbar(self.results)
        self.scrollbar.grid(row=0, column=1, sticky="nsw")
        self.resultslist = ttk.Treeview(self.results, height=11, columns=("1", "2"), selectmode="browse",
                                        show=("tree",), yscrollcommand=self.scrollbar.set)
        self.resultslist.column("#0", width=0, stretch=True)
        self.resultslist.column(1, anchor="center", width=40)
        self.resultslist.column(2, anchor="center", width=560)
        self.scrollbar.config(command=self.resultslist.yview)
        self.resultslist.grid(row=0, column=0, sticky="ew")
        self.resultslist.bind("<<TreeviewSelect>>", self._on_select)
        self.resultslist.bind("<Tab>", self._on_next_tab)
        self.resultslist.bind("<Down>", self._on_next_tab)
        self.resultslist.bind("<Shift-Tab>", self._on_prev_tab)
        self.resultslist.bind("<Up>", self._on_prev_tab)
        self.resultslist.bind("<Double-Button-1>", self.start_player)
        self.show_alltitles()

    def show_alltitles(self) -> None:
        self.resultslist.delete(*self.resultslist.get_children())
        for n, info in self.numeros.items():
            self.resultslist.insert("", index="end", values=(n, info["titulo"]))

    def search_titles(self, titlesearch: str) -> None:
        self.resultslist.delete(*self.resultslist.get_children())
        for title in self.titulos:
            if normalizetxt(titlesearch) in normalizetxt(title):
                n = self.titulos[title]["numero"]
                self.resultslist.insert("", index="end", values=(n, title))

    def mybind(self, sequence: str, func: callable) -> None:
        self.numberentry.bind(sequence, func)
        self.titleentry.bind(sequence, func)
        self.resultslist.bind(sequence, func)

    def getnumber(self) -> int:
        number = self.numbertext.get()
        if number and number != self.numberentry.placeholder:
            return int(number)

    def _validate_number(self) -> None:
        if self.focus_get() != self.numberentry:
            return
        number = self.numbertext.get()
        if number == self.numberentry.placeholder:
            return
        self.update_playbutton()

        maxdigits = 3
        maxnumber = 614

        if not number.isdigit():
            self.numbertext.set(number[:-1])
        elif len(number) > maxdigits:
            self.numbertext.set(number[:maxdigits])
        elif len(number) > 0 and int(number) > maxnumber:
            self.after(100, lambda *args: self.numbertext.set(str(maxnumber)))

        if not number:
            self.titleentry.show_placeholder()
            self.show_alltitles()
        elif number.isdigit() and int(number) in range(1, maxnumber + 1):
            self.show_alltitles()
            number = int(number)
            titulo = self.numeros[number]["titulo"]
            self.titleentry.hide_placeholder()
            self.titletext.set(titulo)
            titles = self.resultslist.get_children()
            self.resultslist.selection_set(titles[number - 1])
            itemsee = number
            if number > 607:
                itemsee = 614
            elif number > 5:
                itemsee += 6
            self.resultslist.see(titles[itemsee - 1])

    def _validate_title(self) -> None:
        if self.focus_get() != self.titleentry:
            return
        titulo = self.titletext.get()
        if titulo == self.titleentry.placeholder:
            return

        allowedchars = "abcdefghijklmnñopqrstuvwxyzáéíóúü"
        allowedchars += allowedchars.upper()
        allowedchars += " ,¡!¿?"

        if titulo not in list(self.titulos.keys()):
            self.numberentry.show_placeholder()
        else:
            n = self.titulos[titulo]["numero"]
            self.numberentry.hide_placeholder()
            self.numbertext.set(n)
        if len(titulo) > 0 and not titulo[-1] in allowedchars:
            self.titleentry.hide_placeholder()
            self.titletext.set(titulo[:-1])
        if self.focus_get() == self.titleentry:
            self.search_titles(self.titletext.get())
        state = "!invalid"
        if len(self.resultslist.get_children()) == 0:
            state = "invalid"
        self.titleentry.state([state])
        self.update_playbutton()

    def change_title(self, direction="next") -> None:
        idir = 1
        if direction == "prev":
            idir = -1
        titulos = self.resultslist.get_children()
        selecteditems = self.resultslist.selection()
        if len(selecteditems) == 0:
            selindex = -1
        else:
            selected = selecteditems[0]
            selindex = titulos.index(selected)
        nexti = selindex + idir
        if nexti == len(titulos):
            nexti = 0
        elif nexti < 0:
            nexti = len(titulos) - 1
        self.resultslist.see(titulos[nexti])
        self.resultslist.selection_set(titulos[nexti])
        self.update_playbutton()

    def add_on_updatesettings(self, func: callable) -> None:
        self.settings.on_update.append(func)

    def _on_focus_result(self, _=None) -> str:
        items = self.resultslist.get_children()
        self.resultslist.focus_set()
        if len(items) > 0:
            self.resultslist.selection_set(items[0])
        return "break"

    def _on_next_tab(self, _=None) -> str:
        self.change_title("next")
        return "break"  # evita que cambie el foco a otro widget

    def _on_prev_tab(self, _=None) -> str:
        self.change_title("prev")
        return "break"  # evita que cambie el foco a otro widget

    def _on_select(self, _=None) -> None:
        if len(self.resultslist.selection()) == 0:
            return
        item = self.resultslist.selection()[0]
        n, title = self.resultslist.item(item, "values")
        currnumber = self.numbertext.get()
        currtitle = self.titletext.get()
        if currnumber != n:
            self.numberentry.hide_placeholder()
            self.numbertext.set(n)
        if currtitle != title:
            self.titleentry.hide_placeholder()
            self.titletext.set(title)
        self.update_playbutton()


def normalizetxt(texto: str) -> str:
    texto = re.sub(r'[^\w\s]', '', texto.lower())
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto


class PlaceholderEntry(ttk.Entry):
    def __init__(self, root: SearchEntries, textvariable: tk.StringVar, placeholder: str, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.settings = root.settings
        self.colors = {"light": ["#1c1c1c", "#d7d7d7"], "dark": ["#e7e7e7", "#4c4c4c"]}
        self.is_placeholder = 1
        self.placeholder = f"ㅤ{placeholder}ㅤ"
        self.textvariable = textvariable

        self.show_placeholder()
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def hide_placeholder(self) -> None:
        self.is_placeholder = 0
        self.update_placeholder()
        if self.textvariable.get() == self.placeholder:
            self.textvariable.set("")

    def show_placeholder(self) -> None:
        self.is_placeholder = 1
        self.update_placeholder()
        self.textvariable.set(self.placeholder)

    def update_placeholder(self) -> None:
        theme = self.settings.get_theme()
        self.config(foreground=self.colors[theme][self.is_placeholder])

    def _on_focus_in(self, _=None) -> None:
        self.hide_placeholder()

    def _on_focus_out(self, _=None) -> None:
        if self.textvariable.get() == "":
            self.show_placeholder()
