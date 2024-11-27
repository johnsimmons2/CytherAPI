from api.loghandler.logger import Logger
from api.model.classes import ClassTable
from api.model.dto.characterDto import CharacterDTO
from api.model.spellbook import *
from api.model.spells import *
from api.model import db
from sqlalchemy.orm import Query

from api.service.repo.spellservice import SpellService
from api.service.repo.classservice import ClassService


class SpellbookService:
    query = db.Query(Spellbook, db.session)

    @classmethod
    def prepareSpellsForSpellbook(cls, spells: list[Spells], spellbook: Spellbook):
        prepared = []
        for s in spells:
            spellbookPrepared = SpellbookPrepared(spell=s, spellbook=spellbook)
            prepared.append(spellbookPrepared)
            Logger.debug(f"Adding {'cantrip' if s.level == 0 else 'spell'} [{s.name}] to prepared spells.")
            db.session.add(spellbookPrepared)
            db.session.flush()
        return prepared

    @classmethod
    def createSpellbookKnowledgeForSpells(cls, spells: list[Spells], spellbook: Spellbook):
        spellbookKnowledge = []
        for s in spells:
            spellKnowledge = SpellbookKnowledge(spell=s, spellbook=spellbook)
            spellbookKnowledge.append(spellKnowledge)
            Logger.debug(f"Adding {'cantrip' if s.level == 0 else 'spell'} [{s.name}] to known spells.")
            db.session.add(spellKnowledge)
            db.session.flush()
        return spellbookKnowledge

    @classmethod
    def createSpellbookForCharacter(cls, characterDto: CharacterDTO):
        Logger.debug("============Creating spellbook for character.============")
        spellbook = Spellbook()
        spellbookDto = characterDto.spellbook

        spellTable: ClassTable | None = ClassService.getClassTable(characterDto.classId)
        if spellTable is None:
            # TODO: If a spell table is created after a character is created, the character will not have a spell table. This should be handled.
            Logger.error(f"Class [{ClassService.get(characterDto.classId).name}] does not have a spell table. Please create it manually, or else the character will have no spells.")

        if spellTable is not None:
            spellSlots = ClassService.getSpellSlotsForLevel(spellTable, characterDto.stats.level)

            spellbook.spellslot1 = spellSlots[0]
            spellbook.spellslot2 = spellSlots[1]
            spellbook.spellslot3 = spellSlots[2]
            spellbook.spellslot4 = spellSlots[3]
            spellbook.spellslot5 = spellSlots[4]
            spellbook.spellslot6 = spellSlots[5]
            spellbook.spellslot7 = spellSlots[6]
            spellbook.spellslot8 = spellSlots[7]
            spellbook.spellslot9 = spellSlots[8]
            # TODO Get if warlock and set those slots, or deprecate the columns

            # Spellbook Knowledge
            knowableSpells = list(map(lambda x: int(x), str(spellTable.spellsKnown).split(',')))[characterDto.stats.level - 1]
            Logger.debug(f"Character can know up to {knowableSpells} spells.")
            if len(spellbookDto.knownSpellIds) > knowableSpells:
                Logger.error(f"Character [{characterDto.name}] is trying to learn more spells than they are allowed to.")
                raise Exception("Character is trying to learn more spells than they are allowed to.")

            knownSpells = SpellService.getByIds(spellbookDto.knownSpellIds)
            spellbookKnowledge = cls.createSpellbookKnowledgeForSpells(knownSpells, spellbook)
            spellbook.knowledge = spellbookKnowledge

            # Spellbook Spells Prepared
            # TODO: Spells prepared handled by spellTable (ClassTable) and level. ClassTable may require
            # alternate calculation methods depending on class.
            preparedSpells = SpellService.getByIds(spellbookDto.preparedSpellIds)
            spellbookPreparedSpells = cls.prepareSpellsForSpellbook(preparedSpells, spellbook)
            spellbook.prepared = spellbookPreparedSpells

        db.session.add(spellbook)
        return spellbook

    @classmethod
    def getAll(cls):
        return cls.query.all()

    @classmethod
    def get(cls, id: str):
        return cls.query.filter_by(id=id).first()
