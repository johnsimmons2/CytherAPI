from dataclasses import dataclass
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped
from extensions import db


@dataclass
class Spell(db.Model):
    __tablename__ = 'spell'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    abilityId: int = db.Column(Integer, ForeignKey('ability.id'), nullable=True)
    name: str = db.Column(String)
    castingTime: str = db.Column(String)
    description: str = db.Column(String)
    duration: str = db.Column(String)
    school: str = db.Column(String)
    range: str = db.Column(String)
    # 0: cantrip
    # 1 - 9: spell level
    level: int = db.Column(Integer)
    melee: bool = db.Column(Boolean, nullable=False)
    verbal: bool = db.Column(Boolean, nullable=False)
    somatic: bool = db.Column(Boolean, nullable=False)
    material: bool = db.Column(Boolean, nullable=False)
    ritual: bool = db.Column(Boolean, nullable=False)
    concentration: bool = db.Column(Boolean, nullable=False)

