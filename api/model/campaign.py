from dataclasses import dataclass

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from api.model.character import Character
from extensions import db


@dataclass
class Campaign(db.Model):
    __tablename__ = 'campaign'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String(255))
    description: str = db.Column(Text)
    
    created: str = db.Column(DateTime)
    updated: str = db.Column(DateTime)
    active: bool = db.Column(Boolean)

    notes = relationship("Note", back_populates="campaign", cascade="all,delete")
    characters = relationship("Character", secondary="campaign_characters", backref="campaign", cascade="all,delete")

@dataclass
class Campaign_Characters(db.Model):
    __tablename__ = 'campaign_characters'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    campaignId: int = db.Column(Integer, ForeignKey('campaign.id'))
    characterId: int = db.Column(Integer, ForeignKey('character.id'))
    active: bool = db.Column(Boolean)

@dataclass
class Note(db.Model):
    __tablename__ = 'note'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    campaignId: int = db.Column(Integer, ForeignKey('campaign.id'))
    name: str = db.Column(String(255))
    description: str = db.Column(Text)
    created: str = db.Column(DateTime)
    updated: str = db.Column(DateTime)
    active: bool = db.Column(Boolean)

    campaign = relationship("Campaign", back_populates="notes", cascade="all,delete")