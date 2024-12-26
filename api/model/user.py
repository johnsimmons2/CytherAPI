from dataclasses import dataclass
from sqlalchemy import ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from api.model.character import Character
from extensions import db


@dataclass
class UserRole(db.Model):
    __tablename__ = 'user_role'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    userId: int = db.Column(Integer, db.ForeignKey('user.id'))
    roleId: int = db.Column(Integer, db.ForeignKey('role.id'))

class UserCharacters(db.Model):
    __tablename__ = 'user_characters'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    userId = db.Column(Integer, ForeignKey('user.id'))
    characterId = db.Column(Integer, ForeignKey('character.id'))

@dataclass
class Role(db.Model):
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    level: int = db.Column(Integer)
    roleName: str = db.Column(String)

@dataclass
class User(db.Model):
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    username: str = db.Column(String, unique=True)
    email: str = db.Column(String, unique=True)
    fName: str = db.Column(String)
    lName: str = db.Column(String)
    lastOnline: DateTime = db.Column(DateTime)
    created: DateTime = db.Column(DateTime)
    password = db.Column(String)
    salt = db.Column(String)

    characters = db.relationship('Character', secondary='user_characters', backref='user')
    roles = db.relationship('Role', secondary='user_role', backref='user')
    
    @classmethod
    def from_dict(cls, data):
        if 'roles' in data:
            data['roles'] = [Role(**role) for role in data['roles']]
        if 'characters' in data:
            data['characters'] = [Character.from_dict(**character) for character in data['characters']]
        return cls(**data)

@dataclass
class UserRequest(db.Model):
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    userId: int = db.Column(Integer, ForeignKey('user.id'))
    expiry: DateTime = db.Column(DateTime)
    content: str = db.Column(String)
