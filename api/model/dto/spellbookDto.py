from dataclasses import dataclass


@dataclass
class SpellbookDTO:
    spellSlots: list[int]
    knownSpellIds: list[int]
    preparedSpellIds: list[int]
    cantripIds: list[int]
