from dataclasses import dataclass
from typing import List
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship, Mapped
from api.model.user import User
from extensions import db


note_shared_users = Table(
    'note_shared_users',
    db.metadata,
    Column('noteId', Integer, ForeignKey('note.id')),
    Column('userId', Integer, ForeignKey('user.id'))
)

@dataclass
class Note(db.Model):
    __tablename__ = 'note'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    userId: int = db.Column(Integer, ForeignKey('user.id'))
    characterId: int = db.Column(Integer, ForeignKey('character.id'))
    campaignId: int = db.Column(Integer, ForeignKey('campaign.id'))
    name: str = db.Column(String(255))
    description: str = db.Column(Text)
    
    created: str = db.Column(DateTime)
    updated: str = db.Column(DateTime)
    active: bool = db.Column(Boolean)
    
    creator = relationship("User", backref="notes_created")
    character = relationship("Character", backref="notes")
    shared_users: Mapped[List[User]] = relationship("User", secondary="note_shared_users", backref="shared_notes", cascade="all,delete")
    
@dataclass
class NoteSharedUsers:
    __tablename__ = 'note_shared_users'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    noteId: int = db.Column(Integer, ForeignKey('note.id'))
    userId: int = db.Column(Integer, ForeignKey('user.id'))