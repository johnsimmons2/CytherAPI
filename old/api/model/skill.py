from dataclasses import dataclass

from sqlalchemy import ForeignKey
from extensions import db
from sqlalchemy.sql.sqltypes import String, Integer


@dataclass
class Skill(db.Model):
    __tablename__ = 'skill'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    abilityId: int = db.Column(Integer, ForeignKey('ability.id'), nullable=False)
    name: str = db.Column(String)
    description: str = db.Column(String)