from enum import Enum


class Sizes(Enum):
    TINY = 'tiny'
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    HUGE = 'huge'
    GARGANTUAN = 'gargantuan'

class CreatureTypes(Enum):
    ABERRATION = 'aberration'
    BEAST = 'beast'
    CELESTIAL = 'celestial'
    CONSTRUCT = 'construct'
    DRAGON = 'dragon'
    ELEMENTAL = 'elemental'
    FEY = 'fey'
    FIEND = 'fiend'
    GIANT = 'giant'
    HUMANOID = 'humanoid'
    MONSTROSITY = 'monstrosity'
    OOZE = 'ooze'
    PLANT = 'plant'
    UNDEAD = 'undead'

class EquipSlots(Enum):
    HEAD = 'head'
    SHOULDERS = 'shoulders'
    HANDS = 'hands'
    LEGS = 'legs'
    ARMS = 'arms'
    FEET = 'feet'
    MAIN_HAND = 'main hand'
    OFF_HAND = 'offhand'
    BACK = 'back'
    RING = 'ring'
    NECK = 'neck'
    CHEST = 'chest'
    BELT = 'belt'
    WRIST = 'wrist'
    WAIST = 'waist'
    EYES = 'eyes'
    EARS = 'ears'
    MOUTH = 'mouth'
    TAIL = 'tail'
    WINGS = 'wings'

class TagIcons(Enum):
    FLAG = 'flagOutline'
    BOOK = 'bookOutline'
    DIAMOND = 'diamondOutline'
    KEY = 'keyOutline'
    PAW = 'pawOutline'
    THUMBSDOWN = 'thumbsDownOutline'
    GIFT = 'giftOutline'
    EAR = 'earOutline'
    HEART = 'heartOutline'
    COLORFILTER = 'colorFilterOutline'
    DICE = 'diceOutline'
    FISH = 'fishOutline'
    EARTH = 'earthOutline'
    FLASK = 'flaskOutline'
    RIBBON = 'ribbonOutline'
    SKULL = 'skullOutline'
    CHECKMARK = 'checkmarkDoneOutline'
    COG = 'cogOutline'
    SEARCH = 'searchOutline'
    STAR = 'starOutline'
    FOLDER = 'folderOutline'
    PERSON = 'personOutline'
    READER = 'readerOutline'