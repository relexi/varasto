"""
hier proibiere ich die Möglichkeiten von tkinter für die Projekt-GUI aus
zu Beginn eine Visualisierung der Regale mit Auswahlmöglichkeit der Plätze
"""

import tkinter as tk
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from functions import etsi_paikka

# Connect to the database using SQLAlchemy
engine = create_engine('sqlite:///test//db//test47.db', echo=False)
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


def select_lava(pos):
    print(pos)


def next_hylly():
    # get the actual "hylly" from the label set earlier
    hylly_idx = abs(65-ord(lbl_actv["text"]))
    hylly_idx += 1
    if hylly_idx == len(hylly_valinta):
        hylly_idx = 0
    hylly = hylly_valinta[hylly_idx]
    lbl_actv["text"] = hylly
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


def nayta_hylly(hylly):
    tasot = hyllyt[hylly][0]
    valit = hyllyt[hylly][1]
    lavat = hyllyt[hylly][2]

    window_title = f"hylly {hylly}"
    window.title(window_title)
    # in case there is alread something: erase it
    widget_list = frm_hylly.winfo_children()
    for i in range(len(widget_list)):
        child = widget_list[i]
        child.destroy()

    for vali in range(valit):
        framek = tk.Frame(
            master=frm_hylly,
            relief=tk.RIDGE,
            padx=20, pady=20,
            borderwidth=2
        )
        framek.grid(row=1, column=vali)

        for t in range(tasot):
            taso = tasot-t-1
            for lava in range(lavat[vali]):
                frame = tk.Frame(
                    master=framek,
                    relief=tk.RAISED,
                    borderwidth=1,
                    padx=20, pady=20
                )
                frame.grid(row=t, column=lava, padx=8, pady=8)
                txt_pos = hylly+str(vali)+str(taso)+str(lava)
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
window.columnconfigure(0, minsize=500)
window.rowconfigure([0, 1], minsize=100)
frm_menu = tk.Frame(master=window)
frm_menu.columnconfigure([0, 1, 2], minsize=200)
frm_hylly = tk.Frame(master=window)
frm_select = tk.Frame(master=frm_menu, bg="blue")
frm_info = tk.Frame(master=frm_menu)
frm_selected = tk.Frame(master=frm_menu, bg="green")

frm_menu.grid(row=0, column=0)
frm_hylly.grid(row=1, column=0)
frm_info.grid(row=0, column=1)
frm_select.grid(row=0, column=0, sticky="w")
frm_selected.grid(row=0, column=2, sticky="e")

btn_fwd = tk.Button(master=frm_select, text=">", command=next_hylly)
lbl_actv = tk.Label(master=frm_selected, text=active_hylly)

lbl_actv.grid(row=0, column=0)
btn_fwd.grid(row=0, column=0)

nayta_hylly(active_hylly)

window.mainloop()
