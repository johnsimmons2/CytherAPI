from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship
from . import db


class Hitdice(db.Model):
    __tablename__ = 'hitdice'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    statsheetId = db.Column(Integer, ForeignKey('statsheet.id'))
    d4 = db.Column(Integer)
    d6 = db.Column(Integer)
    d8 = db.Column(Integer)
    d10 = db.Column(Integer)
    d12 = db.Column(Integer)

    statsheet = relationship("Statsheet", back_populates="hitdice")

    query = db.Query
