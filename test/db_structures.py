from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Valine(Base):
    __tablename__ = "valine"
    ta_no = Column(String, primary_key=True)
    luokka_id = Column(Integer, ForeignKey("luokka.luokka_id"))
    valine_nimi = Column(String)
    huomautus = Column(String)
    paikka_id = Column(Integer, ForeignKey("paikka.paikka_id"))
    active = Column(Integer)

    tapahtumat = relationship("Tapahtuma", backref=backref("ta_no"))


class Tapahtuma(Base):
    __tablename__ = "tapahtuma"
    tapaht_id = Column(Integer, primary_key=True)
    ta_no = Column(String, ForeignKey("valine.ta_no"))
    tluokka = Column(Integer, ForeignKey("tapahtuma_luokka.tapaht_luokka_id"))
    paikka_id = Column(Integer, ForeignKey("paikka.paikka_id"))
    tapahtunut = Column(DateTime)


class Paikka(Base):
    __tablename__ = "paikka"
    paikka_id = Column(Integer, primary_key=True)
    lyhytnimi = Column(String)
    hylly = Column(String)
    taso = Column(Integer)
    vali = Column(Integer)
    lava = Column(Integer)
    active = Column(Integer)

    valineet = relationship("Valine", backref=backref("paikka_id"))
    tapahtumat_paikalla = relationship(
                            "Tapahtuma",
                            backref=backref("paikka_id"))


class Luokka(Base):
    __tablename__ = "luokka"
    luokka_id = Column(Integer, primary_key=True)
    luokka_nimi = Column(String)

    valineet_luokassa = relationship("Valine", backref=backref("luokka_id"))


class Tapahtuma_Luokka(Base):
    __tablename__ = "tapahtuma_luokka"
    tapaht_luokka_id = Column(Integer, primary_key=True)
    tapaht_kuvaus = Column(String)

    tapahtumat_luokassa = relationship("Tapahtuma", backref=backref("tluokka"))
