# this file contains the classes defining the SQLAlchemy ORM

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Meta(Base):
    __tablename__ = "meta"
    version = Column(Integer, primary_key=True, autoincrement=True)
    version_info = Column(String)
    version_date = Column(DateTime)


class Hyllyt(Base):
    __tablename__ = "hyllyt"
    hylly = Column(String, primary_key=True)
    tasot = Column(String)
    valit = Column(String)
    lavat = Column(String)


class Valine(Base):
    __tablename__ = "valine"
    ta_no = Column(String, primary_key=True)
    luokka_id = Column(String, ForeignKey("luokka.luokka_id"))
    nimi = Column(String)
    huomautus = Column(String)
    paikka_id = Column(Integer, ForeignKey("paikka.paikka_id"))
    active = Column(Integer)

    tapahtumat = relationship("Tapahtuma", backref=backref("valine"))


class Tapahtuma(Base):
    __tablename__ = "tapahtuma"
    tapaht_id = Column(Integer, primary_key=True, autoincrement=True)
    ta_no = Column(String, ForeignKey("valine.ta_no"))
    tapaht_luokka = Column(Integer,
                           ForeignKey("tapahtuma_luokka.tapaht_luokka_id"))
    paikka_id = Column(Integer, ForeignKey("paikka.paikka_id"))
    tapaht_kuvaus = Column(String)
    tapahtunut = Column(DateTime)


class Paikka(Base):
    __tablename__ = "paikka"
    paikka_id = Column(Integer, primary_key=True, autoincrement=True)
    lyhytnimi = Column(String)
    hylly = Column(String)
    taso = Column(Integer)
    vali = Column(Integer)
    lava = Column(Integer)
    active = Column(Integer)

    valineet = relationship("Valine", backref=backref("paikka"))
    tapahtumat_paikalla = relationship(
                            "Tapahtuma",
                            backref=backref("paikka"))


class Luokka(Base):
    __tablename__ = "luokka"
    luokka_id = Column(String, primary_key=True)
    luokka_nimi = Column(String)

    valineet_luokassa = relationship("Valine", backref=backref("luokka"))


class Tapahtuma_Luokka(Base):
    __tablename__ = "tapahtuma_luokka"
    tapaht_luokka_id = Column(Integer, primary_key=True, autoincrement=True)
    tapaht_kuvaus = Column(String)

    tapahtumat_luokassa = relationship("Tapahtuma",
                                       backref=backref("luokka"))
