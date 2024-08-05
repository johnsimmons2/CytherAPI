from api.model.spells import *
from api.loghandler.logger import Logger
from api.model import db
from sqlalchemy.orm import Query


class SpellService:
    spellQuery = Query(Spells, db.session)

    @classmethod
    def getAll(cls):
        return cls.spellQuery.all()

    @classmethod
    def get(cls, id: str):
        return cls.spellQuery.filter_by(id=id).first()

    @classmethod
    def getByIds(cls, ids: list[int]):
        return cls.spellQuery.filter(Spells.id.in_(ids)).all()

    @classmethod
    def createSpell(cls, spell: Spells, components: SpellComponents):
        if cls.spellQuery.filter_by(name=spell.name).first() is not None:
            return -1, ["A spell by this name already exists."]

        db.session.add(spell)
        db.session.flush()

        if components is None:
            components = SpellComponents(
                spellId=spell.id, itemId=None, quantity=0, goldValue=0
            )
        else:
            components.spellId = spell.id

        spell.components = components
        db.session.add(components)
        db.session.commit()
        return spell.id, []

    @classmethod
    def updateSpell(cls, spell: Spells, components: SpellComponents):
        foundSpell = cls.spellQuery.filter_by(id=spell.id).first()
        if foundSpell is not None:
            if spell.name is not None:
                foundSpell.name = spell.name
            if spell.castingTime is not None:
                foundSpell.castingTime = spell.castingTime
            if spell.description is not None:
                foundSpell.description = spell.description
            if spell.duration is not None:
                foundSpell.duration = spell.duration
            if spell.school is not None:
                foundSpell.school = spell.school
            if spell.range is not None:
                foundSpell.range = spell.range
            if spell.level is not None:
                foundSpell.level = spell.level
            if spell.verbal is not None:
                foundSpell.verbal = spell.verbal
            if spell.somatic is not None:
                foundSpell.somatic = spell.somatic
            if spell.material is not None:
                foundSpell.material = spell.material
            if spell.ritual is not None:
                foundSpell.ritual = spell.ritual
            if spell.concentration is not None:
                foundSpell.concentration = spell.concentration
            if components is not None:
                foundSpell.components = components
            db.session.commit()
            return foundSpell.id, []
        return -1, ["Could not find a spell with the given ID"]
