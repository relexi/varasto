from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db_structures import Paikka, Valine, Luokka, Tapahtuma, Tapahtuma_Luokka
from datetime import datetime
import configparser
import tkinter as tk
from tkinter import ttk

str_cfg_file = "test//varasto_cfg.ini"
LARGE_FONT = ("Verdana", 12)


class Kysely:
    def __init__(self, parent, title, fields, callback):
        self.title = title
        self.fields = fields
        self.parent = parent

        self.root = tk.Frame(self.parent)
        self.root.columnconfigure(1, minsize=200)
        self.root.grid()
        self.lbl_title = tk.Label(self.root, text=title, font=LARGE_FONT).grid(
            row=0, columnspan=2, sticky="ew"
        )
        # read configuration from ini-file
        cfg = Config(str_cfg_file)
        # establish session to db with info from cfg-file
        session = cfg.session
        self.entry_fields = []
        idx = 1
        for field in fields:
            lbl = ttk.Label(self.root, text=f"{field} :")
            ent = ttk.Entry(self.root, text=field)
            self.entry_fields.append(ent)
            lbl.grid(row=idx, column=0, sticky="nw", padx=20, pady=5)
            ent.grid(row=idx, column=1, sticky="nwe", padx=20, pady=5)
            idx += 1

        btn_tallenna = ttk.Button(self.root,
                                  text="Tallenna",
                                  command=lambda entry=self.entry_fields:
                                  full_return(entry, callback))
        btn_tallenna.grid(row=idx, column=1, sticky="se", padx=20, pady=10)
        btn_peruuta = ttk.Button(self.root,
                                 text="Peruuta",
                                 command=self.root.destroy)
        btn_peruuta.grid(row=idx, column=0, sticky="sw", padx=20, pady=10)

        def full_return(entry_fields, callback):
            returnfields = {}
            for field in entry_fields:
                if str(field["text"]) in (fields):
                    returnfields.update({field["text"]: field.get()})
            callback(session, returnfields)


class Config:
    """
    Config provides the methods and attributes to read basic settings and
    settings for creation of the db from an ini-file
    Attributes:
        ini_file (string): given at init
        db_file: (string):
        session (SQLAlchemy session object)
        hyllyt (dict)
        luokat (dict)
        tapahtumaluokat (list)
    Args:
        ini_file (string): points to the config_ini-file
    Methods:
        db_connect(db_file): creates a SQLAlchemy connection to the db and
                             returns a session-object
        read_hyllyt(): builds the hyllyt-dictionary from the ini and returns it
        read_luokat(): builds the luokat-dictionary from the ini and returns it
        read_tapaht_luokat(): builds a list with tapahtuma-luokat from ini
                              and returns that
    """
    def __init__(self, ini_file):
        self.ini_file = ini_file

        def db_connect():
            # Connect to the database using SQLAlchemy
            engine = create_engine(f"sqlite:///{self.db_file}", echo=False)
            Session = sessionmaker()
            Session.configure(bind=engine)
            session = Session()
            Base = declarative_base()
            Base.metadata.create_all(engine)
            return session

        def read_hyllyt():
            # build the hyllyt-dictionary
            # hyllyt = {
            #           "A": [3, 5, [3, 3, 4]],
            #           "B": [3, 3, [3, 3, 3]],
            #           "C": [3, 3, [3, 3, 3]],
            #           "D": [3, 3, [3, 3, 3]],
            #           "E": [2, 4, [4, 4]]
            # }
            hyllyt = {}
            for (hylly, str_rivi) in cfg.items("varasto"):
                rivi = str_rivi.split(", ")
                int_rivi = [int(item) for item in rivi]
                valit = int_rivi[0]
                tasot = int_rivi[1]
                hylly = hylly.upper()
                lst_lavat = int_rivi[2:valit+2]
                lst_rivi = [valit, tasot, lst_lavat]
                hyllyt[hylly] = lst_rivi
            return hyllyt

        def read_luokat():
            # build luokat-dictionary
            # luokat = {
            #   "181210": "sängyt",
            #   "043306": "painehaavapatjat",
            #   "122203": "pyörätuolit"
            # }
            luokat = {}
            for (luokka_no, luokka_name) in cfg.items("luokat"):
                luokat[luokka_no] = luokka_name
            return luokat

        def read_varit():
            varit = {}
            for (luokka_no, vari) in cfg.items("varit"):
                varit[luokka_no] = vari
            return varit

        def read_tapaht_luokat():
            tapahtumaluokat = []
            for (luokka_no, luokka_name) in cfg.items("tapahtumaluokat"):
                tapahtumaluokat.append(luokka_name)
            return tapahtumaluokat

        # read config from ini-file
        cfg = configparser.ConfigParser()
        cfg.read(ini_file, 'UTF-8')
        # set attributes
        self.db_file = cfg.get('db', 'db_file')
        self.session = db_connect()
        self.hyllyt = read_hyllyt()
        self.luokat = read_luokat()
        self.tapahtumaluokat = read_tapaht_luokat()
        self.varit = read_varit()


def nyt_tapahtuu(session, valine, paikka, luokka, kuvaus="ei huom"):
    # first create a new tapahtuma
    tapa = Tapahtuma(tapahtunut=datetime.now())
    # search for the correspondung tapahtuma_luokka
    tapa_luokka = (
        session.query(Tapahtuma_Luokka)
        .filter(Tapahtuma_Luokka.tapaht_kuvaus == luokka)
        .one_or_none()
    )
    if tapa_luokka is None:
        # !log this!
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
        print("varastoi_väline - väline ei löytynyt")
        return

    paikka = etsi_paikka(session, paikka_lyhyt)
    if paikka is None:
        print("varastoi_väline - paikka ei löytynyt")
        return
    else:
        # do not allow to store the same valine again
        if valine in paikka.valineet:
            print("varastoi_väline - väline on jo paikalla")
            return
        else:
            paikka.valineet.append(valine)
            valine.active = 1
            nyt_tapahtuu(session, valine, paikka, "sisään", varasto_info)
            session.commit()
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


def uusi_valine(session, fields):
    # decode parameters from fields:
    # {'TreVtam': 'TA181210255', 'luokka': '181210',
    # 'nimi': 'Modux', 'huom': 'nix!', 'paikka': 'A021'}
    ta_no = fields["TreVtam"]
    luokka_no = fields["luokka"]
    valine_nimi = fields["nimi"]
    huom = fields["huom"]
    paikka = fields["paikka"]

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

    if huom:
        valine.huomautus = huom

    # write new tapahtuma into db for creation of valine
    nyt_tapahtuu(session, valine, None, "uusi", "väline luotu")

    # assign properties to valine-object and store it to the db
    valine.luokka = luokka
    valine.active = 0  # intitially valine is not active
    session.add(valine)
    session.commit()

    # if paikka is given, then store valine to paikka
    if paikka is not None:
        varastoi_valine(session, ta_no, paikka, "väline varastoitu")
        print("valine varastoitu paikalle", paikka)
    else:
        print("paikka ei ole tiedossa")

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
    return valine  # is of type Valine


def etsi_jotain(session, fields):
    # decode hakusana from fields
    hakusana = fields["hakusana"]

    loyto = (
        session.query(Valine)
        .filter(Valine.ta_no.ilike("%"+hakusana+"%"))
        .all()
    )
    return loyto  # returns a list of Valine


def etsi_paikka(session, paikka_lyhyt):
    paikka = (
        session.query(Paikka)
        .filter(Paikka.lyhytnimi == paikka_lyhyt)
        .one_or_none()
    )
    return paikka


# read configuration from ini-file
cfg = Config(str_cfg_file)
# establish session to db with info from cfg-file
session = cfg.session

if __name__ == "__main__":
    v = uusi_valine(session, "TA181210222", "181210", "Modux480 vanha")
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
