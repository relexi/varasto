import tkinter as tk
from tkinter import ttk
import functions
from db_structures import Hyllyt

LARGE_FONT = ("Verdana", 12)


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
        self.columnconfigure(0, weight=1)
        self.grid()

    def clear(self):
        labels = self.winfo_children()
        for lbl in labels:
            lbl.destroy()


class Menu(Vasen):
    def __init__(self, parent, entries):
        tk.Frame.__init__(self)
        self.root = tk.Frame()
        self.parent = parent
        # self.root.columnconfigure(0, minsize=50)
        self.root.grid(row=0, sticky="nw")
        self.hylly_valinta = ("A", "B", "C", "D", "E")
        self.active_hylly = "A"

        def next_hylly():
            # get the actual "hylly" from the label set earlier
            hylly_idx = abs(65-ord(btn_actv["text"][6]))
            hylly_idx += 1
            if hylly_idx == len(self.hylly_valinta):
                hylly_idx = 0
            hylly = self.hylly_valinta[hylly_idx]
            btn_actv["text"] = "hylly "+hylly
            nayta_hylly(hylly)

        def prev_hylly():
            hylly_idx = abs(65-ord(btn_actv["text"][6]))
            hylly_idx -= 1
            if hylly_idx < 0:
                hylly_idx = len(self.hylly_valinta)-1
            hylly = self.hylly_valinta[hylly_idx]
            btn_actv["text"] = "hylly "+hylly
            nayta_hylly(hylly)

        def nayta_hylly(hylly):
            hyllynaytto = Hyllynaytto(main.oikea, hylly)
            print(hyllynaytto)

        # create the shelf-display menu on top of all other
        btn_fwd = ttk.Button(self.root, text=">", command=next_hylly)
        btn_ret = ttk.Button(self.root, text="<", command=prev_hylly)
        btn_actv = ttk.Button(self.root,
                              text="hylly "+self.active_hylly,
                              command=lambda: nayta_hylly(self.active_hylly))

        btn_ret.grid(row=0, column=0, sticky="w")
        btn_fwd.grid(row=0, column=1, sticky="e")
        btn_actv.grid(row=1, column=0, columnspan=2,
                      sticky="ew")

        # create "normal" menu entries from dictionary entries
        for key, value in entries.items():
            self.key = ttk.Button(self.root,
                                  text=key,
                                  command=value)
            self.key.grid(columnspan=2, sticky="ew")


class Hyllynaytto(Oikea):
    def __init__(self, parent, hylly):
        parent.clear()

        self.parent = parent
        self.hyllyt = {}
        self.active_hylly = hylly
        self.hyllyt = {}
        for int_h in range(65, 90):
            hylly = (
                session.query(Hyllyt)
                .filter(Hyllyt.hylly == chr(int_h))
                .one_or_none())
            if hylly:
                hy = hylly.hylly
                tasot = int(hylly.tasot)
                valit = int(hylly.valit)
                lavat = hylly.lavat.split()
                lavat = [int(lava) for lava in lavat]
                self.hyllyt[hy] = [tasot, valit, lavat]

        # tasot = int(self.hyllyt[self.active_hylly][0])
        # valit = int(self.hyllyt[self.active_hylly][1])
        # lavat = self.hyllyt[self.active_hylly][2].split()
        # int_lavat = [int(item) for item in lavat]

        hylly = self.active_hylly
        tasot = self.hyllyt[self.active_hylly][0]
        valit = self.hyllyt[self.active_hylly][1]
        lavat = self.hyllyt[self.active_hylly][2]

        for vali in range(valit):
            framek = tk.Frame(
                master=parent,
                relief=tk.RIDGE,
                padx=20, pady=20,
                borderwidth=2
            )
            framek.grid(row=1, column=vali, sticky="s")

            for t in range(tasot):
                taso = tasot-t-1
                for lava in range(lavat[vali]):
                    txt_pos = hylly+str(taso)+str(vali)+str(lava)
                    frame = tk.Frame(
                        master=framek,
                        relief=tk.RAISED,
                        borderwidth=1,
                        padx=20, pady=20,
                        highlightbackground="white",
                        highlightthickness=5
                    )
                    frame.grid(row=t, column=lava, padx=8, pady=8)
                    list_valineet = functions.valine_paikalla(session, txt_pos)
                    print(list_valineet)

                    label = tk.Label(master=frame, text=txt_pos)
                    label.pack()
                    label.bind("<Button-1>")
                    label.bind("<Enter>")
                    label.bind("<Leave>")


class Kysely(Oikea):
    def __init__(self, parent, title, fields, callback):
        # clear first
        parent.clear()  # usually parent is of class Oikea

        def full_return(entry_fields):
            returnfields = {}
            for field in entry_fields:
                if str(field["text"]) in (fields):
                    returnfields.update({field["text"]: field.get()})
            self.returnfields = returnfields
            result = callback(session, returnfields)
            if result:
                parent.clear()
                Tulos(parent, "tulos", result)

        self.title = title
        self.fields = fields
        self.parent = parent
        self.callback = callback
        self.root = tk.Frame(self.parent)
        self.root.columnconfigure(0, minsize=10)
        self.root.grid(padx=10, pady=10)
        self.lbl_title = ttk.Label(self.root,
                                   text=title,
                                   font=LARGE_FONT
                                   ).grid(
                                    columnspan=2, pady=10
                                   )
        self.entry_fields = []
        idx = 1
        for field in fields:
            self.lbl = ttk.Label(self.root, text=f"{field} :")
            self.ent = ttk.Entry(self.root, text=field)
            self.entry_fields.append(self.ent)
            self.lbl.grid(row=idx, column=0, sticky="nw", padx=20, pady=5)
            self.ent.grid(row=idx, column=1, sticky="nwe", padx=20, pady=5)
            idx += 1

        btn_tallenna = ttk.Button(
            self.root,
            text="Tallenna",
            command=lambda entry_fields=self.entry_fields:
            full_return(entry_fields)
            )
        btn_tallenna.grid(
            row=idx, column=1,
            sticky="se", padx=10, pady=10
            )
        btn_peruuta = ttk.Button(
            self.root,
            text="Peruuta",
            command=self.root.destroy
            )
        btn_peruuta.grid(
            row=idx, column=0,
            sticky="sw", padx=10, pady=10
            )


class Tulos(Oikea):
    def __init__(self, parent, title, sisalto):
        # clear first
        parent.clear()  # usually parent is of class Oikea
        self.title = title
        self.sisalto = sisalto
        try:  # is there a list of objects?
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
        except TypeError:  # only one object of type valine given
            self.lbl_ta = ttk.Label(
                parent,
                text=f"{sisalto.ta_no}"
                ).grid(row=0, column=0)
            self.lbl_nimi = ttk.Label(
                parent,
                text=f"{sisalto.nimi}"
                ).grid(row=0, column=1)
            self.lbl_paikka = ttk.Label(
                parent,
                text=f"{sisalto.paikka.lyhytnimi}"
                ).grid(row=0, column=2)


class MainApplication(tk.Frame):

    def uusi_valine(self):
        fields = ["TreVtam", "luokka", "nimi", "huom", "paikka"]
        Kysely(
            main.oikea,
            "uusi väline",
            fields,
            functions.uusi_valine)

    def etsi(self):
        fields = ["hakusana"]
        Kysely(
            main.oikea,
            "etsi väline(et)",
            fields,
            functions.etsi_jotain
        )

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.vasen = Vasen(self)
        self.oikea = Oikea(self)
        self.vasen.grid(row=0, column=0)
        self.oikea.grid(row=0, column=1)

        self.columnconfigure(0, minsize=10, weight=1)
        self.columnconfigure(1, minsize=10, weight=1)
        self.rowconfigure(0, weight=1)

        menu_entries = {"uusi väline": self.uusi_valine,
                        "etsi väline": self.etsi}
        Menu(self.vasen, menu_entries)


if __name__ == "__main__":
    # read configuration from ini-file
    str_cfg_file = "test//varasto_cfg.ini"
    cfg = functions.Config(str_cfg_file)
    # establish session to db with info from cfg-file
    session = cfg.session

    root = tk.Tk()
    main = MainApplication(root)
    main.grid()
    root.mainloop()
