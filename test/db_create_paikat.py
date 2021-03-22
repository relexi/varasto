"""
Dieses Programm füllt die Datenbank mit den Pallettenplätzen
der Status der Plätze ist standardmässig active = 0
"""


from sqlalchemy import create_engine
from db_structures import Paikka
from sqlalchemy.orm import sessionmaker


# connect to the database through SQLAlchemy
engine = create_engine('sqlite:///test/test14.db', echo=True)
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()


def add_paikka(session, hylly, taso, vali, lava):
    """
    this function adds a new row into the table paikka
    and sets its status active = 0

    parameters: session (db-connection), hylly (String), taso (Integer),
    vali (Integer), lava (Integer)
    """

    lyhytnimi = hylly + str(taso) + str(vali) + str(lava)
    paikka = Paikka(lyhytnimi=lyhytnimi, hylly=hylly, taso=taso, vali=vali,
                    lava=lava, active=0)

    print(paikka.lyhytnimi)
    session.add(paikka)


# Hylly parametrit
hyllyt = {"A": [5, 3, [3, 3, 4]],
          "B": [3, 3, [3, 3, 3]],
          "C": [3, 3, [3, 3, 3]],
          "D": [3, 3, [3, 3, 3]],
          "E": [4, 2, [4, 4]]}

for hylly, elem in hyllyt.items():
    tasot = hyllyt[hylly][0]
    valit = hyllyt[hylly][1]
    lavat = hyllyt[hylly][2]

    for vali in range(valit):
        for t in range(tasot):
            taso = tasot-t-1
            for lava in range(lavat[vali]):
                add_paikka(session, hylly, taso, vali, lava)

session.commit()
