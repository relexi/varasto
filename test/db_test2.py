from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db_structures import Paikka, Valine, Luokka

# Connect to the database using SQLAlchemy
engine = create_engine('sqlite:///test//db//test31.db', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
Base = declarative_base()
Base.metadata.create_all(engine)


def uusi_valine(session, ta_no, luokka_no, valine_nimi, paikka_lyhyt):
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

    # etsi luokka numerosta
    luokka = (
        session.query(Luokka)
        .filter(Luokka.luokka_id == luokka_no)
        .one_or_none()
    )
    if luokka is None:
        return
    else:
        print(f"luokka {luokka_no} löytyy")
        luokka.valineet_luokassa.append(valine)

    # assign properties to object and store it to the db
    valine.paikka = paikka
    valine.luokka = luokka
    valine.active = 1
    print("uusi väline luotu ja varastoitu ",
          valine.paikka.lyhytnimi, valine.ta_no)
    session.add(valine)
    return valine


def valine_paikalla(session, paikka_lyhyt):
    valineet = (
        session.query(Valine)
        .filter(Paikka.lyhytnimi == paikka_lyhyt)
        .all()
    )

    for valine in valineet:
        print(valine.ta_no, valine.va_paikka_id)


# v = uusi_valine(session, "TA181210255", "181210", "Modux480 vanha", "A000")
valine_paikalla(session, "A002")
session.commit()
