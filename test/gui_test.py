import tkinter as tk
from tkinter import ttk
import functions
LARGE_FONT = ("Verdana", 12)


class Oikea(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.parent = parent
        self.rowconfigure(0, weight=1, minsize=30)
        self.columnconfigure(1, weight=1, minsize=200)
        self.grid()

    def clear(self):
        labels = self.winfo_children()
        for lbl in labels:
            lbl.destroy()


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
        self.root.columnconfigure(1, minsize=300)
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


class Tulos(Oikea):
    def __init__(self, parent, title, sisalto):
        # clear first
        parent.clear()  # usually parent is of class Oikea
        self.title = title
        self.sisalto = sisalto
        print(type(sisalto))
        print(sisalto)
        for item in sisalto:
            self.lbl_ta = ttk.Label(
                parent,
                text=f"{item.ta_no}"
                ).grid(row=sisalto.index(item), column=0)
            self.lbl_nimi = ttk.Label(
                parent,
                text=f"{item.nimi}"
                ).grid(row=sisalto.index(item), column=1)
            self.lbl_paikka = ttk.Label(
                parent,
                text=f"{item.paikka.lyhytnimi}"
                ).grid(row=sisalto.index(item), column=2)


if __name__ == "__main__":
    # read configuration from ini-file
    str_cfg_file = "test//varasto_cfg.ini"
    cfg = functions.Config(str_cfg_file)
    # establish session to db with info from cfg-file
    session = cfg.session
    print(dir(session))
    fields = {"hakusana": "TA1812102"}
    window_root = tk.Tk()
    oikea = Oikea(window_root)
    loyto = functions.etsi_jotain(session, fields)
    frame = Tulos(oikea, "löytyi:", loyto)
    window_root.mainloop()
