from dataclasses import dataclass
from sqlalchemy import ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, Enum
from api.model.enums import CreatureTypes
from extensions import db


@dataclass
class Race(db.Model):
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String)
    description: str = db.Column(String)
    size: str = db.Column(String, nullable=False)
    type: str = db.Column(Enum(CreatureTypes), nullable=True)
    walkSpeed: int = db.Column(Integer, nullable=False)
    swimSpeed: int = db.Column(Integer)
    flySpeed: int = db.Column(Integer)
    climbSpeed: int = db.Column(Integer)
    burrowSpeed: int = db.Column(Integer)

@dataclass
class RaceFeat(db.Model):
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    raceId: int = db.Column(Integer, ForeignKey('race.id'), nullable=False)
    featId: int = db.Column(Integer, ForeignKey('feat.id'), nullable=False)

@dataclass
class RaceLanguage(db.Model):
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    raceId: int = db.Column(Integer, ForeignKey('race.id'), nullable=False)
    languageId: int = db.Column(Integer, ForeignKey('language.id'), nullable=False)