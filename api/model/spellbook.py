from dataclasses import dataclass
from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.orm import relationship
from extensions import db


@dataclass
class Spellbook(db.Model):
    __tablename__ = 'spellbook'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    statsheetId: int = db.Column(Integer, ForeignKey('statsheet.id'), nullable=False)
    spellCastingAbilityId: int = db.Column(Integer, ForeignKey('ability.id'), nullable=False)
    spellslot1: int = db.Column(Integer)
    spellslot2: int = db.Column(Integer)
    spellslot3: int = db.Column(Integer)
    spellslot4: int = db.Column(Integer)
    spellslot5: int = db.Column(Integer)
    spellslot6: int = db.Column(Integer)
    spellslot7: int = db.Column(Integer)
    spellslot8: int = db.Column(Integer)
    spellslot9: int = db.Column(Integer)
    cantrips: int = db.Column(Integer)
    spellsKnown: int = db.Column(Integer)
    spellsPrepared: int = db.Column(Integer)
    actions: int = db.Column(Integer)
    bonusActions: int = db.Column(Integer)

@dataclass
class SpellbookSpell(db.Model):
    __tablename__ = 'spellbook_spell'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    spellbookId: int = db.Column(Integer, ForeignKey('spellbook.id'), nullable=False)
    spellId: int = db.Column(Integer, ForeignKey('spell.id'), nullable=False)
    spellLevel: int = db.Column(Integer) # So I can give users 3rd level spell 'X' but naturally upcast to 5th level.
    isCantrip: bool = db.Column(Boolean, default=False) # So I can give users a spell as a cantrip