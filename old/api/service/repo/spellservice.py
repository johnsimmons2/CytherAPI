from api.model.spell import Spell
from api.loghandler.logger import Logger
from sqlalchemy.orm import Query
from extensions import db


class SpellService:
    spellQuery = Query(Spell, db.session)

    @classmethod
    def getAll(cls):
        return cls.spellQuery.all()

    @classmethod
    def get(cls, id: str):
        return cls.spellQuery.filter_by(id=id).first()

    @classmethod
    def getByIds(cls, ids: list[int]):
        return cls.spellQuery.filter(Spell.id.in_(ids)).all()
