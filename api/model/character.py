from dataclasses import dataclass
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.sql.sqltypes import Text, String, Integer, Boolean, DateTime
from api.model.enums import EquipSlots
from extensions import db


@dataclass
class Character(db.Model):
    __tablename__ = "character"
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    statsheetid: int = db.Column(Integer, ForeignKey('statsheet.id'), unique=True)
    raceId: int = db.Column(Integer, ForeignKey('race.id'), nullable=False)
    userId: int = db.Column(Integer, ForeignKey('user.id'))
    isNpc: bool = db.Column(Boolean, nullable=False)
    
    age: int = db.Column(Integer)
    height: str = db.Column(String)
    weight: str = db.Column(String)
    eye_color: str = db.Column(String)
    skin_color: str = db.Column(String)
    hair_color: str = db.Column(String)
    alignment: str = db.Column(String)
    religion: str = db.Column(String)
    description: str = db.Column(Text)
    appearance: str = db.Column(Text)
    bonds: str = db.Column(Text)
    ideals: str = db.Column(Text)
    personality: str = db.Column(Text)
    flaws: str = db.Column(Text)
    backstory: str = db.Column(Text)
    
    created: str = db.Column(DateTime)
    updated: str = db.Column(DateTime)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class CharacterFeat(db.Model):
    __tablename__ = 'character_feat'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    characterId: int = db.Column(Integer, ForeignKey('character.id'))
    featId: int = db.Column(Integer, ForeignKey('feat.id'))

@dataclass
class CharacterRelationship(db.Model):
    __tablename__ = 'character_relationship'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    characterId: int = db.Column(Integer, ForeignKey('character.id'), nullable=False)
    otherCharacterId: int = db.Column(Integer, ForeignKey('character.id'), nullable=False)
    allies: bool = db.Column(Boolean, nullable=False)
    enemies: bool = db.Column(Boolean, nullable=False)

@dataclass
class CharacterClass(db.Model):
    __tablename__ = 'character_class'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    characterId: int = db.Column(Integer, ForeignKey('character.id'), nullable=False)
    classId: int = db.Column(Integer, ForeignKey('class.id'), nullable=False)
    subclassId: int = db.Column(Integer, ForeignKey('class.id'), nullable=False)
    usedHitDice: int = db.Column(Integer)
    level: int = db.Column(Integer)
    xp: int = db.Column(Integer)
    
@dataclass
class CharacterLanguage(db.Model):
    __tablename__ = 'character_language'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    characterId: int = db.Column(Integer, ForeignKey('character.id'), nullable=False)
    languageId: int = db.Column(Integer, ForeignKey('language.id'), nullable=False)
    
@dataclass
class CharacterCondition(db.Model):
    __tablename__ = 'character_condition'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    characterId: int = db.Column(Integer, ForeignKey('character.id'), nullable=False)
    conditionId: int = db.Column(Integer, ForeignKey('condition.id'), nullable=False)
    source: str = db.Column(String)
    duration: str = db.Column(String)
    stacks: int = db.Column(Integer)

@dataclass
class InventoryShared(db.Model):
    __tablename__ = 'inventory_shared'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    inventoryId: int = db.Column(Integer, ForeignKey('inventory.id'), nullable=False)
    sharedUserId: int = db.Column(Integer, ForeignKey('user.id'), nullable=False)

@dataclass
class Inventory(db.Model):
    __tablename__ = 'inventory'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    characterId: int = db.Column(Integer, ForeignKey('character.id'), nullable=False)
    itemId: int = db.Column(Integer, ForeignKey('item.id'), nullable=False)
    quantity: int = db.Column(Integer, default=1)
    equipped: bool = db.Column(Boolean, default=False)
    equipSlot: str = db.Column(Enum(EquipSlots), nullable=True)
    attuned: bool = db.Column(Boolean, default=False)
    updated: str = db.Column(DateTime)
