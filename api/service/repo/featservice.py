from sqlalchemy.orm import Query
from api.loghandler.logger import Logger
from api.model.race import RaceFeat
from extensions import db
from api.model.feat import Feat


class FeatService:
    query = Query(Feat, db.session)
    raceFeatQuery = Query(RaceFeat, db.session)

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
