from dataclasses import dataclass
from sqlalchemy import ForeignKey
from extensions import db
from sqlalchemy.sql.sqltypes import Text, String, Integer


@dataclass
class Feat(db.Model):
    __tablename__ = 'feat'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String)
    description: str = db.Column(String)
    requirements: str = db.Column(Text)

@dataclass
class FeatEffect(db.Model):
    __tablename__ = "feat_effect"
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    featId: int = db.Column(Integer, ForeignKey('feat.id'), nullable=False)
    conditionId: int = db.Column(Integer, ForeignKey('condition.id'), nullable=True)
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
    requirements: str = db.Column(Text)