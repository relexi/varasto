# hier proibiere ich die Möglichkeiten von tkinter für die Projekt-GUI aus
# zu Beginn eine Visualisierung der Regale mit Auswahlmöglichkeit der Plätze

import tkinter as tk


def select_lava(pos):
    # selected = hylly + vali + taso + lava
    print(pos)


def nayta_hylly(hylly):
    """
    graphic display of the shelf provided in the parameter

    Args:
        hylly (str):

    """
    # Hylly parametrit
    hyllyt = {"A": [3, 5, [3, 3, 4]],
              "B": [3, 3, [3, 3, 3]],
              "C": [3, 3, [3, 3, 3]],
              "D": [3, 3, [3, 3, 3]],
              "E": [2, 4, [4, 4]]}

    valit = hyllyt[hylly][0]
    tasot = hyllyt[hylly][1]
    lavat = hyllyt[hylly][2]

    window_title = f"hylly {hylly}"
    window = tk.Tk()
    window.title(window_title)

    for vali in range(valit):
        framek = tk.Frame(
            master=window,
            relief=tk.RIDGE,
            padx=20, pady=20,
            borderwidth=2
        )
        framek.grid(row=0, column=vali)

        for t in range(tasot):
            taso = tasot-t-1
            for lava in range(lavat[vali]):
                frame = tk.Frame(
                    master=framek,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                frame.grid(row=t, column=lava, padx=5, pady=5)
                label = tk.Label(master=frame,
                                 text=f"väli {vali}\ntaso {taso}\nlava {lava}")
                label.pack()
                label.bind("<Button-1>", lambda e,
                           pos=hylly+str(vali)+str(taso)+str(lava):
                           select_lava(pos))

    window.mainloop()


nayta_hylly("A")
