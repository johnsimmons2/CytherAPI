from api.model.character import Proficiency, SavingThrow, Statsheet
from sqlalchemy.orm import Query
from extensions import db

class StatsheetService:
    query = db.Query(Statsheet, db.session)
    profQuery = db.Query(Proficiency, db.session)
    stQuery = db.Query(SavingThrow, db.session)

    @classmethod
    def initSavingThrows(cls):
        cls.stQuery.filter_by(statName='Strength').first() or db.session.add(SavingThrow(statName='Strength'))
        cls.stQuery.filter_by(statName='Dexterity').first() or db.session.add(SavingThrow(statName='Dexterity'))
        cls.stQuery.filter_by(statName='Constitution').first() or db.session.add(SavingThrow(statName='Constitution'))
        cls.stQuery.filter_by(statName='Intelligence').first() or db.session.add(SavingThrow(statName='Intelligence'))
        cls.stQuery.filter_by(statName='Wisdom').first() or db.session.add(SavingThrow(statName='Wisdom'))
        cls.stQuery.filter_by(statName='Charisma').first() or db.session.add(SavingThrow(statName='Charisma'))
        db.session.commit()

    @classmethod
    def getProficiencyByName(cls, name: str):
        return cls.profQuery.filter_by(name=name).first()

    @classmethod
    def getSavingThrowByName(cls, name: str):
        return cls.stQuery.filter_by(statName=name).first()

    @classmethod
    def getSavingThrows(cls):
        return cls.stQuery.all()
