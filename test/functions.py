from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db_structures import Paikka, Valine, Luokka, Tapahtuma, Tapahtuma_Luokka
from datetime import datetime


# Connect to the database using SQLAlchemy
engine = create_engine('sqlite:///test//db//test48.db', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
Base = declarative_base()
Base.metadata.create_all(engine)


def nyt_tapahtuu(session, valine, paikka, luokka, kuvaus):
    # first create a new tapahtuma
    tapa = Tapahtuma(tapahtunut=datetime.now())
    # search for the correspondung tapahtuma_luokka
    tapa_luokka = (
        session.query(Tapahtuma_Luokka)
        .filter(Tapahtuma_Luokka.tapaht_kuvaus == luokka)
        .one_or_none()
    )
    if tapa_luokka is None:
        return
    # create cross-references from tables valine and tapahtuma_luokka
    valine.tapahtumat.append(tapa)
    tapa_luokka.tapahtumat_luokassa.append(tapa)

    # add valine and additional info to this tapahtuma and
    # add it to the db
    tapa.paikka = paikka
    tapa.valine = valine
    tapa.tapaht_kuvaus = kuvaus
    session.add(tapa)
    return tapa


def varastoi_valine(session, valine_ta_no, paikka_lyhyt, varasto_info):
    # etsi paikka lyhytnimestä
    valine = etsi_valine(session, valine_ta_no)
    if valine is None:
        return

    paikka = etsi_paikka(session, paikka_lyhyt)
    if paikka is None:
        return
    else:
        # do not allow to store the same valine again
        if valine in paikka.valineet:
            print(f"väline {valine.ta_no} on jo varastoitu \
                paikalle {paikka.lyhytnimi}")
            return
        else:
            paikka.valineet.append(valine)
            valine.active = 1
            nyt_tapahtuu(session, valine, paikka, "sisään", varasto_info)
    return valine


def varastosta_valine(session, valine_ta_no, varasto_info):
    # etsi paikka lyhytnimestä
    valine = etsi_valine(session, valine_ta_no)
    if valine is None:
        return
    # log this event
    nyt_tapahtuu(session, valine, valine.paikka, "ulos", varasto_info)
    # remove valine from paikka
    valine.paikka.valineet.remove(valine)
    # and set it inactive
    valine.active = 0
    session.commit
    return valine


def uusi_valine(session, ta_no, luokka_no, valine_nimi):
    # onko valine olemassa?
    valine = etsi_valine(session, ta_no)
    if valine is not None:
        print(f"Väline {ta_no} on jo olemassa - ei luotu")
        return
    else:
        valine = Valine(ta_no=ta_no, nimi=valine_nimi)

    # etsi luokka numerosta
    luokka = (
        session.query(Luokka)
        .filter(Luokka.luokka_id == luokka_no)
        .one_or_none()
    )
    if luokka is None:
        print(f"Luokka {luokka_no} ei löytynyt")
        return
    else:
        luokka.valineet_luokassa.append(valine)

    # write new tapahtuma into db for creation of valine
    nyt_tapahtuu(session, valine, None, "uusi", "Väline luotu")

    # assign properties to valine-object and store it to the db
    valine.luokka = luokka
    valine.active = 0  # intitially valine is not active
    session.add(valine)
    session.commit()
    return valine


def valine_paikalla(session, paikka_lyhyt):
    paikka = etsi_paikka(session, paikka_lyhyt)
    return paikka.valineet


def etsi_valine(session, ta_no):
    valine = (
        session.query(Valine)
        .filter(Valine.ta_no == ta_no)
        .one_or_none()
    )
    return valine


def etsi_paikka(session, paikka_lyhyt):
    paikka = (
        session.query(Paikka)
        .filter(Paikka.lyhytnimi == paikka_lyhyt)
        .one_or_none()
    )
    return paikka


"""v = uusi_valine(session, "TA181210222", "181210", "Modux480 vanha")
v = uusi_valine(session, "TA181210210", "181210", "Modux480 vanha")
v = uusi_valine(session, "TA181210555", "181210", "Modux480 uusi")
v = uusi_valine(session, "20184711", "181210", "Modux480 uusi")
v = uusi_valine(session, "TA043306789", "043306", "Carital Optima EZ 90")
v = uusi_valine(session, "2100900", "043306", "Carital Optima 80 uusi")
v = uusi_valine(session, "TA043306666", "043306", "Quattro +3T 76")
v = uusi_valine(session, "TA043306700", "043306", "Carital Optima EZ 80")

v = varastoi_valine(session, "TA181210222", "A000", "Irmeli käski")
v = varastoi_valine(session, "TA181210210", "A000", "puskurivarastoon")
v = varastoi_valine(session, "TA181210555", "A001", "no niin")
v = varastoi_valine(session, "20184711", "A002", "jotain")
v = varastoi_valine(session, "2100900", "E010", "jotain muuta")
v = varastoi_valine(session, "TA043306666", "E010", "vain siksi")
"""

v = etsi_valine(session, "TA181210222")
for vt in v.tapahtumat:
    print(vt.ta_no, vt.luokka.tapaht_kuvaus,
          vt.tapaht_kuvaus, vt.tapahtunut)

"""vkaks = etsi_valine(session, "2100900")
paikka = etsi_paikka(session, "B111")
vkaks.varastosta()
"""

# v = varastoi_valine(session, "TA043306666", "E010", "vain uudestaan")
# varastosta_valine(session, "TA181210222", "poistoon")
session.commit()
