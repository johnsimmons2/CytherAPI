from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from . import db
from .dice import Hitdice
from api.model import classes


class Character(db.Model):
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String)
    # 0: Player
    # 1: NPC
    type: int = db.Column(Integer)
    race: str = db.Column(String)

    # Untouched basis. Only updated on level up or manual changes.
    basestatsheet = relationship("Statsheet", uselist=False, back_populates="character", cascade="all,delete")
    # This statsheet will change and reflect what is available to the user.
    statsheet = relationship("Statsheet", uselist=False, back_populates="character", cascade="all,delete")

class Statsheet(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    characterId = db.Column(Integer, db.ForeignKey('character.id'), unique=True)
    spellbookId = db.Column(Integer, db.ForeignKey('spellbook.id'), unique=True)
    clazzId = db.Column(Integer, db.ForeignKey('class.id'), unique=True)
    subclassId = db.Column(Integer, db.ForeignKey('subclass.id'), unique=True)

    exp = db.Column(Integer)
    level = db.Column(Integer)
    health = db.Column(Integer)

    strength = db.Column(Integer)
    dexterity = db.Column(Integer)
    constitution = db.Column(Integer)
    intelligence = db.Column(Integer)
    wisdom = db.Column(Integer)
    charisma = db.Column(Integer)

    # 0: Base stats
    # 1: Current stats
    type = db.Column(Integer)

    clazz = relationship("Class", uselist=False, back_populates="statsheet", cascade="all,delete")
    subclass = relationship("Subclass", uselist=False, back_populates="statsheet", cascade="all,delete")
    character = relationship("Character", uselist=False, back_populates="statsheet", cascade="all,delete")
    spellbook = relationship("Spellbook", uselist=False, back_populates="statsheet", cascade="all,delete")
    hitdice = relationship("Hitdice", back_populates="statsheet", cascade="all,delete")

class Inventory(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    characterId = db.Column(Integer, db.ForeignKey('character.id'), unique=True)

    itemId = db.Column(Integer)
    quantity = db.Column(Integer)
