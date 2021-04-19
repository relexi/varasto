import tkinter as tk
from tkinter import ttk
LARGE_FONT = ("Verdana", 12)


def funct_caller(returnfields):
    print(returnfields)


class Vasen(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.parent = parent
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(sticky="nw")


class Oikea(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.parent = parent
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1, minsize=300)
        self.grid()


class Menu(Vasen):
    def __init__(self, parent, entries):
        tk.Frame.__init__(self)
        self.root = tk.Frame()
        self.parent = parent
        self.root.columnconfigure(0, minsize=100)
        self.root.grid(row=0, sticky="nw", padx=10, pady=20)
        for key, value in entries.items():
            self.key = ttk.Button(self.root,
                                  text=key,
                                  command=value)
            self.key.grid()


class Kysely(Oikea):
    def __init__(self, parent, title, fields, callback):

        def full_return(entry_fields):
            returnfields = {}
            for field in entry_fields:
                if str(field["text"]) in (fields):
                    returnfields.update({field["text"]: field.get()})
            self.returnfields = returnfields
            callback(returnfields)

        self.title = title
        self.fields = fields
        self.parent = parent
        self.callback = callback
        self.root = tk.Frame(self.parent)
        self.root.columnconfigure(0, minsize=200)
        self.root.grid(padx=10, pady=20)
        self.lbl_title = ttk.Label(self.root,
                                   text=title,
                                   font=LARGE_FONT).grid(
            row=0, columnspan=2, sticky="ew"
        )
        self.entry_fields = []
        idx = 1
        for field in fields:
            lbl = ttk.Label(self.root, text=f"{field} :")
            ent = ttk.Entry(self.root, text=field)
            self.entry_fields.append(ent)
            lbl.grid(row=idx, column=0, sticky="nw", padx=20, pady=5)
            ent.grid(row=idx, column=1, sticky="nwe", padx=20, pady=5)
            idx += 1

        btn_tallenna = ttk.Button(self.root,
                                  text="Tallenna",
                                  command=lambda entry=self.entry_fields:
                                  full_return(entry))
        btn_tallenna.grid(row=idx, column=1, sticky="se", padx=20, pady=10)
        btn_peruuta = ttk.Button(self.root,
                                 text="Peruuta",
                                 command=self.root.destroy)
        btn_peruuta.grid(row=idx, column=0, sticky="sw", padx=20, pady=10)


class MainApplication(tk.Frame):

    def uusi_valine(self):
        fields = ["vtam", "luokka", "nimi", "huom", "paikka"]
        Kysely(main.oikea, "uusi väline", fields, funct_caller)

    def etsi_valine(self):
        pass

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.vasen = Vasen(self)
        self.oikea = Oikea(self)
        self.vasen.grid(row=0, column=0)
        self.oikea.grid(row=0, column=1)

        self.columnconfigure(0, minsize=100, weight=1)
        self.columnconfigure(1, minsize=300, weight=1)
        self.rowconfigure(0, minsize=200, weight=1)

        menu_entries = {"uusi väline": self.uusi_valine,
                        "etsi väline": self.etsi_valine}
        Menu(self.vasen, menu_entries)


if __name__ == "__main__":
    root = tk.Tk()
    main = MainApplication(root)
    main.grid(row=0, column=0, sticky="nsew")
    root.mainloop()
