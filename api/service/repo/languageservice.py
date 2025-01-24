# Abilities and ability score calculations perchance


from api.model.language import Language
from extensions import db
from sqlalchemy.orm import Query


class LanguageService:
    @classmethod
    def init_default_languages(cls):
        defaults = [
            Language(
                name="Common",
                description="Common is the language spoken by the majority of the population in the world."
            ),
            Language(
                name="Dwarvish",
                description="Dwarvish is the language spoken by dwarves."
            ),
            Language(
                name="Elvish",
                description="Elvish is the language spoken by elves."
            ),
            Language(
                name="Giant",
                description="Giant is the language spoken by giants."
            ),
            Language(
                name="Gnomish",
                description="Gnomish is the language spoken by gnomes."
            ),
            Language(
                name="Goblin",
                description="Goblin is the language spoken by goblins."
            ),
            Language(
                name="Halfling",
                description="Halfling is the language spoken by halflings."
            ),
            Language(
                name="Orc",
                description="Orc is the language spoken by orcs."
            ),
            Language(
                name="Abyssal",
                description="Abyssal is the language spoken by demons."
            ),
            Language(
                name="Celestial",
                description="Celestial is the language spoken by angels."
            ),
            Language(
                name="Draconic",
                description="Draconic is the language spoken by dragons."
            ),
            Language(
                name="Deep Speech",
                description="Deep Speech is the language spoken by abberations."
            ),
            Language(
                name="Infernal",
                description="Infernal is the language spoken by devils."
            ),
            Language(
                name="Primordial",
                description="Primordial is the language spoken by elementals."
            ),
            Language(
                name="Sylvan",
                description="Sylvan is the language spoken by fey creatures."
            ),
            Language(
                name="Undercommon",
                description="Undercommon is the language spoken by underdark creatures."
            )
        ]
        
        existing_by_name = {
            row[0] for row in db.session.query(Language.name).all()
        }
        
        for ability in defaults:
            if ability.name not in existing_by_name:
                db.session.add(ability)

        db.session.commit()
    
    @classmethod
    def get(cls, langId):
        return db.session.query(Language).filter(Language.id == langId).first()
    
    @classmethod
    def getAll(cls):
        return db.session.query(Language).all()
    