import tkinter as tk
from tkinter import ttk
LARGE_FONT = ("Verdana", 12)


class Kysely:
    def __init__(self, parent, title, fields):

        def full_return(entry_fields):
            returnfields = {}
            for field in entry_fields:
                if str(field["text"]) in (fields):
                    returnfields.update({field["text"]: field.get()})
            self.returnfields = returnfields

        self.title = title
        self.fields = fields
        self.parent = parent
        self.root = tk.Frame(self.parent)
        self.root.columnconfigure(1, minsize=200)
        self.root.pack(padx=10, pady=20)
        self.lbl_title = tk.Label(self.root, text=title, font=LARGE_FONT).grid(
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


if __name__ == "__main__":
    fields = ["TreVtam", "luokka", "nimi", "huomautus", "paikka"]
    window_root = tk.Tk()
    frame = Kysely(window_root, "uusi väline", fields)
    window_root.mainloop()
