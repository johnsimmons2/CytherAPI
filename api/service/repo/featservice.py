from sqlalchemy.orm import Query
from api.loghandler.logger import Logger
from api.model.character import CharacterFeat
from api.model.classes import ClassFeat
from api.model.race import RaceFeat
from extensions import db
from api.model.feat import Feat, FeatEffect


class FeatService:
    query = Query(Feat, db.session)
    raceFeatQuery = Query(RaceFeat, db.session)
    classFeatQuery = Query(ClassFeat, db.session)
    characterFeatQuery = Query(CharacterFeat, db.session)

    @classmethod
    def getFeatEffectFromJSON(cls, effect: dict) -> FeatEffect:
        newEffect = FeatEffect()
        newEffect.conditionId = effect.get("conditionId")
        newEffect.vulnerableId = effect.get("vulnerableId")
        newEffect.resistantId = effect.get("resistantId")
        newEffect.immuneId = effect.get("immuneId")
        newEffect.abilityId = effect.get("abilityId")
        newEffect.abilityAdj = effect.get("abilityAdj")
        newEffect.skillId = effect.get("skillId")
        newEffect.skillAdj = effect.get("skillAdj")
        newEffect.rollAdvantage = effect.get("rollAdvantage")
        newEffect.rollDisadvantage = effect.get("rollDisadvantage")
        newEffect.rollType = effect.get("rollType")
        newEffect.requirements = effect.get("requirements")
        return newEffect

    @classmethod
    def addFeatEffect(cls, effect: FeatEffect) -> bool:
        try:
            db.session.add(effect)
            db.session.commit()
            return True
        except Exception as e:
            Logger.error(e)
            return False
    
    @classmethod
    def addFeatToClass(cls, featId: str, classId: str) -> bool:
        try:
            newFeat = ClassFeat()
            newFeat.featId = featId
            newFeat.classId = classId
            db.session.add(newFeat)
            db.session.commit()
            return True
        except Exception as e:
            Logger.error(e)
            return False
    
    @classmethod
    def addFeatToCharacter(cls, featId: str, characterId: str) -> bool:
        try:
            newFeat = CharacterFeat()
            newFeat.featId = featId
            newFeat.characterId = characterId
            db.session.add(newFeat)
            db.session.commit()
            return True
        except Exception as e:
            Logger.error(e)
            return False
    
    @classmethod
    def addFeatToRace(cls, featId: str, raceId: str) -> bool:
        try:
            newFeat = RaceFeat()
            newFeat.featId = featId
            newFeat.raceId = raceId
            db.session.add(newFeat)
            db.session.commit()
            return True
        except Exception as e:
            Logger.error(e)
            return False
    
    @classmethod
    def removeFeatFromRace(cls, featId: str, raceId: str) -> bool:
        try:
            feat = cls.raceFeatQuery.filter_by(featId=featId, raceId=raceId).first()
            db.session.delete(feat)
            db.session.commit()
            return True
        except Exception as e:
            Logger.error(e)
            return False
    
    @classmethod
    def removeFeatFromClass(cls, featId: str, classId: str) -> bool:
        try:
            feat = cls.classFeatQuery.filter_by(featId=featId, classId=classId).first()
            db.session.delete(feat)
            db.session.commit()
            return True
        except Exception as e:
            Logger.error(e)
            return False
        
    @classmethod
    def removeFeatFromCharacter(cls, featId: str, characterId: str) -> bool:
        try:
            feat = cls.characterFeatQuery.filter_by(featId=featId, characterId=characterId).first()
            db.session.delete(feat)
            db.session.commit()
            return True
        except Exception as e:
            Logger.error(e)
            return False

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
        return list(
            map(
                lambda x: cls.get(x.featId),
                cls.raceFeatQuery.all()
            )
        )
    
    @classmethod
    def deleteFeatEffect(cls, effectId: str) -> bool:
        try:
            effect = cls.getFeatEffect(effectId)
            db.session.delete(effect)
            db.session.commit()
            return True
        except Exception as e:
            Logger.error(e)
            return False
    
    @classmethod
    def getFeatEffect(cls, featEffectId: str) -> FeatEffect:
        return cls.query.filter_by(id=featEffectId).first()

    @classmethod
    def getClassFeats(cls) -> list[Feat]:
        return list(
            map(
                lambda x: cls.get(x.featId),
                cls.query.filter(ClassFeat.classId.isnot(None)).all(),
            )
        )

    @classmethod
    def getRacialFeatsFor(cls, id: str):
        return list(
            map(
                lambda x: cls.get(x.featId),
                cls.raceFeatQuery.filter(RaceFeat.raceId == int(id)).all(),
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
            if feat.requirements is not None:
                foundFeat.requirements = feat.requirements
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
        newFeat.requirements = feat.requirements

        db.session.add(feat)
        db.session.commit()
        Logger.success("Creating a new feat with name: " + feat.name)
        return newFeat, []
