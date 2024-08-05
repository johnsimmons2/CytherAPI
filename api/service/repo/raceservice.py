import datetime

from api.loghandler.logger import Logger
from sqlalchemy.orm import Query
from api.model.classes import *
from api.model.ext_content import *
from api.service.ext_dbservice import Ext_ContentService


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
    def getAll(cls) -> list[Race]:
        cls.getRacesOnline()
        return cls.query.all()

    @classmethod
    def get(cls, id: str) -> Race:
        return cls.query.filter_by(id=id).first()

    @classmethod
    def getByName(cls, name: str) -> Race:
        return cls.query.filter(Race.name.ilike(f"%{name}%")).first()

    @classmethod
    def update(cls, race: Race, feats: List[Feat] | None) -> tuple[int, list[str]]:
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
    def createRace(cls, race: Race) -> tuple[int, list[str]]:
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
    def getRaceFeats(cls, raceName: str) -> list[Feat]:
        race = cls.getByName(raceName)
        if race is not None:
            raceFeats = cls.raceFeatQuery.filter_by(raceId=race.id).all()
            feats = map(lambda x: cls.featQuery.filter_by(id=x.featId).first(), raceFeats)
            return list(feats)
        return []
