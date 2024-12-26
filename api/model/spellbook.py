from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship
from extensions import db


class Spellbook(db.Model):
    __tablename__ = 'spellbook'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    # knowledgeId = db.Column(Integer, ForeignKey('spellbookknowledge.id'))
    # preparedId = db.Column(Integer, ForeignKey('spellbookprepared.id'))
    # cantripId = db.Column(Integer, ForeignKey('cantripknowledge.id'))

    spellslot1 = db.Column(Integer)
    spellslot2 = db.Column(Integer)
    spellslot3 = db.Column(Integer)
    spellslot4 = db.Column(Integer)
    spellslot5 = db.Column(Integer)
    spellslot6 = db.Column(Integer)
    spellslot7 = db.Column(Integer)
    spellslot8 = db.Column(Integer)
    spellslot9 = db.Column(Integer)
    warlockslots = db.Column(Integer)
    warlockslotlevel = db.Column(Integer)

    statsheet = relationship("Statsheet", back_populates="spellbook")
    knowledge = relationship("SpellbookKnowledge", back_populates="spellbook")
    prepared = relationship("SpellbookPrepared", back_populates="spellbook")
    cantrips = relationship("CantripKnowledge", back_populates="spellbook")

    query = db.Query

class SpellbookKnowledge(db.Model):
    __tablename__ = 'spellbookknowledge'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    spellbookId = db.Column(Integer, ForeignKey('spellbook.id'))
    spellId = db.Column(Integer, ForeignKey('spells.id'))

    spellbook = relationship("Spellbook", back_populates="knowledge")
    spell = relationship("Spells")

    query = db.Query

class SpellbookPrepared(db.Model):
    __tablename__ = 'spellbookprepared'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    spellbookId = db.Column(Integer, ForeignKey('spellbook.id'))
    spellId = db.Column(Integer, ForeignKey('spells.id'))

    spellbook = relationship("Spellbook", back_populates="prepared")
    spell = relationship("Spells")

    query = db.Query

# TODO: DEPRECATE? Level 0 spells are already cantrips
class CantripKnowledge(db.Model):
    __tablename__ = 'cantripknowledge'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    spellbookId = db.Column(Integer, ForeignKey('spellbook.id'))
    spellId = db.Column(Integer)

    spellbook = relationship("Spellbook", back_populates="cantrips")
