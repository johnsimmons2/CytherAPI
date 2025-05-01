from dataclasses import dataclass
from sqlalchemy.sql.sqltypes import String, Integer
from extensions import db


@dataclass
class Ability(db.Model):
    __tablename__ = "ability"
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String, nullable=False)
    min: int = db.Column(Integer, nullable=False)
    max: int = db.Column(Integer, nullable=False)
    description: str = db.Column(String, nullable=False)
    abbreviation: str = db.Column(String, nullable=False)