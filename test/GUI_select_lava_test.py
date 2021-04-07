"""
hier proibiere ich die Möglichkeiten von tkinter für die Projekt-GUI aus
zu Beginn eine Visualisierung der Regale mit Auswahlmöglichkeit der Plätze
"""

import tkinter as tk
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from functions import etsi_paikka, valine_paikalla

# Connect to the database using SQLAlchemy
engine = create_engine('sqlite:///test//db//test48.db', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
Base = declarative_base()
Base.metadata.create_all(engine)


# Hylly parametrit
# start with hylly A
hyllyt = {"A": [5, 3, [3, 3, 4]],
          "B": [3, 3, [3, 3, 3]],
          "C": [3, 3, [3, 3, 3]],
          "D": [3, 3, [3, 3, 3]],
          "E": [4, 2, [4, 4]]}

hylly_valinta = list(hyllyt.keys())
# start with hylly A
hylly_idx = 0
active_hylly = hylly_valinta[hylly_idx]

# värikoodit
varit = {"181210": "green",
         "043306": "yellow"}


def select_lava(pos):
    print(pos)


def next_hylly():
    # get the actual "hylly" from the label set earlier
    hylly_idx = abs(65-ord(lbl_actv["text"][6]))
    hylly_idx += 1
    if hylly_idx == len(hylly_valinta):
        hylly_idx = 0
    hylly = hylly_valinta[hylly_idx]
    lbl_actv["text"] = "hylly "+hylly
    nayta_hylly(hylly)


def prev_hylly():
    hylly_idx = abs(65-ord(lbl_actv["text"][6]))
    hylly_idx -= 1
    if hylly_idx < 0:
        hylly_idx = len(hylly_valinta)-1
    hylly = hylly_valinta[hylly_idx]
    lbl_actv["text"] = "hylly "+hylly
    nayta_hylly(hylly)


def displ_lava(pos):
    lbl_info_popup = tk.Label(master=frm_info, text="", bg="white")
    lbl_info_popup.grid(row=0, column=0)

    paikka = etsi_paikka(session, pos)
    if paikka.valineet is not []:
        for valine in paikka.valineet:
            print(valine.ta_no)
            lbl_info_popup["text"] += valine.ta_no + " " + valine.nimi + "\n"


def displ_nix(e):
    lbl = frm_info.winfo_children()
    for label in lbl:
        label.destroy()


def uusi_valine():
    frm_uusi_valine = tk.Frame(frm_info)
    ent_ta_no = tk.Entry(frm_uusi_valine, text="vTam ")
    frm_uusi_valine.grid(row=0, column=1)
    frm_uusi_valine.columnconfigure(0, minsize=100)
    ent_ta_no.grid(row=0, column=0)


def nayta_hylly(hylly):
    tasot = hyllyt[hylly][0]
    valit = hyllyt[hylly][1]
    lavat = hyllyt[hylly][2]

    # erase old content first
    widget_list = frm_hylly.winfo_children()
    for i in range(len(widget_list)):
        child = widget_list[i]
        child.destroy()
    # then build the shelfs
    for vali in range(valit):
        framek = tk.Frame(
            master=frm_hylly,
            relief=tk.RIDGE,
            padx=20, pady=20,
            borderwidth=2
        )
        framek.grid(row=1, column=vali, sticky="s")

        for t in range(tasot):
            taso = tasot-t-1
            for lava in range(lavat[vali]):
                txt_pos = hylly+str(vali)+str(taso)+str(lava)
                frame = tk.Frame(
                    master=framek,
                    relief=tk.RAISED,
                    borderwidth=1,
                    padx=20, pady=20,
                    highlightbackground="white",
                    highlightthickness=5
                )
                frame.grid(row=t, column=lava, padx=8, pady=8)
                list_valineet = valine_paikalla(session, txt_pos)

                for valine in list_valineet:
                    if valine.luokka.luokka_id == "181210":
                        frame["highlightbackground"] = "green"

                label = tk.Label(master=frame, text=txt_pos)
                label.pack()
                label.bind("<Button-1>", lambda e,
                           pos=hylly+str(vali)+str(taso)+str(lava):
                           select_lava(pos))
                label.bind("<Enter>", lambda e,
                           pos=hylly+str(vali)+str(taso)+str(lava):
                           displ_lava(pos))
                label.bind("<Leave>", displ_nix)


window = tk.Tk()
window.title("varasto")
window.rowconfigure(0, minsize=700, weight=1)
window.rowconfigure(1, minsize=200, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

frm_menu = tk.Frame(window, relief=tk.RAISED, bd=2)
frm_menu.columnconfigure(1, minsize=100, weight=1)
frm_oikea = tk.Frame(window)
frm_oikea.rowconfigure(0, minsize=500, weight=1)
frm_oikea.rowconfigure(1, minsize=200, weight=1)

frm_info = tk.Frame(frm_oikea, relief=tk.RAISED, bd=2)
frm_hylly = tk.Frame(frm_oikea, relief=tk.RAISED, bd=2)

btn_fwd = tk.Button(frm_menu, text=">", command=next_hylly)
btn_ret = tk.Button(frm_menu, text="<", command=prev_hylly)
lbl_actv = tk.Label(frm_menu, text="hylly "+active_hylly)
btn_uusi_v = tk.Button(frm_menu, text="uusi väline", command=uusi_valine)

lbl_actv.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
btn_ret.grid(row=0, column=0, sticky="w", padx=5)
btn_fwd.grid(row=0, column=2, sticky="e", padx=5)
btn_uusi_v.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5)

frm_menu.grid(row=0, column=0, sticky="ns")
frm_oikea.grid(row=0, column=1, sticky="ns")
frm_hylly.grid(row=0, column=0, sticky="ns")
frm_info.grid(row=1, column=0, sticky="nsew")

nayta_hylly(active_hylly)

window.mainloop()
