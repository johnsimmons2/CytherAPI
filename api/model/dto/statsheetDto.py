from dataclasses import dataclass


@dataclass
class StatsheetDTO:
    id: int
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    hitdice: int
    hitpoints: int
    armorclass: int
