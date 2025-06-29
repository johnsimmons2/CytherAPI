from dataclasses import dataclass
from typing import List, Optional
from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, Text
from sqlalchemy.orm import relationship, Mapped
from extensions import db


@dataclass
class Class(db.Model):
    __tablename__ = 'class'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    primaryAbilityId: int = db.Column(Integer, ForeignKey('ability.id'), nullable=False)
    hitDice: str = db.Column(String)
    name: str = db.Column(String)
    description: str = db.Column(Text)
    isPrimary: bool = db.Column(Boolean)
    primaryClassId: int = db.Column(Integer, ForeignKey('class.id'), nullable=True)

@dataclass
class ClassTable(db.Model):
    __tablename__ = 'class_table'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    classId: int = db.Column(Integer, ForeignKey('class.id'), nullable=False)
    resourceId: int = db.Column(Integer, ForeignKey('class_resource.id'), nullable=True)
    equipTypeId: int = db.Column(Integer, ForeignKey('equipment_type.id'), nullable=True)
    featId: int = db.Column(Integer, ForeignKey('feat.id'), nullable=True)
    resourceQuantity: int = db.Column(Integer)
    level: int = db.Column(Integer)
    spellSlotQuantity: int = db.Column(Integer)
    spellSlotLevel: int = db.Column(Integer)
    requirements: str = db.Column(Text)

@dataclass
class ClassResource(db.Model):
    __tablename__ = 'class_resource'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String)
    description: str = db.Column(Text)
    
@dataclass
class ClassFeat(db.Model):
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    classId: int = db.Column(Integer, ForeignKey('class.id'), nullable=False)
    featId: int = db.Column(Integer, ForeignKey('feat.id'), nullable=False)