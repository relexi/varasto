"""
hier proibiere ich die Möglichkeiten von tkinter für die Projekt-GUI aus
zu Beginn eine Visualisierung der Regale mit Auswahlmöglichkeit der Plätze
"""

import tkinter as tk

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
    # selected = hylly + taso + vali + lava
    print(pos)


def next_hylly():
    hylly_idx = abs(65-ord(lbl_actv["text"]))
    hylly_idx += 1
    if hylly_idx == len(hylly_valinta):
        hylly_idx = 0
    hylly = hylly_valinta[hylly_idx]
    lbl_actv["text"] = hylly
    nayta_hylly(hylly)


def displ_lava(pos):
    pass


def displ_nix():
    pass


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
                    borderwidth=1
                )
                frame.grid(row=t, column=lava, padx=8, pady=8)
                label = tk.Label(master=frame,
                                 text=f"taso {taso}\nväli {vali}\nlava {lava}")
                label.pack()
                label.bind("<Button-1>", lambda e,
                           pos=hylly+str(taso)+str(vali)+str(lava):
                           select_lava(pos))
                label.bind("<Enter>", lambda e,
                           pos=hylly+str(taso)+str(vali)+str(lava):
                           displ_lava(pos))
                label.bind("<Leave>", displ_nix)


window = tk.Tk()
window.columnconfigure(0, minsize=500)
window.rowconfigure([0, 1], minsize=100)
frm_menu = tk.Frame(master=window)
frm_menu.columnconfigure([0, 1, 2], minsize=200)
frm_hylly = tk.Frame(master=window)
frm_select = tk.Frame(master=frm_menu, bg="blue")
frm_selected = tk.Frame(master=frm_menu, bg="green")

frm_menu.grid(row=0, column=0)
frm_hylly.grid(row=1, column=0)
frm_select.grid(row=0, column=0, sticky="w")
frm_selected.grid(row=0, column=2, sticky="e")

btn_fwd = tk.Button(master=frm_select, text=">", command=next_hylly)
lbl_actv = tk.Label(master=frm_selected, text=active_hylly)

lbl_actv.grid(row=0, column=0)
btn_fwd.grid(row=0, column=0)


nayta_hylly(active_hylly)

window.mainloop()
