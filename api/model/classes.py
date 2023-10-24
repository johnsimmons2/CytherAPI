from dataclasses import dataclass
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from . import db


@dataclass
class Race(db.Model):
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String)
    description: str = db.Column(String)

    feats = db.relationship('Feat', secondary='race_feats', backref='race')

# Eventually this will track hit dice
@dataclass
class Class(db.Model):
    __tablename__ = 'class'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String)
    description: str = db.Column(String)

    subclasses = db.relationship('Subclass', secondary="class_subclasses", backref='class')
    feats = db.relationship('Feat', secondary='class_feats', backref='class')
    statsheet = relationship("Statsheet", uselist=False, back_populates="clazz", cascade="all,delete")

@dataclass
class Subclass(db.Model):
    __tablename__ = 'subclass'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    classId: int = db.Column(Integer, ForeignKey('class.id'))
    description: str = db.Column(String)
    name: str = db.Column(String)

    statsheet = db.relationship('Statsheet', uselist=False, back_populates='subclass', cascade="all,delete")
    feats = db.relationship('Feat', secondary='subclass_feats', backref='subclass')

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

class RaceFeats(db.Model):
    __tablename__ = 'race_feats'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    raceId = db.Column(Integer, ForeignKey('race.id'))
    featId = db.Column(Integer, ForeignKey('feat.id'))

class ClassFeats(db.Model):
    __tablename__ = 'class_feats'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    classId = db.Column(Integer, ForeignKey('class.id'))
    featId = db.Column(Integer, ForeignKey('feat.id'))

@dataclass
class Feat(db.Model):
    id: int  = db.Column(Integer, primary_key=True, autoincrement=True)
    description: str = db.Column(String)
    prerequisite: str = db.Column(String)
