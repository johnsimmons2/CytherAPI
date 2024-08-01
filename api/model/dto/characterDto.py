from api.model.dto.spellbookDto import SpellbookDTO
from api.model.dto.statsheetDto import StatsheetDTO
from dataclasses import dataclass


@dataclass
class CharacterDTO:
    name: str
    classId: int
    raceId: int
    type: int
    speed: int
    languages: str
    stats: StatsheetDTO
    spellbook: SpellbookDTO
    savingThrows: list[str]
    skillIds: list[int]
