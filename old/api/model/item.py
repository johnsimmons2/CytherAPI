from dataclasses import dataclass
import enum
from sqlalchemy.sql.sqltypes import String, Float, Boolean, DateTime, Integer, Text, Enum
from api.model.itemtypeenums import ItemBaseType, ItemCondition, ItemMaterial, ItemProperty, ItemRarity, ItemStackable, ItemWeight
from extensions import db


@dataclass
class Item(db.Model):
    __tablename__ = 'item'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String)
    description: str = db.Column(Text)
    type: str = db.Column(Enum(ItemBaseType), nullable=False)
    isConsumable: bool = db.Column(Boolean, nullable=False)
    rarity: str = db.Column(Enum(ItemRarity), nullable=False)
    weight: str = db.Column(Enum(ItemWeight), nullable=False)
    property: str = db.Column(Enum(ItemProperty), nullable=False)
    stackable: str = db.Column(Enum(ItemStackable), nullable=False)
    condition: str = db.Column(Enum(ItemCondition), nullable=False)
    material: str = db.Column(Enum(ItemMaterial), nullable=False)