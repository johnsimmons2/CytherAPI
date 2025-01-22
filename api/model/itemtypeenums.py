from enum import Enum
# 6_511_079 -> broken crystal unqiue magic base item

# X -> item type
class ItemBaseType(Enum):
    Consumable = "Consumable"
    Weapon = "Weapon"
    Armor = "Armor"
    Clothing = "Clothing"
    Shield = "Shields"
    Jewelry = "Jewelry"
    Tool = "Tools"
    Resource = "Resources"
    Misc = "Miscellaneous"
    KeyItem = "Key Items"
    
    def __init__(self, value, name):
        self.id = value
        self.display = name
    
# X0 -> rarity
class ItemRarity(Enum):
    Common = "Common"
    Uncommon = "Uncommon"
    Rare = "Rare"
    VeryRare = "Very Rare"
    Legendary = "Legendary"
    Artifact = "Artifact"
    Relic = "Relic"
    Unique = "Unique"
    Alchemical = "Alchemical"
    
    def __init__(self, value, name):
        self.id = value
        self.display = name

# X00 -> weight
class ItemWeight(Enum):
    NA = "N/A"
    Light = "Light"
    Medium = "Medium"
    Heavy = "Heavy"
    ExtremelyHeavy = "Extremely Heavy"
    
    def __init__(self, value, name):
        self.id = value
        self.display = name

# X_000 -> property
class ItemProperty(Enum):
    BaseItem = "Campaign Item"
    UniqueItem = "Player Item"
    
    def __init__(self, value, name):
        self.id = value
        self.display = name

# X0_000 -> stackable
class ItemStackable(Enum):
    Stackable = "Stackable"
    NotStackable = "Not Stackable"
    
    def __init__(self, value, name):
        self.id = value
        self.display = name

# X00_000 -> condition
class ItemCondition(Enum):
    NA = "N/A"
    Perfect = "Perfect"
    Good = "Good"
    Fair = "Fair"
    Poor = "Poor"
    Broken = "Broken"
    
    def __init__(self, value, name):
        self.id = value
        self.display = name

# X_000_000 -> material
class ItemMaterial(Enum):
    NA = "N/A"
    Wood = "Wood"
    Stone = "Stone"
    Metal = "Metal"
    Leather = "Leather"
    Cloth = "Cloth"
    Crystal = "Crystal"
    Organic = "Organic"
    Parchment = "Parchment"
    Magical = "Magical"
    
    def __init__(self, value, name):
        self.id = value
        self.display = name