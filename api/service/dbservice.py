import json
import os
import hashlib
import api.service.jwthelper as jwth
from types import SimpleNamespace
from datetime import date
from uuid import uuid4
from api.model.user import *
from api.model.items import *
from api.model.character import *
from api.model.spellbook import *
from api.service.config import config
from api.loghandler.logger import Logger
from api.model import db
from sqlalchemy.orm import sessionmaker, Query
from sqlalchemy import desc


class AuthService:
    @classmethod
    def addDefaultRole(cls, user):
        roles = Query(UserRole, db.session).filter_by(userId=user.id).all()
        if roles is None or roles == []:
            user.roles.append(Query(Role, db.session).order_by(desc(Role.level)).first())
            db.session.commit()

    @classmethod
    def register_user(cls, user: User):
        nUser = User()
        nUser.salt = str(uuid4())
        nUser.password = cls._hash_password(user.password, nUser.salt)
        nUser.created = date.today()
        nUser.lastOnline = date.today()
        nUser.username = user.username
        nUser.email = user.email
        db.session.add(nUser)
        db.session.commit()
        cls.addDefaultRole(nUser)
        return True

    @classmethod
    def _hash_password(cls, password: str, salt: str) -> str:
        secret = config('security')
        try:
            sha = hashlib.sha256()
            sha.update(password.encode(encoding = 'UTF-8', errors = 'strict'))
            sha.update(':'.encode(encoding = 'UTF-8'))
            sha.update(salt.encode(encoding = 'UTF-8', errors = 'strict'))
            sha.update(secret['usersecret'].encode(encoding = 'UTF-8', errors = 'strict'))
            return sha.hexdigest()
        except Exception as error:
            Logger.error(error)
        return None

    @classmethod
    def authenticate_user(cls, user: User) -> User | None:
        query = Query(User, db.session)
        secret = user.password
        if user.username is not None:
            user = query.filter_by(username=str.lower(user.username)).first()
        elif user.email is not None:
            user = query.filter_by(email=user.email).first()
        else:
            Logger.error('Attempted to authenticate without email or username provided, or both were provided.')
            return None
        if not user:
            Logger.error('no user')
            return None
        else:
            if AuthService._hash_password(secret, user.salt) == user.password:
                user.lastOnline = date.today()
                db.session.commit()
                cls.addDefaultRole(user)
                return jwth.create_token(user)
            else:
                Logger.error('Incorrect password!')
                return None

class RoleService:
    query = Query(Role, db.session)

    @classmethod
    def getAll(cls):
        return cls.query.all()

    @classmethod
    def roleWithLevel(cls, level: int):
        return cls.query.filter_by(level=level).first()

    @classmethod
    def initRoles(cls):
        cls.query.filter_by(roleName='Admin').first() or db.session.add(Role(roleName='Admin', level=0))
        cls.query.filter_by(roleName='Player').first() or db.session.add(Role(roleName='Player', level=1))
        cls.query.filter_by(roleName='Guest').first() or db.session.add(Role(roleName='Guest', level=2))
        db.session.commit()

class UserService:
    query = Query(User, db.session)

    @classmethod
    def getCurrentUserRoles(cls):
        username = jwth.decode_token(jwth.get_access_token())['username']
        if username is not None:
            return cls.query.filter_by(username=str.lower(username)).first().roles
        else:
            return None

    @classmethod
    def updateUserRoles(cls, id, roles):
        user = cls.get(id)
        user.roles = []
        user.roles = roles
        db.session.commit()

    @classmethod
    def initUsers(cls):
      existingAdmin = cls.query.filter_by(username='admin').first()
      if existingAdmin is None:
        admin = User()
        admin.username = 'admin'
        admin.email = 'admin@cyther.net'
        admin.fName = 'Admin'
        admin.lName = 'Admin'
        admin.salt = str(uuid4())
        admin.password = AuthService._hash_password(os.getenv('ADMIN_PS'), admin.salt)
        admin.created = date.today()
        admin.lastOnline = date.today()
        admin.roles.append(RoleService.query.filter_by(roleName='Admin').first())
        db.session.add(admin)
      db.session.commit()

    @classmethod
    def getAll(cls):
        return cls.query.all()

    @classmethod
    def get(cls, id: str):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def getByUsername(cls, username: str):
        return cls.query.filter_by(username=str.lower(username)).first()

    @classmethod
    def exists(cls, user: User):
        if user.username is not None:
            return cls.query.filter_by(username=user.username).first() is not None
        elif user.email is not None:
            return cls.query.filter_by(email=user.email).first() is not None
        else:
            return False

    @classmethod
    def updateUser(cls, id: str, user: User):
        Logger.debug('Updating user with id: ' + id)
        dbUser: User = cls.query.filter_by(id=id).first()
        dbUser.username = user.username if user.username is not None else dbUser.username
        dbUser.email = user.email if user.email is not None else dbUser.email
        dbUser.fName = user.fName if user.fName is not None else dbUser.fName
        dbUser.lName = user.lName if user.lName is not None else dbUser.lName
        dbUser.lastOnline = date.today()

        db.session.commit()


class SpellbookService:
    @classmethod
    def getAll(cls):
        return Spellbook.query.all()

    @classmethod
    def get(cls, id: str):
        return Spellbook.query.filter_by(id=id).first()

class CharacterService:
    @classmethod
    def getAll(cls):
        return Query(Character, db.session).all()

    @classmethod
    def getPlayerCharacters(cls):
        query = Query(Character, db.session)
        return query.filter_by(type=0).all()

    @classmethod
    def get(cls, id: str):
        return Query(Character, db.session).filter_by(id=id).first()

class ItemsService:
    @classmethod
    def getAll(cls):
        return Items.query.all()

    @classmethod
    def get(cls, id: str):
        return Items.query.filter_by(id=id).first()
