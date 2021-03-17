from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Valine(Base):
    __tablename__ = "valine"
    ta_no = Column(String, primary_key=True)
    luokka_id = Column(Integer)
    valine_nimi = Column(String)
    huomautus = Column(String)
    paikka_id = Column(Integer)
    active = Column(Integer)
    
    tapahtumat = relationship("Tamaphtuma", backref=backref("ta_no"))


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
