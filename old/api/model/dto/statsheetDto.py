from dataclasses import dataclass


@dataclass
class StatsheetDTO:
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

    health: int
    level: int
    #armorclass: int
