from dataclasses import dataclass, field
from typing import List, Optional
from api.loghandler.logger import Logger
from api.model import db
from sqlalchemy.orm import Query
from api.model.classes import Class, Feat, Race, Subclass
from api.service.dbservice import RaceService, FeatService, ClassService
import requests


@dataclass
class Dnd5eFeatDTO:
    name: str = ""
    descriptions: [str] = field(default_factory=list)

@dataclass
class Dnd5eRaceDTO:
    name: str = ""
    size: str = ""
    languages: str = ""
    alignment: str = ""
    speed: str = ""
    traits: [Dnd5eFeatDTO] = field(default_factory=list)

@dataclass
class Dnd5eSubclassDTO:
    name: str = ""
    description: str = ""
    feats: Optional[List[Dnd5eFeatDTO]] = field(default_factory=list)

@dataclass
class Dnd5eClassDTO:
    name: str = ""
    description: str = ""
    hitdice: int = 0
    proficiencies: [str] = field(default_factory=list)
    subclasses: [Dnd5eSubclassDTO] = field(default_factory=list)
    feats: [Dnd5eFeatDTO] = field(default_factory=list)


class Dnd5eAPIService:
    URL = "https://www.dnd5eapi.co"

    featQuery = Query(Feat, db.session)

    # Entry point to find all Classes from DnD 5e. Double check each request to minimize API use.
    @classmethod
    def getClasses(cls):
        response = requests.get(cls.URL + "/api/classes")
        Logger.debug(f"Calling: {cls.URL + '/api/classes'}")
        responseJson = response.json()["results"]

        classMap = list(map(lambda x: (x["index"], x["name"]), responseJson))

        for clazz in classMap:
            existingClass = ClassService.getByName(clazz[1])
            if existingClass is None:
                newClass = Class()
                classDto = cls.getClass(clazz[0])
                newClass.name = classDto.name
                newClass.description = classDto.description
                newClass.subclasses = list(map(lambda x: ClassService.getSubclassByName(x.name), classDto.subclasses))
                newClass.feats = list(map(lambda x: cls.traitAsFeat(x), classDto.feats))
                db.session.add(newClass)
                db.session.commit()

    @classmethod
    def getClass(cls, classIndex: str):
        response = requests.get(cls.URL + "/api/classes/" + classIndex)
        Logger.debug(f"Calling: {cls.URL + '/api/classes/' + classIndex}")
        responseJson = response.json()

        classDto = Dnd5eClassDTO()
        classDto.name = responseJson["name"]
        classDto.hitdice = responseJson["hit_die"]
        classDto.proficiencies = list(map(lambda x: x["name"], responseJson["proficiencies"]))

        for subclass in responseJson["subclasses"]:
            existingSubclass = ClassService.getSubclassByName(subclass["name"])
            if existingSubclass is None:
                subclassDto = cls.getSubclass(subclass["index"])
                newSubclass = Subclass()
                newSubclass.name = subclassDto.name
                newSubclass.description = subclassDto.description
                newSubclass.feats = list(map(lambda x: cls.traitAsFeat(x), subclassDto.feats))
                classDto.subclasses.append(subclassDto)
                db.session.add(newSubclass)
                db.session.commit()
            else:
                subclassDto = Dnd5eSubclassDTO()
                subclassDto.name = existingSubclass.name
                subclassDto.description = existingSubclass.description
                subclassDto.feats = list(map(lambda x: cls.featAsTrait(x), existingSubclass.feats))
                classDto.subclasses.append(subclassDto)
        return classDto

    @classmethod
    def getSubclass(cls, subclassIndex: str) -> Dnd5eSubclassDTO:
        response = requests.get(cls.URL + "/api/subclasses/" + subclassIndex)
        Logger.debug(f"Calling: {cls.URL + '/api/subclasses/' + subclassIndex}")
        responseJson = response.json()

        subclassDto = Dnd5eSubclassDTO()
        subclassDto.name = responseJson["name"]
        subclassDto.description = ", ".join(responseJson["desc"])

        # Get the feats for the subclass and insert them into the database
        feats = cls.createFeatsForSubclass(responseJson["subclass_levels"])

        subclassDto.feats = feats

        return subclassDto
        
    @classmethod
    def createFeatsForSubclass(cls, nextRequest: str) -> [Dnd5eFeatDTO]:
        if nextRequest is None:
            return
        response = requests.get(cls.URL + nextRequest)
        Logger.debug(f"Calling: {cls.URL + nextRequest}")
        responseJson = response.json()

        feats = []

        for level in responseJson:
            for feature in level["features"]:
                trait = cls.getTraitByName(feature["name"])
                if not trait:
                    trait = cls.getFeatureByIndex(feature["index"])
                    cls.traitAsFeat(trait)
                    feats.append(trait)
                else:
                    feats.append(trait)
        return feats

    @classmethod
    def getFeatureByIndex(cls, featureIndex: str):
        response = requests.get(cls.URL + "/api/features/" + featureIndex)
        Logger.debug(f"Calling: {cls.URL + '/api/features/' + featureIndex}")
        responseJson = response.json()

        newFeat = Dnd5eFeatDTO()
        newFeat.name = responseJson["name"]
        newFeat.descriptions = responseJson["desc"]

        return newFeat

    @classmethod
    def getTraitByName(cls, traitName: str) -> Dnd5eFeatDTO | None:
        newTrait = Dnd5eFeatDTO()
        if cls.featQuery.filter(Feat.name == traitName).count() > 0:
            feat = cls.featQuery.filter(Feat.name == traitName).first()
            newTrait.name = feat.name
            newTrait.descriptions = [feat.description]
            return newTrait
        return None

    @classmethod
    def getTraitByIndex(cls, traitIndex: str) -> Dnd5eFeatDTO:
        newTrait = Dnd5eFeatDTO()
        traitResponse = requests.get(cls.URL + "/api/traits/" + traitIndex)
        Logger.debug(f"Calling: {cls.URL + '/api/traits/' + traitIndex}")
        traitResponseJson = traitResponse.json()

        newTrait.name = traitResponseJson["name"]
        newTrait.descriptions = traitResponseJson["desc"]
        return newTrait

    @classmethod
    def traitAsFeat(cls, trait: Dnd5eFeatDTO) -> Feat:
        feat = FeatService.getByName(trait.name)
        if feat:
            return feat
        newFeat = Feat()
        newFeat.name = trait.name
        newFeat.description = ', '.join(trait.descriptions)
        db.session.add(newFeat)
        db.session.commit()
        return newFeat
    
    @classmethod
    def featAsTrait(cls, feat: Feat) -> Dnd5eFeatDTO:
        trait = Dnd5eFeatDTO()
        trait.name = feat.name
        trait.descriptions = [feat.description]
        return trait

    # Entry point for races. Double check each request to minimize API use.
    @classmethod
    def getRaces(cls):
        response = requests.get(cls.URL + "/api/races")
        Logger.debug(f"Calling: {cls.URL + '/api/races'}")
        responseJson = response.json()["results"]

        raceMap = list(map(lambda x: (x["index"], x["name"]), responseJson))

        for race in raceMap:
            if RaceService.getByName(race[1]) is None:
                newRace = Race()
                raceDto = cls.getRace(race[0])

                newRace.alignment = raceDto.alignment
                newRace.description = raceDto.alignment
                newRace.languages = raceDto.languages
                newRace.name = raceDto.name
                newRace.size = raceDto.size
                newRace.feats = list(map(lambda x: cls.traitAsFeat(x), raceDto.traits))
                db.session.add(newRace)
                Logger.success(f"Added {newRace.name} to the races table.")
        db.session.commit()

    @classmethod
    def getRaceDtoFromRace(cls, raceName: str) -> Dnd5eRaceDTO:
        race = RaceService.getByName(raceName)
        if race is None:
            return None
        
        raceDto = Dnd5eRaceDTO()
        raceDto.alignment = race.alignment
        raceDto.languages = race.languages
        raceDto.name = race.name
        raceDto.size = race.size
        raceDto.speed = "30ft"
        raceDto.traits = list(map(lambda x: cls.getTraitByName(x.name), race.feats))

    @classmethod
    def getRace(cls, raceIndex: str) -> Dnd5eRaceDTO:
        response = requests.get(cls.URL + "/api/races/" + raceIndex)
        Logger.debug(f"Calling: {cls.URL + '/api/races/' + raceIndex}")
        responseJson = response.json()

        raceDto = Dnd5eRaceDTO()
        raceDto.name = responseJson["name"]
        raceDto.speed = responseJson["speed"]
        raceDto.size = responseJson["size"]
        raceDto.alignment = responseJson["alignment"]
        raceDto.languages = responseJson["language_desc"]

        for feat in responseJson["traits"]:
            trait = cls.getTraitByName(feat["name"])
            if trait:
                raceDto.traits.append(trait)
            else:
                raceDto.traits.append(cls.getTraitByIndex(feat["index"]))
        
        for bonus in responseJson["ability_bonuses"]:
            traitName = "Ability Score Increase: +" + str(bonus["bonus"]) + " " + bonus["ability_score"]["name"]
            trait = cls.getTraitByName(traitName)
            if trait:
                raceDto.traits.append(trait)
            else:
                abilityFeat = Dnd5eFeatDTO()
                abilityFeat.name = traitName
                abilityFeat.descriptions = ["+" + str(bonus["bonus"]) + " to " + bonus["ability_score"]["name"]]
                raceDto.traits.append(abilityFeat)
        return raceDto



