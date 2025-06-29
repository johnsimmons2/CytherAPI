from dataclasses import dataclass
from sqlalchemy import ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer
from extensions import db


@dataclass
class Condition(db.Model):
    __tablename__ = "condition"
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String, nullable=False)
    description: str = db.Column(String, nullable=False)
    source: str = db.Column(String)
    
@dataclass
class ConditionEffect(db.Model):
    __tablename__ = "condition_effect"
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    conditionId: int = db.Column(Integer, ForeignKey('condition.id'), nullable=False)
    description: str = db.Column(String, nullable=True)
    vulnerableId: int = db.Column(Integer, ForeignKey('damage_type.id'), nullable=True)
    resistantId: int = db.Column(Integer, ForeignKey('damage_type.id'), nullable=True)
    immuneId: int = db.Column(Integer, ForeignKey('damage_type.id'), nullable=True)
    abilityId: int = db.Column(Integer, ForeignKey('ability.id'), nullable=True)
    abilityAdj: int = db.Column(Integer, nullable=True)
    skillId: int = db.Column(Integer, ForeignKey('skill.id'), nullable=True)
    skillAdj: int = db.Column(Integer, nullable=True)
    rollAdvantage: bool = db.Column(db.Boolean, nullable=True)
    rollDisadvantage: bool = db.Column(db.Boolean, nullable=True)
    # RollType: attack, skill, saving throw, etc.
    rollType: str = db.Column(String, nullable=True)