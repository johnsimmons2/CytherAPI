from dataclasses import dataclass
from typing import List
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship, Mapped
from api.model.user import User
from extensions import db


@dataclass
class Tag(db.Model):
    __tablename__ = 'tag'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    userId: int = db.Column(Integer, ForeignKey('user.id'), nullable=True)
    
    name: str = db.Column(String(255))
    description: str = db.Column(Text)
    
    created: str = db.Column(DateTime)
    updated: str = db.Column(DateTime)
    active: bool = db.Column(Boolean)
    color: str = db.Column(String)
    icon: str = db.Column(String)

@dataclass
class Note(db.Model):
    __tablename__ = 'note'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    # If the user ID is present, the note belongs to that user.
    userId: int = db.Column(Integer, ForeignKey('user.id'), nullable=True)
    # If the character ID is present, the note belongs to that character.
    # If there was no user ID, then the note is an ADMIN NOTE.
    characterId: int = db.Column(Integer, ForeignKey('character.id'), nullable=True)
    # If the campaign ID is present, the note belongs to that campaign.
    # If there was no user ID and no character ID, then the note is an ADMIN NOTE.
    # If there was only a character ID then the note is shared with the entire campaign.
    campaignId: int = db.Column(Integer, ForeignKey('campaign.id'), nullable=True)
    name: str = db.Column(String(255))
    # The directory of the note, parsed on the front-end. It should be:
    # /username/
    # /campaignname/
    # /charactername/
    # /$global/ <-- REQUIRE AUTH FOR ADMIN
    directory: str = db.Column(String(255))
    description: str = db.Column(Text)
    
    created: str = db.Column(DateTime)
    updated: str = db.Column(DateTime)
    active: bool = db.Column(Boolean)
    
    creator = relationship("User", backref="notes_created")
    character = relationship("Character", backref="notes")
    campaign = relationship("Campaign", backref="notes")
    shared_users: Mapped[List[User]] = relationship("User", secondary="note_shared_users", backref="shared_notes", cascade="all,delete")
    tags: Mapped[List[Tag]] = relationship("Tag", secondary="note_tags", backref="notes", cascade="all,delete")

@dataclass
class NoteSharedDirectories(db.Model):
    __tablename__ = 'note_shared_directories'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    userId: int = db.Column(Integer, ForeignKey('user.id'))
    sharedWithId: int = db.Column(Integer, ForeignKey('user.id'))
    directory: str = db.Column(String(255))
    shareDate: str = db.Column(DateTime)

@dataclass
class NoteSharedUsers(db.Model):
    __tablename__ = 'note_shared_users'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    noteId: int = db.Column(Integer, ForeignKey('note.id'))
    userId: int = db.Column(Integer, ForeignKey('user.id'))
    shareDate: str = db.Column(DateTime)
    
@dataclass
class TagSharedUsers(db.Model):
    __tablename__ = 'tag_shared_users'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    tagId: int = db.Column(Integer, ForeignKey('tag.id'))
    userId: int = db.Column(Integer, ForeignKey('user.id'))
    sharedWithId: int = db.Column(Integer, ForeignKey('user.id'))    
    shareDate: str = db.Column(DateTime)

@dataclass
class NoteTags(db.Model):
    __tablename__ = 'note_tags'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    noteId: int = db.Column(Integer, ForeignKey('note.id'))
    tagId: int = db.Column(Integer, ForeignKey('tag.id'))