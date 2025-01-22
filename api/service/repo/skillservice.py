from sqlalchemy.orm import Query
from extensions import db
from api.model.skill import Skill


class SkillService:
    query = db.Query(Skill, db.session)

    @classmethod
    def get(cls, id: int):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def getAll(cls):
        return cls.query.all()
