from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from . import db
from .dice import Hitdice


class Character(db.Model):
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String)
    # 0: Player
    # 1: NPC
    type: int = db.Column(Integer)
    race: str = db.Column(String)
    classId: int = db.Column(Integer)
    subclassId: int = db.Column(Integer)

    statsheet = relationship("Statsheet", back_populates="character", cascade="all,delete")

class Statsheet(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    characterId = db.Column(Integer, db.ForeignKey('character.id'), unique=True)
    spellbookId = db.Column(Integer, db.ForeignKey('spellbook.id'), unique=True)

    strength = db.Column(Integer)
    dexterity = db.Column(Integer)
    constitution = db.Column(Integer)
    intelligence = db.Column(Integer)
    wisdom = db.Column(Integer)
    charisma = db.Column(Integer)
    health = db.Column(Integer)

    character = relationship("Character", uselist=False, back_populates="statsheet", cascade="all,delete")
    spellbook = relationship("Spellbook", uselist=False, back_populates="statsheet", cascade="all,delete")
    hitdice = relationship("Hitdice", back_populates="statsheet", cascade="all,delete")

class Inventory(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    itemId = db.Column(Integer)
    quantity = db.Column(Integer)