from api.loghandler.logger import Logger
from api.model.classes import ClassTable
from api.model.dto.characterDto import CharacterDTO
from api.model.spellbook import *
from api.model.spell import *
from sqlalchemy.orm import Query
from extensions import db

from api.service.repo.spellservice import SpellService
from api.service.repo.classservice import ClassService


class SpellbookService:
    query = db.Query(Spellbook, db.session)

    @classmethod
    def getAll(cls):
        return cls.query.all()

    @classmethod
    def get(cls, id: str):
        return cls.query.filter_by(id=id).first()
