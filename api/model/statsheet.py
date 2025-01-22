from dataclasses import dataclass
from sqlalchemy import ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, Boolean, DateTime
from extensions import db


@dataclass
class Statsheet(db.Model):
    __tablename__ = "statsheet"
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    health: int = db.Column(Integer)
    maxHealth: int = db.Column(Integer)
    tempHealth: int = db.Column(Integer)
    armorClass: int = db.Column(Integer)
    initative: int = db.Column(Integer)
    exhaustion: int = db.Column(Integer)
    observation: int = db.Column(Integer)
    walkSpeed: int = db.Column(Integer)
    swimSpeed: int = db.Column(Integer)
    flySpeed: int = db.Column(Integer)
    burrowSpeed: int = db.Column(Integer)
    climbSpeed: int = db.Column(Integer)
    updated: str = db.Column(DateTime)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class StatsheetAbility(db.Model):
    __tablename__ = "statsheet_ability"
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    statshetId: int = db.Column(Integer, ForeignKey('statsheet.id'), nullable=False)
    abilityId: int = db.Column(Integer, ForeignKey('ability.id'), nullable=False)
    adjustment: int = db.Column(Integer)
    value: int = db.Column(Integer, nullable=False)

@dataclass
class StatsheetProficiency(db.Model):
    __tablename__ = "statsheet_proficiency"
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    statshetId: int = db.Column(Integer, ForeignKey('statsheet.id'), nullable=False)
    skillId: int = db.Column(Integer, ForeignKey('skill.id'), nullable=True)
    adjustment: int = db.Column(Integer)
    custom: str = db.Column(String)
    source: str = db.Column(String)
    updated: str = db.Column(DateTime)
    
@dataclass
class StatsheetSavingthrow(db.Model):
    __tablename__ = "statsheet_savingthrow"
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    statshetId: int = db.Column(Integer, ForeignKey('statsheet.id'), nullable=False)
    abilityId: int = db.Column(Integer, ForeignKey('ability.id'), nullable=False)
    advantage: bool = db.Column(Boolean)
    source: str = db.Column(String)
    updated: str = db.Column(DateTime)

@dataclass
class StatsheetDamageType(db.Model):
    __tablename__ = "statsheet_damage_type"
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    statshetId: int = db.Column(Integer, ForeignKey('statsheet.id'), nullable=False)
    damageTypeId: int = db.Column(Integer, ForeignKey('damage_type.id'), nullable=False)
    vulnerable: bool = db.Column(Boolean)
    resistant: bool = db.Column(Boolean)
    immune: bool = db.Column(Boolean)
    source: str = db.Column(String)
    updated: str = db.Column(DateTime)