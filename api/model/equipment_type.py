from dataclasses import dataclass
from sqlalchemy.sql.sqltypes import String, Integer
from extensions import db


@dataclass
class EquipmentType(db.Model):
    __tablename__ = "equipment_type"
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String, nullable=False)
    description: str = db.Column(String)
    icon: str = db.Column(String)
    isWeapon: bool = db.Column(db.Boolean, nullable=False)
    isArmor: bool = db.Column(db.Boolean, nullable=False)
    isShield: bool = db.Column(db.Boolean, nullable=False)