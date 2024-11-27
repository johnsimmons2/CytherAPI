from api.model.user import *
from api.model.character import *
from api.model.classes import Class
from api.model.dto.characterDto import CharacterDTO, CharacterDescriptionDTO
from api.model.dto.statsheetDto import StatsheetDTO
from api.model.dto.userDto import UserDTO
from api.loghandler.logger import Logger
from sqlalchemy.orm import Query

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
    def getXPForLevel(cls, level: int):
        return cls.XP_TABLE[level][0]

    @classmethod
    def getProficiencyBonusForLevel(cls, level: int):
        return cls.XP_TABLE[level][1]

    @classmethod
    def getProficienciesForCharacter(cls, characterDto: CharacterDTO):
        Logger.debug("============Creating Proficiencies for Character.============")
        # Get the proficiencies and check if they already exist in the database
        # If they do, add them to the character
        # If they do not, create them and add them to the character
        proficiencies = []
        for prof in characterDto.proficiencies:
            proficiency = StatsheetService.getProficiencyByName(prof)
            if proficiency is None:
                Logger.debug(
                    f"Proficiency {prof} not found in database, creating it now."
                )
                proficiency = Proficiency(name=prof)
                db.session.add(proficiency)
                db.session.flush()
            proficiencies.append(proficiency)
        return proficiencies

    @classmethod
    def getSavingThrowsForCharacter(cls, characterDto: CharacterDTO):
        Logger.debug("============Creating Saving Throws for Character.============")
        savingThrows = []
        for throw in characterDto.savingThrows:
            st = StatsheetService.getSavingThrowByName(throw)
            if st is None:
                Logger.debug(
                    f"Saving throw {throw} not found in database, creating it now."
                )
                st = SavingThrow(statName=throw)
                db.session.add(st)
                db.session.flush()
            savingThrows.append(st)
        return savingThrows

    @classmethod
    def getSkillsForCharacter(cls, characterDto: CharacterDTO):
        Logger.debug("============Creating Skills for Character.============")
        skills = []
        for skillId in characterDto.skillIds:
            skill = SkillService.get(skillId)
            if skill is None:
                Logger.error(f"Skill {skillId} is not a valid skill ID.")
                continue
            Logger.debug(f"Skill proficiency [{skill.name}] added to character.")
            skills.append(skill)
        return skills

    @classmethod
    def makeStatsheetForCharacter(
        cls, characterDto: CharacterDTO, clazz: Class
    ) -> Statsheet:
        Logger.debug("============Creating Statsheet for Character.============")
        statsheetDto = characterDto.stats
        statsheet: Statsheet = Statsheet()

        statsheet.level = statsheetDto.level
        statsheet.health = statsheetDto.health

        statsheet.exp = cls.getXPForLevel(statsheetDto.level)
        Logger.debug(
            f"Statsheet EXP: {statsheet.exp}, Level: {statsheet.level}, Proficiency Bonus: {cls.getProficiencyBonusForLevel(statsheet.level)}"
        )

        # Make Hitdice for character
        hitdice = Hitdice()
        diceNum = None
        if characterDto.hitDiceShape is not None:
            diceNum = characterDto.hitDiceShape
        else:
            diceNum = clazz.classTable.hitDice
        match diceNum:
            case 4:
                hitdice.d4 = statsheet.level  # Currently not multiclass supported
            case 6:
                hitdice.d6 = statsheet.level
            case 8:
                hitdice.d8 = statsheet.level
            case 10:
                hitdice.d10 = statsheet.level
            case 12:
                hitdice.d12 = statsheet.level

        db.session.add(hitdice)
        db.session.flush()

        statsheet.hitdice = hitdice
        Logger.debug(
            f"Hitdice added for character: {statsheet.level}d{diceNum}, HP: {statsheet.health}"
        )
        # Assign proficiencies, skills, etc

        proficiencies = cls.getProficienciesForCharacter(characterDto)
        savingThrows = cls.getSavingThrowsForCharacter(characterDto)
        skills = cls.getSkillsForCharacter(characterDto)
        spellbook = SpellbookService.createSpellbookForCharacter(characterDto)

        statsheet.proficiencies = proficiencies
        statsheet.savingThrows = savingThrows
        statsheet.skills = skills
        statsheet.spellbook = spellbook

        # Callout to create spellbook for statsheet
        statsheet.strength = statsheetDto.strength
        statsheet.charisma = statsheetDto.charisma
        statsheet.intelligence = statsheetDto.intelligence
        statsheet.wisdom = statsheetDto.wisdom
        statsheet.constitution = statsheetDto.constitution
        statsheet.dexterity = statsheetDto.dexterity
        statsheet.type = 0

        db.session.add(statsheet)
        db.session.flush()

        return statsheet

    @classmethod
    def makeCharacterDescriptionForCharacter(cls, description: CharacterDescriptionDTO):
        characterDescription = CharacterDescription()
        characterDescription.age = description.age
        characterDescription.height = description.height
        characterDescription.weight = description.weight
        characterDescription.eyes = description.eyes
        characterDescription.skin = description.skin
        characterDescription.hair = description.hair
        characterDescription.background = description.background
        characterDescription.appearance = description.appearance
        characterDescription.bonds = description.bonds
        characterDescription.ideals = description.ideals
        characterDescription.personality = description.personality
        characterDescription.flaws = description.flaws
        characterDescription.religion = description.religion

        db.session.add(characterDescription)
        db.session.flush()

        return characterDescription

    @classmethod
    def createCharacter(cls, characterDto: CharacterDTO, user: UserDTO):
        Logger.debug("============Creating Character.============")
        # Errors to return if something goes wrong
        # The ID of the character once created
        resultId = None
        # Who will own this character
        user = None
        character = Character()

        character.name = characterDto.name

        if cls.query.filter_by(name=characterDto.name).first():
            raise Exception("Character with this name already exists")

        character.type = characterDto.type
        character.speed = characterDto.speed
        character.languages = characterDto.languages

        race = RaceService.get(characterDto.raceId)
        if race == None:
            raise Exception("Race did not match any ID")

        clazz = ClassService.get(characterDto.classId)
        if clazz == None:
            raise Exception("Class did not match any ID")

        subclazz = ClassService.getSubclass(characterDto.subclassId)
        if subclazz == None:
            raise Exception("Subclass did not match any ID")

        # TODO Check if subclass and add it

        character.race = race
        character.class_ = clazz
        character.subclass_ = subclazz

        Logger.debug("Creating character " + characterDto.name)
        Logger.debug(f"Race: {character.race.name}, Class: {character.class_.name}")

        statsheet = cls.makeStatsheetForCharacter(characterDto, clazz)
        characterDescription = cls.makeCharacterDescriptionForCharacter(characterDto.description)

        character.statsheet = statsheet
        character.characterDescription = characterDescription

        # TODO: When we are running in a development mode trying to bypass auth, what account should we pull down for the username / ownership
        if characterDto.type == 0:
            # CURRENT WORKAROUND
            user = User.query.filter_by(username="admin").first()
            user.characters.append(character)

        db.session.add(character)
        db.session.commit()
        return character.id

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
