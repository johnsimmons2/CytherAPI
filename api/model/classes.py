from dataclasses import dataclass
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import relationship, Mapped
from . import db


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
    classId: int = db.Column(Integer, ForeignKey('class.id'))
    description: str = db.Column(String)
    name: str = db.Column(String)

    feats: Mapped[Feat] = db.relationship('Feat', secondary='subclass_feats', backref='subclass')

# Eventually this will track hit dice
@dataclass
class Class(db.Model):
    __tablename__ = 'class'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String)
    description: str = db.Column(String)

    subclasses: Mapped[Subclass] = db.relationship('Subclass', secondary="class_subclasses", backref='class')
    feats: Mapped[Feat] = db.relationship('Feat', secondary='class_feats', backref='class')

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