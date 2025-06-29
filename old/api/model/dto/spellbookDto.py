from dataclasses import dataclass
from typing import Optional


@dataclass
class SpellbookDTO:
    cantripIds: list[int]
    knownSpellIds: Optional[list[int]]
    preparedSpellIds: list[int]
