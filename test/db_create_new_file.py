from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_structures import Paikka, Luokka, Tapahtuma_Luokka, Meta

# this program creates a new db-structure
# with the help of functions in create_module and the parameters
# given below

# define parameters for the new db

str_db_file = "test49.db"
str_db_version_info = "introduced table meta for db with version"\
                    + "and version_info"

hyllyt = {
    "A": [3, 5, [3, 3, 4]],
    "B": [3, 3, [3, 3, 3]],
    "C": [3, 3, [3, 3, 3]],
    "D": [3, 3, [3, 3, 3]],
    "E": [2, 4, [4, 4]]
        }

luokat = {
    "181210": "sängyt",
    "043306": "painehaavapatjat",
    "122203": "pyörätuolit",
    "120606": "kävelytelineet",
    "181224": "sängynpäädynkohottaja",
    "044808": "seisontatuet, kehikot",
    "044821": "kippilaudat",
    "093312": "suihkupaarit",
    "093303": "suihkutuolit, pyörättömät",
    "091203": "suihkupyörätuolit",
    "120612": "kävelypöydät",
             }

tapahtumaluokat = [
    "sisään",
    "ulos",
    "siirto",
    "uusi"
]

# define functions that actually create the db and structures


def luo_db_file(str_db_file, version_info):
    import sqlite3
    from sqlite3 import Error
    # the SQL-queries that create the db-structure
    create_string = ["""CREATE TABLE `meta` (
    `version` INTEGER NOT NULL PRIMARY KEY,
    `version_info` varchar(255)
    );
    """, """
    CREATE TABLE `valine` (
    `ta_no` varchar(255) NOT NULL PRIMARY KEY,
    `luokka_id` varchar(255) REFERENCES luokka,
    `nimi` varchar(255),
    `huomautus` varchar(255),
    `paikka_id` INTEGER REFERENCES paikka,
    `active` tinyint
    );
    """, """
    CREATE TABLE `luokka` (
    `luokka_id` varchar(10) NOT NULL PRIMARY KEY,
    `luokka_nimi` varchar(255)
    );
    """, """
    CREATE TABLE `paikka` (
    `paikka_id` INTEGER NOT NULL PRIMARY KEY,
    `lyhytnimi` varchar(255),
    `hylly` varchar(255),
    `taso` tinyint,
    `vali` tinyint,
    `lava` tinyint,
    `active` tinyint
    );
    """, """
    CREATE TABLE `tapahtuma` (
    `tapaht_id` INTEGER NOT NULL PRIMARY KEY,
    `ta_no` varchar(255) REFERENCES valine,
    `tapaht_luokka` INTEGER REFERENCES tapahtuma_luokka,
    `paikka_id` INTEGER REFERENCES paikka,
    `tapaht_kuvaus` varchar(255),
    `tapahtunut` datetime DEFAULT (now())
    );
    """, """
    CREATE TABLE `tapahtuma_luokka` (
    `tapaht_luokka_id` INTEGER NOT NULL PRIMARY KEY,
    `tapaht_kuvaus` varchar(255)
    );
    """]
    # create new db-file
    conn = None
    try:
        conn = sqlite3.connect(f"test\\db\\{str_db_file}")
    except Error as e:
        print(e)
    crsr = conn.cursor()
    # execute sql-queries one after another
    for query in create_string:
        crsr.execute(query)

    # connect to the database through SQLAlchemy
    engine = create_engine(f'sqlite:///test//db//{str_db_file}', echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    # write meta-info into new db
    meta = Meta(version_info=version_info)
    session.add(meta)
    session.commit()


def luo_db_paikat(str_db_file, hyllyt):

    # connect to the database through SQLAlchemy
    engine = create_engine(f'sqlite:///test//db//{str_db_file}', echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    # iterate through the places and call add_paikka
    for hylly, elem in hyllyt.items():
        valit = hyllyt[hylly][0]
        tasot = hyllyt[hylly][1]
        lavat = hyllyt[hylly][2]

        for vali in range(valit):
            for t in range(tasot):
                taso = tasot-t-1
                for lava in range(lavat[vali]):
                    lyhytnimi = hylly + str(vali) + str(taso) + str(lava)
                    onko = session.query(Paikka.lyhytnimi)\
                        .filter(Paikka.lyhytnimi == lyhytnimi).all()
                    if onko != []:
                        print(lyhytnimi + " on jo olemassa")
                    else:
                        paikka = Paikka(lyhytnimi=lyhytnimi, hylly=hylly,
                                        vali=vali, taso=taso,
                                        lava=lava, active=0)
                        session.add(paikka)
    session.commit()


def luo_db_luokat(str_db_file, luokat):
    # connect to the database through SQLAlchemy
    engine = create_engine(f'sqlite:///test//db//{str_db_file}', echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    for no, nimi in luokat.items():
        onko = session.query(Luokka.luokka_id)\
               .filter(Luokka.luokka_id == no).all()
        if onko != []:
            print(no + " on jo olemassa")
        else:
            luokka = Luokka(luokka_id=no, luokka_nimi=nimi)
            session.add(luokka)
    session.commit()


def luo_db_tapahtumaluokat(str_db_file, tapahtumat):
    # connect to the database through SQLAlchemy
    engine = create_engine(f'sqlite:///test//db//{str_db_file}', echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    for luokka in tapahtumat:
        onko = session.query(Tapahtuma_Luokka.tapaht_kuvaus)\
               .filter(Tapahtuma_Luokka.tapaht_kuvaus == luokka).all()
        if onko != []:
            print(luokka + " on jo olemassa")
        else:
            tapahtumaluokka = Tapahtuma_Luokka(tapaht_kuvaus=luokka)
            session.add(tapahtumaluokka)
    session.commit()


# call functions to create first the
# database and then fill it with the table-data given above

luo_db_file(str_db_file, str_db_version_info)
luo_db_paikat(str_db_file, hyllyt)
luo_db_luokat(str_db_file, luokat)
luo_db_tapahtumaluokat(str_db_file, tapahtumaluokat)
