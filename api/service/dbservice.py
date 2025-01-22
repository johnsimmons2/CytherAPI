import base64
import os
import hashlib
import api.service.jwthelper as jwth
from api.model.dto.characterDto import CharacterDTO
from api.model.dto.statsheetDto import StatsheetDTO
from api.model.dto.userDto import UserDTO
from api.model.spell import Spells, SpellComponents
from api.model.campaign import Campaign
from api.model.classes import *
from api.model.ext_content import Ext_Content
from api.service.ext_dbservice import Ext_ContentService
from types import SimpleNamespace
from datetime import date, datetime, timedelta
from uuid import uuid4
from api.model.user import *
from api.model.item import *
from api.model.character import *
from api.model.spellbook import *
from api.service.config import config
from api.loghandler.logger import Logger
from sqlalchemy.orm import Query
from sqlalchemy import desc, func
from flask_mail import Message
from flask import current_app
from api.service.repo.authservice import AuthService
from extensions import db

    
class RoleService:
    query = Query(Role, db.session)

    @classmethod
    def getAll(cls):
        return cls.query.all()

    @classmethod
    def get(cls, id: str):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def roleWithLevel(cls, level: int):
        return cls.query.filter_by(level=level).first()
    
    @classmethod
    def getRolesForUser(cls, userId: int):
        return Query(UserRole, db.session).filter_by(userId=userId).all()

    @classmethod
    def initRoles(cls):
        cls.query.filter_by(roleName="Admin").first() or db.session.add(
            Role(roleName="Admin", level=0)
        )
        cls.query.filter_by(roleName="Player").first() or db.session.add(
            Role(roleName="Player", level=1)
        )
        cls.query.filter_by(roleName="Guest").first() or db.session.add(
            Role(roleName="Guest", level=2)
        )
        db.session.commit()

class UserService:
    query = Query(User, db.session)

    @classmethod
    def getCurrentUserRoles(cls):
        username = jwth.decode_token(jwth.get_access_token())["username"]
        if username is not None:
            return cls.query.filter(func.lower(User.username) == func.lower(username)).first().roles
        else:
            return None

    @classmethod
    def updateUserRoles(cls, id, roles):
        user: User = cls.get(id)
        if user is None:
            return None
        user.roles = []
        user.roles = roles
        db.session.commit()

    @classmethod
    def initUsers(cls):
        existingAdmin = cls.query.filter_by(username="admin").first()
        if existingAdmin is None:
            admin = User()
            admin.username = "admin"
            admin.email = "admin@cyther.net"
            admin.fName = "Admin"
            admin.lName = "Admin"
            admin.salt = str(uuid4())
            admin.password = AuthService._hash_password(
                os.getenv("ADMIN_PS"), admin.salt
            )
            admin.created = datetime.now()
            admin.lastOnline = datetime.now()
            admin.roles.append(RoleService.query.filter_by(roleName="Admin").first())
            db.session.add(admin)
        db.session.commit()

    @classmethod
    def getAll(cls):
        return cls.query.all()

    @classmethod
    def get(cls, id: str):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def delete(cls, id: str):
        row = cls.query.filter_by(id=id).first()
        roles = RoleService.getRolesForUser(id)
        userRequests = Query(UserRequest, db.session).filter_by(userId=id).all()
        for role in roles:
            db.session.delete(role)
            
        for req in userRequests:
            db.session.delete(req)
        db.session.delete(row)
        db.session.commit()
        return True

    @classmethod
    def getByUsername(cls, username: str):
        return cls.query.filter(func.lower(User.username) == func.lower(username)).first()

    @classmethod
    def getByEmail(cls, email: str) -> User | None:
        return cls.query.filter(User.email.ilike(f"%{email}%")).first()

    @classmethod
    def exists(cls, user: User):
        exist = False
        if user.email is not None:
            exist = (
                cls.query.filter(User.email.ilike(f"%{user.email}%")).first()
                is not None
            )
        if user.username is not None and not exist:
            exist = (
                cls.query.filter(func.lower(User.username) == func.lower(user.username)).first()
                is not None
            )
        return exist

    @classmethod
    def updateUser(cls, id: str, user: User):
        dbUser: User = cls.query.filter_by(id=id).first()
        dbUser.username = user.username if user.username is not None else dbUser.username
        dbUser.email = user.email if user.email is not None else dbUser.email
        dbUser.fName = user.fName if user.fName is not None else dbUser.fName
        dbUser.lName = user.lName if user.lName is not None else dbUser.lName
        dbUser.lastOnline = datetime.now()
        db.session.commit()

    @classmethod
    def getUserIdFor(cls, username: str) -> int:
        user = cls.getByUsername(username)
        if user is not None:
            return user.id
        return -1