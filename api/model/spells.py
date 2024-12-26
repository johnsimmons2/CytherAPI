from dataclasses import dataclass
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped
from extensions import db


# TODO: Change itemId to a one to many items relationship.
@dataclass
class SpellComponents(db.Model):
    __tablename__ = 'spellcomponents'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    spellId: int = db.Column(Integer, ForeignKey('spells.id'))
    itemId: int = db.Column(Integer)
    quantity: int = db.Column(Integer)
    goldValue: int = db.Column(Integer)

@dataclass
class Spells(db.Model):
    __tablename__ = 'spells'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String)
    castingTime: str = db.Column(String)
    description: str = db.Column(String)
    duration: str = db.Column(String)
    school: str = db.Column(String)
    range: str = db.Column(String)
    # 0: cantrip
    # 1 - 9: spell level
    level: int = db.Column(Integer)
    verbal: bool = db.Column(Boolean)
    somatic: bool = db.Column(Boolean)
    material: bool = db.Column(Boolean)
    ritual: bool = db.Column(Boolean)
    concentration: bool = db.Column(Boolean)

    components: Mapped[SpellComponents] = db.relationship('SpellComponents', uselist=False, backref='spells')

