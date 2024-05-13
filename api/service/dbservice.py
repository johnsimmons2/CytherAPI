import json
import os
import hashlib
from api.model.spells import Spells
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
from sqlalchemy.orm import sessionmaker, Query
from sqlalchemy import desc


class StatsheetService:
    query = db.Query(Statsheet, db.session)
    stQuery = db.Query(SavingThrow, db.session)

    @classmethod
    def initSavingThrows(cls):
        cls.stQuery.filter_by(statName='Strength').first() or db.session.add(SavingThrow(statName='Strength'))
        cls.stQuery.filter_by(statName='Dexterity').first() or db.session.add(SavingThrow(statName='Dexterity'))
        cls.stQuery.filter_by(statName='Constitution').first() or db.session.add(SavingThrow(statName='Constitution'))
        cls.stQuery.filter_by(statName='Intelligence').first() or db.session.add(SavingThrow(statName='Intelligence'))
        cls.stQuery.filter_by(statName='Wisdom').first() or db.session.add(SavingThrow(statName='Wisdom'))
        cls.stQuery.filter_by(statName='Charisma').first() or db.session.add(SavingThrow(statName='Charisma'))
        db.session.commit()

    @classmethod
    def getProfiencyBonus(cls, level: int) -> int:
        if level < 5:
            return 2
        elif level < 9:
            return 3
        elif level < 13:
            return 4
        elif level < 17:
            return 5
        elif level < 21:
            return 6
        else:
            return 7

class SkillService:
    query = db.Query(Skill, db.session)

    @classmethod
    def initBaseSkills(cls):
        cls.query.filter_by(name='Athletics').first() or db.session.add(Skill(name='Athletics', description='Strength (Athletics)'))
        cls.query.filter_by(name='Acrobatics').first() or db.session.add(Skill(name='Acrobatics', description='Dexterity (Acrobatics)'))
        cls.query.filter_by(name='Sleight of Hand').first() or db.session.add(Skill(name='Sleight of Hand', description='Dexterity (Sleight of Hand)'))
        cls.query.filter_by(name='Stealth').first() or db.session.add(Skill(name='Stealth', description='Dexterity (Stealth)'))
        cls.query.filter_by(name='Arcana').first() or db.session.add(Skill(name='Arcana', description='Intelligence (Arcana)'))
        cls.query.filter_by(name='History').first() or db.session.add(Skill(name='History', description='Intelligence (History)'))
        cls.query.filter_by(name='Investigation').first() or db.session.add(Skill(name='Investigation', description='Intelligence (Investigation)'))
        cls.query.filter_by(name='Nature').first() or db.session.add(Skill(name='Nature', description='Intelligence (Nature)'))
        cls.query.filter_by(name='Religion').first() or db.session.add(Skill(name='Religion', description='Intelligence (Religion)'))
        cls.query.filter_by(name='Animal Handling').first() or db.session.add(Skill(name='Animal Handling', description='Wisdom (Animal Handling)'))
        cls.query.filter_by(name='Insight').first() or db.session.add(Skill(name='Insight', description='Wisdom (Insight)'))
        cls.query.filter_by(name='Medicine').first() or db.session.add(Skill(name='Medicine', description='Wisdom (Medicine)'))
        cls.query.filter_by(name='Perception').first() or db.session.add(Skill(name='Perception', description='Wisdom (Perception)'))
        cls.query.filter_by(name='Survival').first() or db.session.add(Skill(name='Survival', description='Wisdom (Survival)'))
        cls.query.filter_by(name='Deception').first() or db.session.add(Skill(name='Deception', description='Charisma (Deception)'))
        cls.query.filter_by(name='Intimidation').first() or db.session.add(Skill(name='Intimidation', description='Charisma (Intimidation)'))
        cls.query.filter_by(name='Performance').first() or db.session.add(Skill(name='Performance', description='Charisma (Performance)'))
        cls.query.filter_by(name='Persuasion').first() or db.session.add(Skill(name='Persuasion', description='Charisma (Persuasion)'))
        db.session.commit()

    @classmethod
    def getAll(cls):
        return cls.query.all()

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
    def getRacialFeats(cls) -> [Feat]:
        return list(map(lambda x: cls.get(x.featId), cls.raceFeatQuery.all()))

    @classmethod
    def getRacialFeatsFor(cls, id: str):
        return list(map(lambda x: cls.get(x.featId), cls.raceFeatQuery.filter(RaceFeats.raceId == int(id)).all()))

    @classmethod
    def getAll(cls) -> [Feat]:
        return cls.query.all()

    @classmethod
    def get(cls, id: str) -> Feat:
        return cls.query.filter(Feat.id == id).first()

    @classmethod
    def getMultiple(cls, ids: [str]) -> [Feat]:
        print(ids)
        return list(map(lambda x: cls.get(x), ids))

    @classmethod
    def getByName(cls, name: str) -> Feat:
        return cls.query.filter_by(name=name).first()

    @classmethod
    def update(cls, id: int, feat: Feat) -> (Feat | None, [str]):
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
    def createFeat(cls, feat: Feat) -> (Feat | None, [str]):
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

class RaceService:
    query = Query(Race, db.session)
    raceFeatQuery = Query(RaceFeats, db.session)
    featQuery = Query(Feat, db.session)

    @classmethod
    def delete(cls, id: int):
        foundClass = cls.query.filter(Race.id == id).first()

        if not foundClass:
            return False
        db.session.delete(foundClass)
        db.session.commit()
        return True

    # Initialize by gathering races from API.
    @classmethod
    def getRacesOnline(cls):
        raceRefresh: Ext_Content = Ext_ContentService.getByKey('race_refresh')
        if raceRefresh is None:
            # Trigger actual refresh
            # Create the
            # refresh key with the current time
            Ext_ContentService.add(Ext_Content(**{
                'key': 'race_refresh',
                'name': 'Last refresh time for Race table',
                'content': str(datetime.now().timestamp())
            }))
            cls._refresh()
        else:
            # Check if the refresh is older than 1 day
            # If it is, trigger refresh
            # If not, do nothing
            if ((datetime.now().timestamp()) - float(raceRefresh.content)) >= 60 * 60 * 24:
                cls._refresh()

    @classmethod
    def _refresh(cls):
        from api.service.dnd5eapiservice import Dnd5eAPIService
        Dnd5eAPIService.getRaces()
        Logger.debug("Refreshing the race database")

    @classmethod
    def getAll(cls) -> [Race]:
        cls.getRacesOnline()
        return cls.query.all()

    @classmethod
    def get(cls, id: str) -> Race:
        return cls.query.filter_by(id=id).first()

    @classmethod
    def getByName(cls, name: str) -> Race:
        return cls.query.filter(Race.name.ilike(f"%{name}%")).first()

    @classmethod
    def update(cls, race: Race, feats: List[Feat] | None) -> (int, [str]):
        foundRace: Race = cls.query.filter(Race.id == race.id).first()
        success = False
        errors = []

        if foundRace is not None:
            if race.name is not None:
                foundRace.name = race.name
            if race.description is not None:
                foundRace.description = race.description
            if race.size is not None:
                foundRace.size = race.size
            if race.languages is not None:
                foundRace.languages = race.languages
            if race.alignment is not None:
                foundRace.alignment = race.alignment
            if feats is not None and len(feats) > 0:
                foundRace.feats = feats
            db.session.add(foundRace)
            success = True
        else:
            errors.append("Could not find a race with the given ID")

        db.session.commit()
        return success, errors

    @classmethod
    def createRace(cls, race: Race) -> (int, [str]):
        if cls.getByName(race.name) is not None:
            return -1, ["A race by this name already exists."]

        newRace = Race()
        newRace.name = race.name
        newRace.languages = race.languages
        newRace.alignment = race.alignment
        newRace.description = race.description
        newRace.feats = race.feats

        db.session.add(newRace)
        db.session.commit()
        return newRace.id, True

    @classmethod
    def getRaceFeats(cls, raceName: str) -> [Feat]:
        race = cls.getByName(raceName)
        if race is not None:
            raceFeats = cls.raceFeatQuery.filter_by(raceId=race.id).all()
            feats = map(lambda x: cls.featQuery.filter_by(id=x.featId).first(), raceFeats)
            return list(feats)
        return []

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
        dbCampaign.name = campaign.name if campaign.name is not None else dbCampaign.name
        dbCampaign.description = campaign.description if campaign.description is not None else dbCampaign.description
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

class ClassService:
    query = Query(Class, db.session)
    querySubclass = Query(Subclass, db.session)
    queryCSC = Query(ClassSubclasses, db.session)

    @classmethod
    def getClassSubclasses(cls, id):
        return cls.query.filter(Class.id == id).first().subclasses

    # Initialize by gathering races from API.
    @classmethod
    def getClassesOnline(cls):
        classRefresh: Ext_Content = Ext_ContentService.getByKey('class_refresh')
        if classRefresh is None:
            # Trigger actual refresh
            # Create the
            # refresh key with the current time
            Ext_ContentService.add(Ext_Content(**{
                'key': 'class_refresh',
                'name': 'Last refresh time for Class table',
                'content': str(datetime.now().timestamp())
            }))
            cls._refresh()
        else:
            # Check if the refresh is older than 1 day
            # If it is, trigger refresh
            # If not, do nothing
            if ((datetime.now().timestamp()) - float(classRefresh.content)) >= 60 * 60 * 24:
                pass
            cls._refresh()

    @classmethod
    def getSubclasses(cls, classId: str):
        return cls.querySubclass.filter_by(classId=classId).all()

    @classmethod
    def getClassTable(cls, classId: str):
        return cls.queryClassTable.filter_by(classId=classId).first()

    # TODO: Long term project, get this information filled out automatically. For now we pause on the automatic compilation of classes to focus on getting a product out.
    @classmethod
    def updateClassTable(cls, classId, classTableJson):
        classTable = cls.getClassTable(classId)
        if classTable is None:
            classTable = ClassTable()
        if 'profBonus' in classTableJson:
            classTable.profBonus = classTableJson['profBonus']
        if 'cantripsKnown' in classTableJson:
            classTable.cantripsKnown = classTableJson['cantripsKnown']
        if 'spellsKnown' in classTableJson:
            classTable.spellsKnown = classTableJson['spellsKnown']
        if 'level1SpellSlots' in classTableJson:
            classTable.level1SpellSlots = classTableJson['level1SpellSlots']
        if 'level2SpellSlots' in classTableJson:
            classTable.level2SpellSlots = classTableJson['level2SpellSlots']
        if 'level3SpellSlots' in classTableJson:
            classTable.level3SpellSlots = classTableJson['level3SpellSlots']
        if 'level4SpellSlots' in classTableJson:
            classTable.level4SpellSlots = classTableJson['level4SpellSlots']
        if 'level5SpellSlots' in classTableJson:
            classTable.level5SpellSlots = classTableJson['level5SpellSlots']
        if 'level6SpellSlots' in classTableJson:
            classTable.level6SpellSlots = classTableJson['level6SpellSlots']
        if 'level7SpellSlots' in classTableJson:
            classTable.level7SpellSlots = classTableJson['level7SpellSlots']
        if 'level8SpellSlots' in classTableJson:
            classTable.level8SpellSlots = classTableJson['level8SpellSlots']
        if 'level9SpellSlots' in classTableJson:
            classTable.level9SpellSlots = classTableJson['level9SpellSlots']
        db.session.add(classTable)
        db.session.commit()
        return (True, None)
    def delete(cls, classId):
        foundClass = cls.get(classId)

        if not foundClass:
            return False
        try:
            db.session.delete(foundClass)
            db.session.commit()
        except Exception as e:
            Logger.error(e)
            return False, [e.__str__()]
        return True, []

    @classmethod
    def createClass(cls, clazz: Class):
        foundClass = cls.getByName(clazz.name)
        if foundClass is not None:
            return None, ["A class by this name already exists."]

        newClass = Class()
        newClass.description = clazz.description
        newClass.name = clazz.name
        newClass.spellCastingAbility = clazz.spellCastingAbility
        db.session.add(newClass)
        db.session.commit()
        return newClass, []

    @classmethod
    def update(cls, id: int, clazz: Class):
        foundClass = cls.get(id)
        if foundClass:
            if clazz.name:
                foundClass.name = clazz.name
            if clazz.description:
                foundClass.description = clazz.description

            # Spellcasting is nullable, if nothing is sent, it will become nothing.
            foundClass.spellCastingAbility = clazz.spellCastingAbility
            db.session.add(foundClass)
            db.session.commit()
            return foundClass, []
        return None, ["Could not find a class with the given ID"]


    @classmethod
    def _refresh(cls):
        from api.service.dnd5eapiservice import Dnd5eAPIService
        Logger.debug("Refreshing the class database")
        Dnd5eAPIService.getClasses()

    @classmethod
    def getSubclassByName(cls, subclassName: str):
        return cls.querySubclass.filter(Subclass.name.ilike(f"%{subclassName}%")).first()

    @classmethod
    def getByName(cls, className: str):
        return cls.query.filter(Class.name.ilike(f"%{className}%")).first()

    @classmethod
    def getAll(cls):
        cls.getClassesOnline()
        return cls.query.all()

    @classmethod
    def get(cls, id: str):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def getSubclass(cls, id: str):
        return cls.querySubclass.filter_by(id=id).first()

class AuthService:
    # Adds the current lowest level Role to the user if they have no roles.
    @classmethod
    def addDefaultRole(cls, user):
        roles = Query(UserRole, db.session).filter_by(userId=user.id).all()
        if roles is None or roles == []:
            user.roles.append(Query(Role, db.session).order_by(desc(Role.level)).first())
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
    def authenticate_user(cls, inputUser: User) -> User | None:
        query = Query(User, db.session)
        user = None

        secret = inputUser.password
        if inputUser.username is not None:
            user = query.filter(User.username.ilike(f"%{inputUser.username}%")).first()
        elif inputUser.email is not None:
            user = query.filter_by(email=inputUser.email).first()
        else:
            Logger.error('Attempted to authenticate without email or username provided, or both were provided.')
            return None

        if not user:
            Logger.error('no user')
            return None

        if AuthService._hash_password(secret, user.salt) == user.password:
            user.lastOnline = datetime.now()
            cls.addDefaultRole(user)
            db.session.commit()
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
    def get(cls, id: str):
        return cls.query.filter_by(id=id).first()

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
      existingAdmin = cls.query.filter_by(username='admin').first()
      if existingAdmin is None:
        admin = User()
        admin.username = 'admin'
        admin.email = 'admin@cyther.net'
        admin.fName = 'Admin'
        admin.lName = 'Admin'
        admin.salt = str(uuid4())
        admin.password = AuthService._hash_password(os.getenv('ADMIN_PS'), admin.salt)
        admin.created = datetime.now()
        admin.lastOnline = datetime.now()
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
            return cls.query.filter(User.username.ilike(f"%{user.username}%")).first() is not None
        elif user.email is not None:
            return cls.query.filter(User.email.ilike(f"%{user.email}%")).first() is not None
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
        dbUser.lastOnline = datetime.now()

        db.session.commit()

class SpellService:
    spellQuery = Query(Spells, db.session)

    @classmethod
    def getAll(cls):
        return cls.spellQuery.all()

    @classmethod
    def get(cls, id: str):
        return cls.spellQuery.filter_by(id=id).first()

    @classmethod
    def createSpell(cls, spell: Spells):
        if cls.spellQuery.filter_by(name=spell.name).first() is not None:
            return -1, ["A spell by this name already exists."]

        newSpell = Spells()
        newSpell.castingTime = spell.castingTime
        newSpell.description = spell.description
        newSpell.duration = spell.duration
        newSpell.level = spell.level
        newSpell.material = spell.material
        newSpell.name = spell.name
        newSpell.school = spell.school
        newSpell.type = spell.type
        newSpell.verbal = spell.verbal
        newSpell.somatic = spell.somatic
        newSpell.ritual = spell.ritual

        db.session.add(newSpell)
        db.session.commit()
        return newSpell.id, []

class SpellbookService:
    @classmethod
    def getAll(cls):
        return Spellbook.query.all()

    @classmethod
    def get(cls, id: str):
        return Spellbook.query.filter_by(id=id).first()

class CharacterService:
    @classmethod
    def createSpellbookForCharacter(cls):
      pass

    @classmethod
    def makeStatsheetForCharacter(cls, stats) -> (Statsheet, list[str]):
        errors = []
        statsheet: Statsheet = Statsheet()
        if 'str' not in stats:
            errors.append('Strength [str] is required.')
        else:
            statsheet.strength = stats['str']
        if 'cha' not in stats:
            errors.append('Charisma [cha] is required.')
        else:
            statsheet.charisma = stats['cha']
        if 'int' not in stats:
            errors.append('Intelligence [int] is required.')
        else:
            statsheet.intelligence = stats['int']
        if 'wis' not in stats:
            errors.append('Wisdom [wis] is required.')
        else:
            statsheet.wisdom = stats['wis']
        if 'con' not in stats:
            errors.append('Constitution [con] is required.')
        else:
            statsheet.constitution = stats['con']
        if 'dex' not in stats:
            errors.append('Dexterity [dex] is required.')
        else:
            statsheet.dexterity = stats['dex']

        if 'exp' not in stats:
            statsheet.exp = 0
        else:
            statsheet.exp = stats['exp']

        if 'level' not in stats:
            statsheet.level = 1
        else:
            statsheet.level = stats['level']

        if 'health' not in stats:
            # TODO: Calculate health based on class and level
            errors.append('Base health [health] is required.')
        else:
            statsheet.health = stats['health']

        return (statsheet, errors)

    @classmethod
    def createCharacter(cls, characterJson):
        # Errors to return if something goes wrong
        errors = []
        # The ID of the character once created
        resultId = None
        # Who will own this character
        user = None
        character = Character()

        if 'name' not in characterJson:
            errors.append('Name is required.')
            return (resultId, errors)
        character.name = characterJson['name']

        if 'race' not in characterJson:
            errors.append('Race is required.')
            return (resultId, errors)
        character.race = characterJson['race']

        if 'userId' not in characterJson:
            # Check token to see if they are an admin. If they are, this is an NPC. Otherwise, attach to userId.
            if jwth.has_role_level(0):
                character.type = 1
            else:
                character.type = 0
                user: User = UserService.getByUsername(jwth.get_username())
        else:
            character.type = 0
            user: User = UserService.get(characterJson['userId'])

        if 'stats' not in characterJson:
            errors.append('Stats are required [str, cha, int, wis, con, dex].')
            return (resultId, errors)
        else:
            stats = characterJson['stats']
            (x, y) = cls.makeStatsheetForCharacter(stats)
            statsheet: Statsheet = x
            errs: list[str] = y

            if len(errs) > 0:
                errors.extend(errs)
            else:
                statsheet.character = character

                if 'classId' in characterJson:
                    clazz = ClassService.get(characterJson['classId'])
                    if clazz is None:
                        errors.append('Class with id ' + str(characterJson['classId']) + ' does not exist.')
                        return (resultId, errors)
                    statsheet.clazz = clazz
                if 'subclassId' in characterJson:
                    subclass = ClassService.getSubclass(characterJson['subclassId'])
                    if subclass is None:
                        errors.append('Subclass with id ' + str(characterJson['subclassId']) + ' does not exist.')
                        return (resultId, errors)
                    statsheet.subclass = subclass
                # TODO: Calculate the spellbook based on the user's level and class
                # TODO: Duplicate the statsheet, currently it points to the same stat sheet.
                # statsheet.spellbook = cls.createSpellbookForCharacter()
                character.statsheet = statsheet
                character.basestatsheet = statsheet

        # If this character was meant to be attached to a user
        if user is not None and character.type == 0:
            user.characters.append(character)

        db.session.add(character)
        db.session.add(statsheet)
        db.session.commit()
        return (character.id, errors)

    @classmethod
    def updateCharacter(cls, id: str, characterJson):
        errors = []
        success = True

        character: Character = CharacterService.get(id)
        if character is None:
            errors.append("Could not find a character with the given ID.")
            success = False
        else:
            if 'name' in characterJson:
                character.name = characterJson['name']

            if 'race' in characterJson:
                character.race = characterJson['race']

            if 'stats' in characterJson:
                stats = characterJson['stats']
                statsheet: Statsheet = character.statsheet

                if 'classId' in characterJson:
                    clazz = ClassService.get(characterJson['classId'])
                    if clazz is None:
                        success = False
                        errors.append('Class with id ' + str(characterJson['classId']) + ' does not exist.')
                    else:
                        statsheet.clazz = clazz
                if 'subclassId' in characterJson:
                    subclass = ClassService.getSubclass(characterJson['subclassId'])
                    if subclass is None:
                        success = False
                        errors.append('Subclass with id ' + str(characterJson['subclassId']) + ' does not exist.')
                    else:
                        statsheet.subclass = subclass

                if 'str' in stats:
                    statsheet.strength = stats['str']
                if 'cha' in stats:
                    statsheet.charisma = stats['cha']
                if 'int' in stats:
                    statsheet.intelligence = stats['int']
                if 'wis' in stats:
                    statsheet.wisdom = stats['wis']
                if 'con' in stats:
                    statsheet.constitution = stats['con']
                if 'dex' in stats:
                    statsheet.dexterity = stats['dex']
                if 'exp' in stats:
                    statsheet.exp = stats['exp']
                if 'level' in stats:
                    statsheet.level = stats['level']
                if 'health' in stats:
                    statsheet.health = stats['health']
        db.session.commit()
        return (success, errors)


    @classmethod
    def getAll(cls):
        return Query(Character, db.session).all()

    @classmethod
    def getAllPlayerCharacters(cls):
        query = Query(Character, db.session)
        return query.filter_by(type=0).all()

    @classmethod
    def getAllNPCs(cls):
        query = Query(Character, db.session)
        return query.filter_by(type=1).all()

    @classmethod
    def getCharactersByUserId(cls, id: str):
        query = Query(Character, db.session).join(User.characters)
        return query.all()

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
