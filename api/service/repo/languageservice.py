# Abilities and ability score calculations perchance


from api.model.character import Character, CharacterLanguage
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
    def get(cls, langId: str):
        return db.session.query(Language).filter(Language.id == langId).first()
    
    @classmethod
    def getAll(cls):
        return db.session.query(Language).all()
    
    @classmethod
    def getLanguageByName(cls, name: str):
        return db.session.query(Language).filter_by(name=name).first()
    
    @classmethod
    def createLanguage(cls, language: Language):
        if cls.getLanguageByName(language.name) is not None:
            return None
        
        newLanguage = Language()
        newLanguage.name = language.name
        newLanguage.description = language.description
        
        db.session.add(newLanguage)
        db.session.commit()
        
        return newLanguage
    
    @classmethod
    def deleteLanguage(cls, langId: str):
        lang = cls.get(langId)
        if lang is not None:
            db.session.delete(lang)
            db.session.commit()
            return lang
        return None
    
    @classmethod
    def addLanguageToCharacter(cls, langId: str, charId: str):
        lang = cls.get(langId)
        if lang is not None:
            char = db.session.query(Character).filter(Character.id == charId).first()
            if char is not None:
                charLang = CharacterLanguage()
                charLang.characterId = charId
                charLang.languageId = langId
                db.session.add(charLang)
                db.session.commit()
                return lang
        return None
    
    @classmethod
    def removeLanguageFromCharacter(cls, langId: str, charId: str):
        lang = cls.get(langId)
        if lang is not None:
            char = db.session.query(Character).filter(Character.id == charId).first()
            if char is not None:
                charLang = db.session.query(CharacterLanguage).filter(CharacterLanguage.characterId == charId, CharacterLanguage.languageId == langId).first()
                if charLang is not None:
                    db.session.delete(charLang)
                    db.session.commit()
                    return lang
        return None