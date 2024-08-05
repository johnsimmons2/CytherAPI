import json
import os
import hashlib
from api.model.dto.characterDto import CharacterDTO
from api.model.dto.statsheetDto import StatsheetDTO
from api.model.dto.userDto import UserDTO
from api.model.spells import Spells, SpellComponents
from api.model.campaign import Campaign
from api.model.classes import *
from api.model.ext_content import Ext_Content
from api.service.ext_dbservice import Ext_ContentService
import api.service.jwthelper as jwth
from types import SimpleNamespace
from datetime import date, datetime
from uuid import uuid4
from api.model.user import *
from api.model.items import *
from api.model.character import *
from api.model.spellbook import *
from api.service.config import config
from api.loghandler.logger import Logger
from api.model import db
from sqlalchemy.orm import Query
from sqlalchemy import desc


class FeatService:
    query = Query(Feat, db.session)
    raceFeatQuery = Query(RaceFeats, db.session)
    subClassFeatQuery = Query(SubClassFeats, db.session)
    classFeatQuery = Query(ClassFeats, db.session)

    @classmethod
    def delete(cls, id: str):
        foundFeat = cls.get(id)

        if not foundFeat:
            return False
        try:
            db.session.delete(foundFeat)
            db.session.commit()
        except Exception as e:
            Logger.error(e)
            return False, [e.__str__()]
        return True, []

    @classmethod
    def getRacialFeats(cls) -> list[Feat]:
        return list(map(lambda x: cls.get(x.featId), cls.raceFeatQuery.all()))

    @classmethod
    def getRacialFeatsFor(cls, id: str):
        return list(
            map(
                lambda x: cls.get(x.featId),
                cls.raceFeatQuery.filter(RaceFeats.raceId == int(id)).all(),
            )
        )

    @classmethod
    def getAll(cls) -> list[Feat]:
        return cls.query.all()

    @classmethod
    def get(cls, id: str) -> Feat:
        return cls.query.filter(Feat.id == id).first()

    @classmethod
    def getMultiple(cls, ids: list[str]) -> list[Feat]:
        print(ids)
        return list(map(lambda x: cls.get(x), ids))

    @classmethod
    def getByName(cls, name: str) -> Feat:
        return cls.query.filter_by(name=name).first()

    @classmethod
    def update(cls, id: int, feat: Feat) -> tuple[Feat | None, list[str]]:
        foundFeat = cls.get(id)
        if foundFeat is not None:
            if feat.name is not None:
                foundFeat.name = feat.name
            if feat.description is not None:
                foundFeat.description = feat.description
            if feat.prerequisite is not None:
                foundFeat.prerequisite = feat.prerequisite
            db.session.commit()
            return foundFeat, []
        return None, ["Could not find a feat with the given ID"]

    @classmethod
    def createFeat(cls, feat: Feat) -> tuple[Feat | None, list[str]]:
        if cls.getByName(feat.name) is not None:
            return None, ["A feat by this name already exists."]

        newFeat = Feat()
        newFeat.name = feat.name
        newFeat.description = feat.description
        newFeat.prerequisite = feat.prerequisite

        db.session.add(feat)
        db.session.commit()
        Logger.success("Creating a new feat with name: " + feat.name)
        return newFeat, []


class CampaignService:
    query = Query(Campaign, db.session)

    @classmethod
    def get(cls, id: str):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def getAll(cls):
        return cls.query.all()

    @classmethod
    def getActive(cls):
        return cls.query.filter_by(active=True).all()

    @classmethod
    def create(cls, campaign: Campaign):
        campaign.active = True
        campaign.created = date.today()
        campaign.updated = date.today()

        db.session.add(campaign)
        db.session.commit()
        return campaign

    @classmethod
    def updateCampaign(cls, id: str, campaign: Campaign):
        dbCampaign: Campaign = cls.query.filter_by(id=id).first()
        dbCampaign.name = (
            campaign.name if campaign.name is not None else dbCampaign.name
        )
        dbCampaign.description = (
            campaign.description
            if campaign.description is not None
            else dbCampaign.description
        )
        dbCampaign.updated = date.today()
        db.session.commit()

    @classmethod
    def delete(cls, id: str):
        campaign: Campaign = cls.query.filter_by(id=id).first()

        if campaign is None:
            return False
        campaign.active = False
        db.session.commit()
        return True

    @classmethod
    def getCharactersByCampaignID(cls, id: str):
        return cls.query.filter_by(id=id).first().characters

    @classmethod
    def updateCampaignCharacters(cls, id: str, characters: list[Character]):
        campaign: Campaign = cls.query.filter_by(id=id).first()
        if campaign is None:
            return False
        campaign.characters = characters
        db.session.commit()
        return True


class AuthService:
    # Adds the current lowest level Role to the user if they have no roles.
    @classmethod
    def addDefaultRole(cls, user):
        roles = Query(UserRole, db.session).filter_by(userId=user.id).all()
        if roles is None or roles == []:
            user.roles.append(
                Query(Role, db.session).order_by(desc(Role.level)).first()
            )
            db.session.commit()

    @classmethod
    def register_user(cls, user: User):
        salt = str(uuid4())
        nUser = User()
        nUser.salt = salt
        nUser.password = cls._hash_password(user.password, salt)
        nUser.username = user.username

        nUser.email = user.email
        nUser.fName = user.fName
        nUser.lName = user.lName

        nUser.created = datetime.now()
        nUser.lastOnline = datetime.now()

        db.session.add(nUser)
        cls.addDefaultRole(nUser)
        db.session.commit()
        return nUser

    @classmethod
    def _hash_password(cls, password: str, salt: str) -> str:
        secret = config("security")
        try:
            sha = hashlib.sha256()
            sha.update(password.encode(encoding="UTF-8", errors="strict"))
            sha.update(":".encode(encoding="UTF-8"))
            sha.update(salt.encode(encoding="UTF-8", errors="strict"))
            sha.update(secret["usersecret"].encode(encoding="UTF-8", errors="strict"))
            return sha.hexdigest()
        except Exception as error:
            Logger.error(error)
        return None

    @classmethod
    def authenticate_user(cls, inputUser: User) -> User | None:
        query = Query(User, db.session)
        user = None

        secret = inputUser.password
        if inputUser.username is not None:
            user = query.filter(User.username.ilike(f"%{inputUser.username}%")).first()
        elif inputUser.email is not None:
            user = query.filter_by(email=inputUser.email).first()
        else:
            Logger.error(
                "Attempted to authenticate without email or username provided, or both were provided."
            )
            return None

        if not user:
            Logger.error("no user")
            return None

        if AuthService._hash_password(secret, user.salt) == user.password:
            user.lastOnline = datetime.now()
            cls.addDefaultRole(user)
            db.session.commit()
            return jwth.create_token(user)
        else:
            Logger.error("Incorrect password!")
            return None


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
            return cls.query.filter(User.username.ilike(f"%{username}%")).first().roles
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
        db.session.delete(row)
        db.session.commit()
        return True

    @classmethod
    def getByUsername(cls, username: str):
        return cls.query.filter(User.username.ilike(f"%{username}%")).first()

    @classmethod
    def exists(cls, user: User):
        if user.username is not None:
            return (
                cls.query.filter(User.username.ilike(f"%{user.username}%")).first()
                is not None
            )
        elif user.email is not None:
            return (
                cls.query.filter(User.email.ilike(f"%{user.email}%")).first()
                is not None
            )
        else:
            return False

    @classmethod
    def updateUser(cls, id: str, user: User):
        Logger.debug("Updating user with id: " + id)
        dbUser: User = cls.query.filter_by(id=id).first()
        dbUser.username = (
            user.username if user.username is not None else dbUser.username
        )
        dbUser.email = user.email if user.email is not None else dbUser.email
        dbUser.fName = user.fName if user.fName is not None else dbUser.fName
        dbUser.lName = user.lName if user.lName is not None else dbUser.lName
        dbUser.lastOnline = datetime.now()

        db.session.commit()


class ItemsService:
    @classmethod
    def getAll(cls):
        return Items.query.all()

    @classmethod
    def get(cls, id: str):
        return Items.query.filter_by(id=id).first()
