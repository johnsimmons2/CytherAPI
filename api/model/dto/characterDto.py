from typing import Optional
from api.model.dto.spellbookDto import SpellbookDTO
from api.model.dto.statsheetDto import StatsheetDTO
from dataclasses import dataclass


@dataclass
class CharacterDescriptionDTO:
  age: str
  height: str
  weight: str
  eyes: str
  skin: str
  hair: str
  background: str
  appearance: str
  bonds: str
  ideals: str
  personality: str
  flaws: str
  religion: str
  backstory: str

@dataclass
class CharacterDTO:
  name: str
  classId: int
  subclassId: Optional[int]
  raceId: int
  type: int
  speed: int
  languages: str
  stats: StatsheetDTO
  spellbook: SpellbookDTO
  savingThrows: list[str]
  skillIds: list[int]
  proficiencies: list[str]
  description: CharacterDescriptionDTO

  hitDiceShape: Optional[int] = None # Temporary fix until class structures are in place.
