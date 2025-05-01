from dataclasses import dataclass
from sqlalchemy import ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer
from extensions import db


@dataclass
class Language(db.Model):
    __tablename__ = "language"
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String, nullable=False)
    description: str = db.Column(String, nullable=False)