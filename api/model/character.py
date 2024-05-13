from dataclasses import dataclass
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Text
from . import db
from api.model.dice import Hitdice
from api.model.spellbook import Spellbook
from api.model import classes


@dataclass
class Character(db.Model):
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    statsheetid: int = db.Column(Integer, ForeignKey('statsheet.id'), unique=True)
    name: str = db.Column(String)
    # 0: Player
    # 1: NPC
    type: int = db.Column(Integer)
    speed: int = db.Column(Integer)
    race: str = db.Column(String)
    languages: str = db.Column(String)

    # If the campaign compatability number matches the campaign ID, the character may be used.
    campaignCompatability: int = db.Column(Integer)

    # This statsheet will change and reflect what is available to the user.
    statsheet = db.relationship("Statsheet", uselist=False, foreign_keys=[statsheetid], backref="statsheetid", cascade="all,delete")
    characterDescription = db.relationship("CharacterDescription", uselist=False, backref="character", cascade="all,delete")
    characterRace = db.relationship("Race", uselist=False, back_populates="character")

@dataclass
class CharacterDescription(db.Model):
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    characterId: int = db.Column(Integer, ForeignKey('character.id'), unique=True)
    age: str = db.Column(String)
    height: str = db.Column(String)
    weight: str = db.Column(String)
    eyes: str = db.Column(String)
    skin: str = db.Column(String)
    hair: str = db.Column(String)

    background: str = db.Column(Text)
    appearance: str = db.Column(Text)
    bonds: str = db.Column(Text)
    ideals: str = db.Column(Text)
    personality: str = db.Column(Text)
    flaws: str = db.Column(Text)
    religion: str = db.Column(Text)


@dataclass
class Skill(db.Model):
    __tablename__ = 'skill'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String)
    description: str = db.Column(String)

@dataclass
class Proficiency(db.Model):
    __tablename__ = 'proficiency'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String, unique=True)
    description: str = db.Column(String)

@dataclass
class SavingThrow(db.Model):
    __tablename__ = 'savingthrow'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    statName: str = db.Column(String)

class StatsheetProficiencies(db.Model):
    __tablename__ = 'statsheet_proficiencies'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    statsheetId = db.Column(Integer, ForeignKey('statsheet.id'))
    proficiencyId = db.Column(Integer, ForeignKey('proficiency.id'))

class StatsheetSkills(db.Model):
    __tablename__ = 'statsheet_skills'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    statsheetId = db.Column(Integer, ForeignKey('statsheet.id'))
    skillId = db.Column(Integer, ForeignKey('skill.id'))

class StatsheetSavingThrows(db.Model):
    __tablename__ = 'statsheet_savingthrows'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    statsheetId = db.Column(Integer, ForeignKey('statsheet.id'))
    savingThrowId = db.Column(Integer, ForeignKey('savingthrow.id'))

class Statsheet(db.Model):
    __tablename__ = 'statsheet'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    spellbookId = db.Column(Integer, db.ForeignKey('spellbook.id'), unique=True)

    inspiration = db.Column(Integer, default=0)

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

    proficiencies = db.relationship("Proficiency", secondary="statsheet_proficiencies", backref="statsheet")
    savingThrows = db.relationship("SavingThrow", secondary="statsheet_savingthrows", backref="statsheet")
    skills = db.relationship("Skill", secondary="statsheet_skills", backref="statsheet")
    spellbook = db.relationship("Spellbook", uselist=False, back_populates="statsheet", cascade="all,delete")
    hitdice = db.relationship("Hitdice", back_populates="statsheet", cascade="all,delete")

class Inventory(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    characterId = db.Column(Integer, db.ForeignKey('character.id'), unique=True)

    itemId = db.Column(Integer)
    quantity = db.Column(Integer)
