"""
hier proibiere ich die Möglichkeiten von tkinter für die Projekt-GUI aus
zu Beginn eine Visualisierung der Regale mit Auswahlmöglichkeit der Plätze
"""

import tkinter as tk
from tkinter import ttk
import functions


str_cfg_file = "test//varasto_cfg.ini"
# read configuration from ini-file
# and use its class "Config"
cfg = functions.Config(str_cfg_file)
session = cfg.session
hyllyt = cfg.hyllyt
# start with hylly A
hylly_valinta = list(hyllyt.keys())
# start with hylly A
hylly_idx = 0
active_hylly = hylly_valinta[hylly_idx]

# värikoodit
varit = cfg.varit


def select_lava(pos):
    print(pos)


def next_hylly():
    # get the actual "hylly" from the label set earlier
    hylly_idx = abs(65-ord(btn_actv["text"][6]))
    hylly_idx += 1
    if hylly_idx == len(hylly_valinta):
        hylly_idx = 0
    hylly = hylly_valinta[hylly_idx]
    btn_actv["text"] = "hylly "+hylly
    nayta_hylly(hylly)


def prev_hylly():
    hylly_idx = abs(65-ord(btn_actv["text"][6]))
    hylly_idx -= 1
    if hylly_idx < 0:
        hylly_idx = len(hylly_valinta)-1
    hylly = hylly_valinta[hylly_idx]
    btn_actv["text"] = "hylly "+hylly
    nayta_hylly(hylly)


def displ_lava(pos):
    lbl_info_popup = tk.Label(master=frm_info, text="", bg="white")
    lbl_info_popup.grid(row=0, column=0)

    paikka = functions.etsi_paikka(session, pos)
    if paikka.valineet is not []:
        for valine in paikka.valineet:
            print(valine.ta_no)
            lbl_info_popup["text"] += valine.ta_no + " " + valine.nimi + "\n"


def displ_nix(frm):
    lbl = frm.winfo_children()
    for label in lbl:
        label.destroy()


def uusi_valine_gui(callback):
    # this function creates a new valine based on user input.

    """    def valine():
        val = functions.uusi_valine(
           session, ent_ta_no.get(), ent_luokka.get(), ent_kuvaus.get())
        paikka = functions.etsi_paikka(session, ent_paikka.get())
        paikka.valineet.append(val)
        val.active = 1
        functions.nyt_tapahtuu(session, val, paikka, "sisään",
                               "luotu ja varastoitu")
        session.commit()
    """

    fields = ["TreVtam", "luokka", "nimi", "huom", "paikka"]
    displ_nix(frm_hylly)
    functions.Kysely(frm_hylly, "uusi väline", fields, callback)


def nayta_hylly(hylly):
    valit = hyllyt[hylly][0]
    tasot = hyllyt[hylly][1]
    lavat = hyllyt[hylly][2]

    # erase old content first
    displ_nix(frm_hylly)

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
                list_valineet = functions.valine_paikalla(session, txt_pos)

                for valine in list_valineet:
                    str_luokka_id = valine.luokka.luokka_id
                    if str_luokka_id in varit:
                        frame["highlightbackground"] = varit[str_luokka_id]

                label = tk.Label(master=frame, text=txt_pos)
                label.pack()
                label.bind("<Button-1>", lambda e,
                           pos=hylly+str(vali)+str(taso)+str(lava):
                           select_lava(pos))
                label.bind("<Enter>", lambda e,
                           pos=hylly+str(vali)+str(taso)+str(lava):
                           displ_lava(pos))
                label.bind("<Leave>", lambda: displ_nix(frm_info))


window = tk.Tk()
window.title("varasto")
window.rowconfigure(0, minsize=800, weight=1)
window.rowconfigure(1, minsize=300, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

frm_menu = tk.Frame(window, relief=tk.RAISED, bd=2)

frm_menu.columnconfigure(0, minsize=100, weight=1)
frm_menu.rowconfigure(0, minsize=500, weight=1)
frm_menu.rowconfigure(1, minsize=300, weight=1)

frm_hyllymenu = tk.Frame(frm_menu, relief=tk.RAISED, bd=2)
frm_alamenu = tk.Frame(frm_menu, relief=tk.RAISED, bd=2)
frm_alamenu.columnconfigure(0, minsize=100, weight=1)
frm_hyllymenu.columnconfigure(1, minsize=80, weight=1)

frm_oikea = tk.Frame(window)
frm_oikea.rowconfigure(0, minsize=500, weight=1)
frm_oikea.rowconfigure(1, minsize=300, weight=1)
frm_oikea.columnconfigure(0, minsize=800, weight=1)

frm_info = tk.Frame(frm_oikea, relief=tk.RAISED, bd=2)
frm_hylly = tk.Frame(frm_oikea, relief=tk.RAISED, bd=2)

btn_fwd = ttk.Button(frm_hyllymenu, text=">", command=next_hylly)
btn_ret = ttk.Button(frm_hyllymenu, text="<", command=prev_hylly)
btn_actv = ttk.Button(frm_hyllymenu,
                      text="hylly "+active_hylly,
                      command=lambda: nayta_hylly(active_hylly)
                      )
btn_uusi_v = ttk.Button(frm_hyllymenu,
                        text="uusi väline",
                        command=lambda: uusi_valine_gui(
                            callback=functions.uusi_valine)
                        )

btn_ret.grid(row=0, column=0, sticky="w", padx=5)
btn_actv.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
btn_fwd.grid(row=0, column=2, sticky="e", padx=5)
btn_uusi_v.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5)


frm_hyllymenu.grid(row=0, column=0, sticky="nsew")
frm_alamenu.grid(row=1, column=0, sticky="nsew")
frm_menu.grid(row=0, column=0, sticky="ns")
frm_oikea.grid(row=0, column=1, sticky="nsw")
frm_hylly.grid(row=0, column=0, sticky="ns")
frm_info.grid(row=1, column=0, sticky="nsew")

nayta_hylly(active_hylly)

window.mainloop()
