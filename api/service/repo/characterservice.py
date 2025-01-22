from api.model.user import *
from api.model.character import *
from api.model.classes import Class
from api.model.dto.characterDto import CharacterDTO, CharacterDescriptionDTO
from api.model.dto.statsheetDto import StatsheetDTO
from api.model.dto.userDto import UserDTO
from api.loghandler.logger import Logger
from sqlalchemy.orm import Query

from api.service.dbservice import UserService
from api.service.repo.raceservice import RaceService
from api.service.repo.classservice import ClassService
from api.service.repo.skillservice import SkillService
from api.service.repo.spellbookservice import SpellbookService
from api.service.repo.statsheetservice import StatsheetService


class CharacterService:
    query = db.Query(Character, db.session)
    XP_TABLE = {
        1: (0, 2),
        2: (300, 2),
        3: (900, 2),
        4: (2700, 2),
        5: (6500, 3),
        6: (14000, 3),
        7: (23000, 3),
        8: (34000, 3),
        9: (48000, 4),
        10: (64000, 4),
        11: (85000, 4),
        12: (100000, 4),
        13: (120000, 5),
        14: (140000, 5),
        15: (165000, 5),
        16: (195000, 5),
        17: (225000, 6),
        18: (265000, 6),
        19: (305000, 6),
        20: (355000, 6),
    }

    @classmethod
    def getOwnerIdFor(cls, characterId: str):
        userCharacter: UserCharacters = Query(UserCharacters, db.session).filter_by(characterId=characterId).first()
        if userCharacter is None:
            return None
        return userCharacter.userId

    @classmethod
    def getOwnerUsernameFor(cls, characterId: str):
        user = (
            db.session.query(User)
            .join(UserCharacters, User.id == UserCharacters.userId)
            .filter(UserCharacters.characterId == characterId)
            .first()
        )
        if user is None:
            return None
        return user.username

    @classmethod
    def updateUserCharacters(cls, userId: str, characterId: str):
        user = UserService.get(userId)
        character = cls.get(characterId)
        if user is None:
            raise Exception("User not found")
        if character is None:
            raise Exception("Character not found")
        userCharacter: UserCharacters = Query(UserCharacters, db.session).filter_by(userId=userId).first()
        if userCharacter is None:
            Logger.debug(f"Adding character {characterId} to user {userId}")
            userCharacter = UserCharacters(userId=userId, characterId=characterId)
            db.session.add(userCharacter)
        else:
            Logger.debug(f"Updating character {characterId} for user {userId}")
            userCharacter.characterId = characterId
            userCharacter.userId = userId
        db.session.commit()

    @classmethod
    def getXPForLevel(cls, level: int):
        return cls.XP_TABLE[level][0]

    @classmethod
    def getProficiencyBonusForLevel(cls, level: int):
        return cls.XP_TABLE[level][1]

    @classmethod
    def getCharacterByName(cls, characterName):
        return cls.query.filter_by(name=characterName).first()
    
    @classmethod
    def getAll(cls):
        return Query(Character, db.session).all()

    @classmethod
    def getAllPlayerCharacters(cls):
        query = Query(Character, db.session)
        return query.filter_by(isNpc=False).all()

    @classmethod
    def getAllNPCs(cls):
        query = Query(Character, db.session)
        return query.filter_by(isNpc=True).all()

    @classmethod
    def getCharactersByUserId(cls, id: str):
        query = Query(Character, db.session) \
            .join(UserCharacters, UserCharacters.characterId == Character.id) \
            .filter(UserCharacters.userId == id)
        return query.all()
    
    @classmethod
    def getUserCharactersMappings(cls):
        return Query(UserCharacters, db.session).all()

    @classmethod
    def get(cls, id: str):
        return cls.query.filter_by(id=id).first()
