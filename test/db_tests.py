from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from db_structures import Paikka, Valine, Luokka, Tapahtuma, Tapahtuma_Luokka
# from datetime import datetime
# import configparser
import functions

""" here I test methods that should read and write the databases structure
from the database itself. It then should generate the warehouses properties
fom information of the database.
"""

def db_read_hyllyt(session):
    


str_cfg_file = "test//varasto_cfg.ini"
cfg = functions.Config(str_cfg_file)
session = cfg.session

engine = create_engine("sqlite:///test//db//test79.db", echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
Base = declarative_base()
Base.metadata.create_all(engine)

v = functions.etsi_valine(session, "TA181210155")
print(v.nimi, v.paikka.lyhytnimi)
