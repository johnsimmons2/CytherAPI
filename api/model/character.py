from dataclasses import dataclass
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Text
from . import db
from api.model.dice import Hitdice
from api.model.spellbook import Spellbook
from api.model import classes


# TODO: Change race to a relationship
@dataclass
class Character(db.Model):
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    statsheetid: int = db.Column(Integer, ForeignKey('statsheet.id'), unique=True)
    raceId: int = db.Column(Integer, ForeignKey('race.id'), unique=True)
    classId: int = db.Column(Integer, ForeignKey('class.id'), unique=True)

    # 0: Player
    # 1: NPC
    type: int = db.Column(Integer)
    speed: int = db.Column(Integer)
    languages: str = db.Column(String)
    name: str = db.Column(String)

    # If the campaign compatability number matches the campaign ID, the character may be used.
    campaignCompatability: int = db.Column(Integer)

    race = db.relationship("Race", uselist=False)
    class_ = db.relationship("Class", uselist=False)
    statsheet = db.relationship("Statsheet", uselist=False, foreign_keys=[statsheetid], backref="statsheetid", cascade="all,delete")
    characterDescription = db.relationship("CharacterDescription", uselist=False, backref="character", cascade="all,delete")

@dataclass
class CharacterDescription(db.Model):
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    characterId: int = db.Column(Integer, ForeignKey('character.id'), unique=True)
    age: str = db.Column(String, nullable=True)
    height: str = db.Column(String, nullable=True)
    weight: str = db.Column(String, nullable=True)
    eyes: str = db.Column(String, nullable=True)
    skin: str = db.Column(String, nullable=True)
    hair: str = db.Column(String, nullable=True)

    background: str = db.Column(Text, nullable=True)
    appearance: str = db.Column(Text, nullable=True)
    bonds: str = db.Column(Text, nullable=True)
    ideals: str = db.Column(Text, nullable=True)
    personality: str = db.Column(Text, nullable=True)
    flaws: str = db.Column(Text, nullable=True)
    religion: str = db.Column(Text, nullable=True)
    backstory: str = db.Column(Text, nullable=True)

@dataclass
class Skill(db.Model):
    __tablename__ = 'skill'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String)
    description: str = db.Column(String)

# TODO: Make default entries in startup alongside roles, or relate to stats table for future custom stats
@dataclass
class Proficiency(db.Model):
    __tablename__ = 'proficiency'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String, unique=True)
    description: str = db.Column(String)

# TODO: Make default entries in startup alongside roles
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
    hitdice = db.relationship("Hitdice", uselist=False, back_populates="statsheet", cascade="all,delete")

class Inventory(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    characterId = db.Column(Integer, db.ForeignKey('character.id'), unique=True)

    itemId = db.Column(Integer)
    quantity = db.Column(Integer)
