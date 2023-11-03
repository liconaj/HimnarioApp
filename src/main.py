from finder import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        st.make_dpi_aware()
        width, height = 800, 700
        self.title("Himnario Adventista")
        self.geometry(f"{width}x{height}")
        self.minsize(width, height)
        self.iconbitmap(f"{st.DATA_DIR}/icon.ico")
        self.protocol("WM_DELETE_WINDOW", self._exit)
        self.settings = st.Settings(self)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.finder = Finder(self.settings)
        self.finder.pack(fill="both", expand=True)
        self.settingsui = st.SettingsUI(self, self.settings)
        self.notebook.add(self.finder, text="Buscar")
        self.notebook.add(self.settingsui, text="Ajustes")

    def _exit(self) -> None:
        self.settings.save()
        self.quit()


if __name__ == "__main__":
    app = App()
    app.mainloop()
