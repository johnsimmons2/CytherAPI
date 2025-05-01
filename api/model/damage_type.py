from dataclasses import dataclass
from sqlalchemy.sql.sqltypes import String, Integer
from extensions import db


@dataclass
class DamageType(db.Model):
    __tablename__ = "damage_type"
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String, nullable=False)
    description: str = db.Column(String)
    icon: str = db.Column(String)