from dataclasses import dataclass
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import relationship, Mapped
from extensions import db


@dataclass
class Feat(db.Model):
    id: int  = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String, unique=True)
    description: str = db.Column(String)
    prerequisite: Optional[str] = db.Column(String)

@dataclass
class Race(db.Model):
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String)
    description: str = db.Column(String)
    size: str = db.Column(String)
    languages: str = db.Column(String)
    alignment: str = db.Column(String)

    feats: Mapped[List[Feat]] = db.relationship('Feat', secondary='race_feats', backref='race')

@dataclass
class Subclass(db.Model):
    __tablename__ = 'subclass'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    description: str = db.Column(String)
    name: str = db.Column(String)

    feats: Mapped[List[Feat]] = db.relationship('Feat', secondary='subclass_feats', backref='subclass', uselist=True)

@dataclass
class ClassTable(db.Model):
    __tablename__ = 'class_table'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    classId: int = db.Column(Integer, ForeignKey('class.id'))

    # --- DEPRECATE? ---
    profBonus: int = db.Column(String)
    # --- ---------- ---

    # Spells known and Cantrips known are split by commas, example for Warlock below:
    # Cantrips Known: 2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4
    # Spells Known: 2,3,4,5,6,7,8,9,10,10,11,11,12,12,13,13,14,14,15,15
    cantripsKnown: int = db.Column(String)
    spellsKnown: int = db.Column(String)

    hitDice: int = db.Column(Integer) # 4 = d4, 8 = d8, etc.
    # Spell slots are stored as a string of integers separated by commas, example for Cleric below.
    # First number = level 1, 2nd number = level 2, etc.
    # Slot 1: (2,3,4)
    # Slot 2: (-,-,2,3)
    # Slot 9: (-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,1)
    level1SpellSlots: int = db.Column(String)
    level2SpellSlots: int = db.Column(String)
    level3SpellSlots: int = db.Column(String)
    level4SpellSlots: int = db.Column(String)
    level5SpellSlots: int = db.Column(String)
    level6SpellSlots: int = db.Column(String)
    level7SpellSlots: int = db.Column(String)
    level8SpellSlots: int = db.Column(String)
    level9SpellSlots: int = db.Column(String)

    # # Comma separated for each level, example: Ki for Monk
    # # (0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
    # classResource: str = db.Column(String)

@dataclass
class ClassResource(db.Model):
    __tablename__ = 'class_resource'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    classTableId: int = db.Column(Integer, ForeignKey('class_table.id'))
    name: str = db.Column(String)
    description: str = db.Column(String)
    max: int = db.Column(Integer)
    current: int = db.Column(Integer)

    classTable: Mapped[ClassTable] = db.relationship('ClassTable', backref='classResources')

# Eventually this will track hit dice
@dataclass
class Class(db.Model):
    __tablename__ = 'class'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String)
    description: str = db.Column(String)
    spellCastingAbility: str = db.Column(String, nullable=True)

    classTable: Mapped[ClassTable] = db.relationship('ClassTable', backref='class')
    subclasses: Mapped[List[Subclass]] = db.relationship('Subclass', secondary="class_subclasses", backref='class')
    feats: Mapped[List[Feat]] = db.relationship('Feat', secondary='class_feats', backref='class', uselist=True)

class SubClassFeats(db.Model):
    __tablename__ = 'subclass_feats'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    subclassId = db.Column(Integer, ForeignKey('subclass.id'))
    featId = db.Column(Integer, ForeignKey('feat.id'))

class ClassSubclasses(db.Model):
    __tablename__ = 'class_subclasses'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    classId = db.Column(Integer, ForeignKey('class.id'))
    subclassId = db.Column(Integer, ForeignKey('subclass.id'))

@dataclass
class RaceFeats(db.Model):
    __tablename__ = 'race_feats'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    raceId: int = db.Column(Integer, ForeignKey('race.id'))
    featId: int = db.Column(Integer, ForeignKey('feat.id'))

class ClassFeats(db.Model):
    __tablename__ = 'class_feats'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    classId = db.Column(Integer, ForeignKey('class.id'))
    featId = db.Column(Integer, ForeignKey('feat.id'))
