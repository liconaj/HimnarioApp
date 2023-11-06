from tkinter import ttk
import Source.Utils as Utils


class Indexes(ttk.Frame):
    def __init__(self, indices: dict):
        super().__init__()
        self.indices = indices
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.indexframe = ttk.Frame(self)
        self.indexframe.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.indexframe.grid_columnconfigure(0, weight=1)
        self.indexframe.grid_columnconfigure(2, weight=1)
        self.setup_themeindex()
        self.setup_titleindex()

    def setup_themeindex(self):
        self.themeindex = ttk.Treeview(self.indexframe, columns=("numeros",), height=25, show="tree",
                                       selectmode="none")
        self.themeindex.grid(row=0, column=0, sticky="nsew")
        self.themeindex.column("#0", width=200, minwidth=5, anchor="w", stretch=True)
        self.themeindex.column("numeros", width=10, minwidth=5, anchor="e", stretch=True)
        self.themescrollbar = ttk.Scrollbar(self.indexframe)
        self.themescrollbar.config(command=self.themeindex.yview)
        self.themeindex.config(yscrollcommand=self.themescrollbar.set)
        self.themescrollbar.grid(row=0, column=1, sticky="nsw")
        for tema in self.indices["temas"]:
            if tema["hassubs"]:
                temaiid = self.themeindex.insert("", index="end", text=tema["nombre"], open=True)
                for subtema in tema["subtemas"]:
                    subiid = self.themeindex.insert(temaiid, index="end", text=subtema["nombre"], open=False)
                    self.add_hymns_by_number(self.themeindex, subiid, subtema["rango"])
            else:
                temaiid = self.themeindex.insert("", index="end", text=tema["nombre"], open=True)
                self.add_hymns_by_number(self.themeindex, temaiid, tema["rango"])

    def setup_titleindex(self):
        self.titleindex = ttk.Treeview(self.indexframe, columns=("numeros",), height=25, show="tree",
                                       selectmode="none")
        self.titleindex.column("#0", width=200, minwidth=5, anchor="w", stretch=True)
        self.titleindex.column("numeros", width=10, minwidth=5, anchor="e", stretch=True)
        self.titleindex.grid(row=0, column=2, sticky="new", padx=(20, 0))
        self.titlescrollbar = ttk.Scrollbar(self.indexframe)
        self.titlescrollbar.config(command=self.titleindex.yview)
        self.titleindex.config(yscrollcommand=self.titlescrollbar.set)
        self.titlescrollbar.grid(row=0, column=3, sticky="nsw")

        normtitles = []
        himnos = dict()
        for title in self.indices["titulos"]:
            nt = Utils.normalizetxt(title)
            himnos[nt] = self.indices["titulos"][title]
            normtitles.append(nt)
        normtitles.sort()
        letter = ""
        lid = ""
        for nt in normtitles:
            newletter = nt[0]
            if newletter != letter:
                letter = nt[0]
                # self.titleindex.insert("", index="end")
                txt = "Letra {}".format(newletter.upper())
                lid = self.titleindex.insert("", index="end", text=txt, open=True)
            titulo = himnos[nt]["titulo"]
            n = int(himnos[nt]["numero"])
            self.titleindex.insert(lid, index="end", text=titulo, values=(n,))

    def add_hymns_by_number(self, tree: ttk.Treeview, iid: str, lim: list):
        for n in range(lim[0], lim[1] + 1):
            hymn = self.indices["numeros"][n]
            tree.insert(iid, index="end", text=hymn["titulo"], values=(n,))
