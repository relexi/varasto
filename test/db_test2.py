from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db_structures import Paikka, Valine, Luokka

# Connect to the database using SQLAlchemy
engine = create_engine('sqlite:///test//db//test37.db', echo=False)
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
        valine = Valine(ta_no=ta_no, nimi=valine_nimi)

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
    paikka = (
        session.query(Paikka)
        .filter(Paikka.lyhytnimi == paikka_lyhyt)
        .one_or_none()
    )
    for valine in paikka.valineet:
        print(valine.ta_no, valine.luokka_id, valine.nimi)


def etsi_valine(session, ta_no):
    valine = (
        session.query(Valine)
        .filter(ta_no == Valine.ta_no)
        .one_or_none()
    )
    print(valine.paikka.lyhytnimi)


v = uusi_valine(session, "TA181210222", "181210", "Modux480 vanha", "A000")
v = uusi_valine(session, "TA181210210", "181210", "Modux480 vanha", "A001")
v = uusi_valine(session, "TA181210555", "181210", "Modux480 uusi", "A001")
v = uusi_valine(session, "20184711", "181210", "Modux480 uusi", "A002")
v = uusi_valine(session, "TA043306789", "043306",
                         "Carital Optima EZ 90", "A010")
v = uusi_valine(session, "2100900", "043306", "Carital Optima 80 uusi", "A010")
v = uusi_valine(session, "TA043306666", "043306", "Quattro +3T 76", "A011")
v = uusi_valine(session, "TA043306700", "043306",
                         "Carital Optima EZ 80", "A012")

valine_paikalla(session, "A001")
etsi_valine(session, "TA181210555")
session.commit()
