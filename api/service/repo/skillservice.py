from api.model import db
from sqlalchemy.orm import Query
from api.model.character import Skill


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
    def get(cls, id: int):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def getAll(cls):
        return cls.query.all()
