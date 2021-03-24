from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from db_structures import Paikka, Valine

# Connect to the database using SQLAlchemy
engine = create_engine('sqlite:///test//db//test26.db', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
Base = declarative_base()
Base.metadata.create_all(engine)


def uusi_valine(session, ta_no, luokka, valine_nimi, paikka_lyhyt):
    # onko valine olemassa?
    valine = (
        session.query(Valine)
        .filter(Valine.ta_no == ta_no)
        .one_or_none()
        )
    if valine is not None:
        return
    else:
        valine = Valine(ta_no=ta_no, valine_nimi=valine_nimi)

    # etsi paikka lyhytnimestä
    paikka = (
        session.query(Paikka)
        .filter(Paikka.lyhytnimi == paikka_lyhyt)
        .one_or_none()
        )
    if paikka is None:
        return
    else:
        print(f"paikka {paikka.lyhytnimi} löytyy")
        paikka.valineet.append(valine)

    valine.paikka = paikka
    valine.active = 1
    print("uusi väline luotu ja varastoitu ",
          valine.paikka.lyhytnimi, valine.ta_no)
    session.add(valine)
    return valine


v = uusi_valine(session, "TA181210210", "181210", "Modux480 uusi", "A002")
session.commit()
