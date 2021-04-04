import tkinter as tk

hyllyt = {"A": [5, 3, [3, 3, 4]],
          "B": [3, 3, [3, 3, 3]],
          "C": [3, 3, [3, 3, 3]],
          "D": [3, 3, [3, 3, 3]],
          "E": [4, 2, [4, 4]]}

hylly_valinta = list(hyllyt.keys())
hylly_idx = 0
active_hylly = hylly_valinta[hylly_idx]


def next_hylly():
    hylly_idx = abs(65-ord(lbl_actv["text"]))
    hylly_idx += 1
    if hylly_idx == len(hylly_valinta):
        hylly_idx = 0
    lbl_actv["text"] = hylly_valinta[hylly_idx]


window = tk.Tk()
btn_fwd = tk.Button(master=window, text=">", command=next_hylly)
btn_fwd.pack()

lbl_actv = tk.Label(master=window, text=active_hylly)
lbl_actv.pack()

window.mainloop()
