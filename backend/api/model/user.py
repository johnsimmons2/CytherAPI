from dataclasses import dataclass
from sqlalchemy import ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from . import db


@dataclass
class UserRole(db.Model):
    __tablename__ = 'user_role'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    userId: int = db.Column(Integer, db.ForeignKey('user.id'))
    roleId: int = db.Column(Integer, db.ForeignKey('role.id'))

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
    password = db.Column(String)
    salt = db.Column(String)
    created = db.Column(DateTime)
    lastOnline = db.Column(DateTime)
    
    roles = db.relationship('Role', secondary='user_role', backref='user')
    