from sqlalchemy import String, Boolean, Integer
from . import db


class Spells(db.Model):
    __tablename__ = 'spells'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    spellComponentId = db.Column(Integer)
    name = db.Column(String)
    castingTime = db.Column(String)
    description = db.Column(String)
    duration = db.Column(String)
    school = db.Column(String)
    # 0: Spell
    # 1: Cantrip
    type = db.Column(Integer)
    # 0: cantrip
    # 1 - 9: spell level
    level = db.Column(Integer)
    verbal = db.Column(Boolean)
    somatic = db.Column(Boolean)
    material = db.Column(Boolean)
    ritual = db.Column(Boolean)

    query = db.Query

class SpellComponents(db.Model):
    __tablename__ = 'spellcomponents'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    spellId = db.Column(Integer)
    itemId = db.Column(Integer)
    quantity = db.Column(Integer)
    goldValue = db.Column(Integer)