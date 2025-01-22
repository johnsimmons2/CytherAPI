from datetime import datetime

from api.loghandler.logger import Logger
from sqlalchemy.orm import Query
from api.model.race import Race, RaceFeat, RaceLanguage
from api.model.feat import Feat
from api.model.classes import *
from api.model.ext_content import *
from api.service.ext_dbservice import Ext_ContentService


class RaceService:
    query = Query(Race, db.session)
    raceFeatQuery = Query(RaceFeat, db.session)
    featQuery = Query(Feat, db.session)

    @classmethod
    def delete(cls, id: int):
        foundClass = cls.query.filter(Race.id == id).first()

        if not foundClass:
            return False
        db.session.delete(foundClass)
        db.session.commit()
        return True

    @classmethod
    def getAll(cls) -> list[Race]:
        return cls.query.all()

    @classmethod
    def get(cls, id: str) -> Race:
        return cls.query.filter_by(id=id).first()

    @classmethod
    def getByName(cls, name: str) -> Race:
        return cls.query.filter(Race.name.ilike(f"%{name}%")).first()