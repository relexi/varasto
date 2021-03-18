from importlib import resources

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

"""
engine = create_engine('sqlite:///test3.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
"""


# Connect to the database using SQLAlchemy
engine = create_engine('sqlite:///test3.db', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
Base = declarative_base()

class Paikka(Base):
    __tablename__ = 'paikka'
    id = Column(Integer, primary_key=True)
    hyllyStr = Column(String)
    tasoNo = Column(Integer)
    valiNo = Column(Integer)
    lavaStr = Column(String)

    def __repr__(self):
        return "<Hylly(hyllyStr='%s', tasoNo='%s', valiNo='%s', lavaStr='%s')\
            >" % (self.hyllyStr, self.tasoNo, self.valiNo, self.lavaStr)


Base.metadata.create_all(engine)


def tyhjeneVarasto():
    for instance in session.query(Paikka):
        session.delete(instance)


def teeVarasto():
    hyllyt = {
        "hylly": ["A", "B", "C", "D", "E"],
        "taso": [0, 1, 2, 3, 4, 5],
        "vali": [0, 1, 2, 3, 4, 5],
        "lava": ["v", "o", "k"]
    }

    for h in hyllyt.get("hylly"):
        for t in hyllyt.get("taso"):
            for v in hyllyt.get("vali"):
                for la in hyllyt.get("lava"):
                    p = Paikka(hyllyStr=h, tasoNo=t, valiNo=v, lavaStr=la)
                    session.add(p)


tyhjeneVarasto()
teeVarasto()
session.commit()


for instance in session.query(Paikka).order_by(Paikka.id):
    print(instance.id, instance.hyllyStr, instance.tasoNo,
          instance.valiNo, instance.lavaStr)
