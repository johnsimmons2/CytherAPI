# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Ability(models.Model):
    name = models.CharField()
    min = models.IntegerField()
    max = models.IntegerField()
    description = models.CharField()
    abbreviation = models.CharField()

    class Meta:
        managed = False
        db_table = 'ability'


class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'alembic_version'


class Campaign(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaign'


class CampaignCharacters(models.Model):
    campaignid = models.ForeignKey(Campaign, models.DO_NOTHING, db_column='campaignId', blank=True, null=True)  # Field name made lowercase.
    characterid = models.ForeignKey('Character', models.DO_NOTHING, db_column='characterId', blank=True, null=True)  # Field name made lowercase.
    active = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaign_characters'


class CampaignUsers(models.Model):
    campaignid = models.ForeignKey(Campaign, models.DO_NOTHING, db_column='campaignId', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    active = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaign_users'


class Character(models.Model):
    statsheetid = models.OneToOneField('Statsheet', models.DO_NOTHING, db_column='statsheetid', blank=True, null=True)
    raceid = models.ForeignKey('Race', models.DO_NOTHING, db_column='raceId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    isnpc = models.BooleanField(db_column='isNpc')  # Field name made lowercase.
    age = models.IntegerField(blank=True, null=True)
    height = models.CharField(blank=True, null=True)
    weight = models.CharField(blank=True, null=True)
    eye_color = models.CharField(blank=True, null=True)
    skin_color = models.CharField(blank=True, null=True)
    hair_color = models.CharField(blank=True, null=True)
    alignment = models.CharField(blank=True, null=True)
    religion = models.CharField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    appearance = models.TextField(blank=True, null=True)
    bonds = models.TextField(blank=True, null=True)
    ideals = models.TextField(blank=True, null=True)
    personality = models.TextField(blank=True, null=True)
    flaws = models.TextField(blank=True, null=True)
    backstory = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'character'


class CharacterClass(models.Model):
    characterid = models.ForeignKey(Character, models.DO_NOTHING, db_column='characterId')  # Field name made lowercase.
    classid = models.ForeignKey('Class', models.DO_NOTHING, db_column='classId')  # Field name made lowercase.
    subclassid = models.ForeignKey('Class', models.DO_NOTHING, db_column='subclassId', related_name='characterclass_subclassid_set')  # Field name made lowercase.
    usedhitdice = models.IntegerField(db_column='usedHitDice', blank=True, null=True)  # Field name made lowercase.
    level = models.IntegerField(blank=True, null=True)
    xp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'character_class'


class CharacterCondition(models.Model):
    characterid = models.ForeignKey(Character, models.DO_NOTHING, db_column='characterId')  # Field name made lowercase.
    conditionid = models.ForeignKey('Condition', models.DO_NOTHING, db_column='conditionId')  # Field name made lowercase.
    source = models.CharField(blank=True, null=True)
    duration = models.CharField(blank=True, null=True)
    stacks = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'character_condition'


class CharacterFeat(models.Model):
    characterid = models.ForeignKey(Character, models.DO_NOTHING, db_column='characterId', blank=True, null=True)  # Field name made lowercase.
    featid = models.ForeignKey('Feat', models.DO_NOTHING, db_column='featId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'character_feat'


class CharacterLanguage(models.Model):
    characterid = models.ForeignKey(Character, models.DO_NOTHING, db_column='characterId')  # Field name made lowercase.
    languageid = models.ForeignKey('Language', models.DO_NOTHING, db_column='languageId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'character_language'


class CharacterRelationship(models.Model):
    characterid = models.ForeignKey(Character, models.DO_NOTHING, db_column='characterId')  # Field name made lowercase.
    othercharacterid = models.ForeignKey(Character, models.DO_NOTHING, db_column='otherCharacterId', related_name='characterrelationship_othercharacterid_set')  # Field name made lowercase.
    allies = models.BooleanField()
    enemies = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'character_relationship'


class Class(models.Model):
    name = models.CharField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    primaryabilityid = models.ForeignKey(Ability, models.DO_NOTHING, db_column='primaryAbilityId')  # Field name made lowercase.
    hitdice = models.CharField(db_column='hitDice', blank=True, null=True)  # Field name made lowercase.
    isprimary = models.BooleanField(db_column='isPrimary', blank=True, null=True)  # Field name made lowercase.
    primaryclassid = models.ForeignKey('self', models.DO_NOTHING, db_column='primaryClassId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'class'


class ClassFeat(models.Model):
    classid = models.ForeignKey(Class, models.DO_NOTHING, db_column='classId')  # Field name made lowercase.
    featid = models.ForeignKey('Feat', models.DO_NOTHING, db_column='featId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'class_feat'


class ClassResource(models.Model):
    name = models.CharField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'class_resource'


class ClassTable(models.Model):
    classid = models.ForeignKey(Class, models.DO_NOTHING, db_column='classId')  # Field name made lowercase.
    resourceid = models.ForeignKey(ClassResource, models.DO_NOTHING, db_column='resourceId', blank=True, null=True)  # Field name made lowercase.
    equiptypeid = models.ForeignKey('EquipmentType', models.DO_NOTHING, db_column='equipTypeId', blank=True, null=True)  # Field name made lowercase.
    featid = models.ForeignKey('Feat', models.DO_NOTHING, db_column='featId', blank=True, null=True)  # Field name made lowercase.
    resourcequantity = models.IntegerField(db_column='resourceQuantity', blank=True, null=True)  # Field name made lowercase.
    level = models.IntegerField(blank=True, null=True)
    spellslotquantity = models.IntegerField(db_column='spellSlotQuantity', blank=True, null=True)  # Field name made lowercase.
    spellslotlevel = models.IntegerField(db_column='spellSlotLevel', blank=True, null=True)  # Field name made lowercase.
    requirements = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'class_table'


class Condition(models.Model):
    name = models.CharField()
    description = models.CharField()
    source = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'condition'


class ConditionEffect(models.Model):
    conditionid = models.ForeignKey(Condition, models.DO_NOTHING, db_column='conditionId')  # Field name made lowercase.
    vulnerableid = models.ForeignKey('DamageType', models.DO_NOTHING, db_column='vulnerableId', blank=True, null=True)  # Field name made lowercase.
    resistantid = models.ForeignKey('DamageType', models.DO_NOTHING, db_column='resistantId', related_name='conditioneffect_resistantid_set', blank=True, null=True)  # Field name made lowercase.
    immuneid = models.ForeignKey('DamageType', models.DO_NOTHING, db_column='immuneId', related_name='conditioneffect_immuneid_set', blank=True, null=True)  # Field name made lowercase.
    abilityid = models.ForeignKey(Ability, models.DO_NOTHING, db_column='abilityId', blank=True, null=True)  # Field name made lowercase.
    abilityadj = models.IntegerField(db_column='abilityAdj', blank=True, null=True)  # Field name made lowercase.
    skillid = models.ForeignKey('Skill', models.DO_NOTHING, db_column='skillId', blank=True, null=True)  # Field name made lowercase.
    skilladj = models.IntegerField(db_column='skillAdj', blank=True, null=True)  # Field name made lowercase.
    rolladvantage = models.BooleanField(db_column='rollAdvantage', blank=True, null=True)  # Field name made lowercase.
    rolldisadvantage = models.BooleanField(db_column='rollDisadvantage', blank=True, null=True)  # Field name made lowercase.
    rolltype = models.CharField(db_column='rollType', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'condition_effect'


class DamageType(models.Model):
    name = models.CharField()
    description = models.CharField(blank=True, null=True)
    icon = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'damage_type'


class EquipmentType(models.Model):
    name = models.CharField()
    description = models.CharField(blank=True, null=True)
    icon = models.CharField(blank=True, null=True)
    isweapon = models.BooleanField(db_column='isWeapon')  # Field name made lowercase.
    isarmor = models.BooleanField(db_column='isArmor')  # Field name made lowercase.
    isshield = models.BooleanField(db_column='isShield')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'equipment_type'


class ExtContent(models.Model):
    key = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    userid = models.IntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.
    characterid = models.IntegerField(db_column='characterId', blank=True, null=True)  # Field name made lowercase.
    value = models.IntegerField(blank=True, null=True)
    previousvalue = models.IntegerField(db_column='previousValue', blank=True, null=True)  # Field name made lowercase.
    active = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ext_content'


class Feat(models.Model):
    name = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feat'


class FeatEffect(models.Model):
    featid = models.ForeignKey(Feat, models.DO_NOTHING, db_column='featId')  # Field name made lowercase.
    conditionid = models.ForeignKey(Condition, models.DO_NOTHING, db_column='conditionId', blank=True, null=True)  # Field name made lowercase.
    vulnerableid = models.ForeignKey(DamageType, models.DO_NOTHING, db_column='vulnerableId', blank=True, null=True)  # Field name made lowercase.
    resistantid = models.ForeignKey(DamageType, models.DO_NOTHING, db_column='resistantId', related_name='feateffect_resistantid_set', blank=True, null=True)  # Field name made lowercase.
    immuneid = models.ForeignKey(DamageType, models.DO_NOTHING, db_column='immuneId', related_name='feateffect_immuneid_set', blank=True, null=True)  # Field name made lowercase.
    abilityid = models.ForeignKey(Ability, models.DO_NOTHING, db_column='abilityId', blank=True, null=True)  # Field name made lowercase.
    abilityadj = models.IntegerField(db_column='abilityAdj', blank=True, null=True)  # Field name made lowercase.
    skillid = models.ForeignKey('Skill', models.DO_NOTHING, db_column='skillId', blank=True, null=True)  # Field name made lowercase.
    skilladj = models.IntegerField(db_column='skillAdj', blank=True, null=True)  # Field name made lowercase.
    rolladvantage = models.BooleanField(db_column='rollAdvantage', blank=True, null=True)  # Field name made lowercase.
    rolldisadvantage = models.BooleanField(db_column='rollDisadvantage', blank=True, null=True)  # Field name made lowercase.
    rolltype = models.CharField(db_column='rollType', blank=True, null=True)  # Field name made lowercase.
    requirements = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feat_effect'


class Inventory(models.Model):
    characterid = models.ForeignKey(Character, models.DO_NOTHING, db_column='characterId')  # Field name made lowercase.
    itemid = models.ForeignKey('Item', models.DO_NOTHING, db_column='itemId')  # Field name made lowercase.
    quantity = models.IntegerField(blank=True, null=True)
    equipped = models.BooleanField(blank=True, null=True)
    equipslot = models.TextField(db_column='equipSlot', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    attuned = models.BooleanField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventory'


class InventoryShared(models.Model):
    inventoryid = models.ForeignKey(Inventory, models.DO_NOTHING, db_column='inventoryId')  # Field name made lowercase.
    shareduserid = models.ForeignKey('User', models.DO_NOTHING, db_column='sharedUserId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'inventory_shared'


class Item(models.Model):
    name = models.CharField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type = models.TextField()  # This field type is a guess.
    isconsumable = models.BooleanField(db_column='isConsumable')  # Field name made lowercase.
    rarity = models.TextField()  # This field type is a guess.
    weight = models.TextField()  # This field type is a guess.
    property = models.TextField()  # This field type is a guess.
    stackable = models.TextField()  # This field type is a guess.
    condition = models.TextField()  # This field type is a guess.
    material = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'item'


class Language(models.Model):
    name = models.CharField()
    description = models.CharField()

    class Meta:
        managed = False
        db_table = 'language'


class Note(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    characterid = models.ForeignKey(Character, models.DO_NOTHING, db_column='characterId', blank=True, null=True)  # Field name made lowercase.
    campaignid = models.ForeignKey(Campaign, models.DO_NOTHING, db_column='campaignId', blank=True, null=True)  # Field name made lowercase.
    directory = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'note'


class NoteSharedDirectories(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    directory = models.CharField(max_length=255, blank=True, null=True)
    sharedwithid = models.ForeignKey('User', models.DO_NOTHING, db_column='sharedWithId', related_name='noteshareddirectories_sharedwithid_set', blank=True, null=True)  # Field name made lowercase.
    sharedate = models.DateTimeField(db_column='shareDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'note_shared_directories'


class NoteSharedUsers(models.Model):
    noteid = models.ForeignKey(Note, models.DO_NOTHING, db_column='noteId', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    sharedate = models.DateTimeField(db_column='shareDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'note_shared_users'


class NoteTags(models.Model):
    noteid = models.ForeignKey(Note, models.DO_NOTHING, db_column='noteId', blank=True, null=True)  # Field name made lowercase.
    tagid = models.ForeignKey('Tag', models.DO_NOTHING, db_column='tagId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'note_tags'


class Race(models.Model):
    name = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    size = models.CharField()
    type = models.TextField(blank=True, null=True)  # This field type is a guess.
    walkspeed = models.IntegerField(db_column='walkSpeed')  # Field name made lowercase.
    swimspeed = models.IntegerField(db_column='swimSpeed', blank=True, null=True)  # Field name made lowercase.
    flyspeed = models.IntegerField(db_column='flySpeed', blank=True, null=True)  # Field name made lowercase.
    climbspeed = models.IntegerField(db_column='climbSpeed', blank=True, null=True)  # Field name made lowercase.
    burrowspeed = models.IntegerField(db_column='burrowSpeed', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'race'


class RaceFeat(models.Model):
    raceid = models.ForeignKey(Race, models.DO_NOTHING, db_column='raceId')  # Field name made lowercase.
    featid = models.ForeignKey(Feat, models.DO_NOTHING, db_column='featId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'race_feat'


class RaceLanguage(models.Model):
    raceid = models.ForeignKey(Race, models.DO_NOTHING, db_column='raceId')  # Field name made lowercase.
    languageid = models.ForeignKey(Language, models.DO_NOTHING, db_column='languageId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'race_language'


class Role(models.Model):
    level = models.IntegerField(blank=True, null=True)
    rolename = models.CharField(db_column='roleName', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'role'


class Skill(models.Model):
    name = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    abilityid = models.ForeignKey(Ability, models.DO_NOTHING, db_column='abilityId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'skill'


class Spell(models.Model):
    abilityid = models.ForeignKey(Ability, models.DO_NOTHING, db_column='abilityId', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(blank=True, null=True)
    castingtime = models.CharField(db_column='castingTime', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(blank=True, null=True)
    duration = models.CharField(blank=True, null=True)
    school = models.CharField(blank=True, null=True)
    range = models.CharField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    melee = models.BooleanField()
    verbal = models.BooleanField()
    somatic = models.BooleanField()
    material = models.BooleanField()
    ritual = models.BooleanField()
    concentration = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'spell'


class Spellbook(models.Model):
    spellslot1 = models.IntegerField(blank=True, null=True)
    spellslot2 = models.IntegerField(blank=True, null=True)
    spellslot3 = models.IntegerField(blank=True, null=True)
    spellslot4 = models.IntegerField(blank=True, null=True)
    spellslot5 = models.IntegerField(blank=True, null=True)
    spellslot6 = models.IntegerField(blank=True, null=True)
    spellslot7 = models.IntegerField(blank=True, null=True)
    spellslot8 = models.IntegerField(blank=True, null=True)
    spellslot9 = models.IntegerField(blank=True, null=True)
    statsheetid = models.ForeignKey('Statsheet', models.DO_NOTHING, db_column='statsheetId')  # Field name made lowercase.
    spellcastingabilityid = models.ForeignKey(Ability, models.DO_NOTHING, db_column='spellCastingAbilityId')  # Field name made lowercase.
    cantrips = models.IntegerField(blank=True, null=True)
    spellsknown = models.IntegerField(db_column='spellsKnown', blank=True, null=True)  # Field name made lowercase.
    spellsprepared = models.IntegerField(db_column='spellsPrepared', blank=True, null=True)  # Field name made lowercase.
    actions = models.IntegerField(blank=True, null=True)
    bonusactions = models.IntegerField(db_column='bonusActions', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'spellbook'


class SpellbookSpell(models.Model):
    spellbookid = models.ForeignKey(Spellbook, models.DO_NOTHING, db_column='spellbookId')  # Field name made lowercase.
    spellid = models.ForeignKey(Spell, models.DO_NOTHING, db_column='spellId')  # Field name made lowercase.
    spelllevel = models.IntegerField(db_column='spellLevel', blank=True, null=True)  # Field name made lowercase.
    iscantrip = models.BooleanField(db_column='isCantrip', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'spellbook_spell'


class Statsheet(models.Model):
    health = models.IntegerField(blank=True, null=True)
    maxhealth = models.IntegerField(db_column='maxHealth', blank=True, null=True)  # Field name made lowercase.
    temphealth = models.IntegerField(db_column='tempHealth', blank=True, null=True)  # Field name made lowercase.
    armorclass = models.IntegerField(db_column='armorClass', blank=True, null=True)  # Field name made lowercase.
    initative = models.IntegerField(blank=True, null=True)
    exhaustion = models.IntegerField(blank=True, null=True)
    observation = models.IntegerField(blank=True, null=True)
    walkspeed = models.IntegerField(db_column='walkSpeed', blank=True, null=True)  # Field name made lowercase.
    swimspeed = models.IntegerField(db_column='swimSpeed', blank=True, null=True)  # Field name made lowercase.
    flyspeed = models.IntegerField(db_column='flySpeed', blank=True, null=True)  # Field name made lowercase.
    burrowspeed = models.IntegerField(db_column='burrowSpeed', blank=True, null=True)  # Field name made lowercase.
    climbspeed = models.IntegerField(db_column='climbSpeed', blank=True, null=True)  # Field name made lowercase.
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statsheet'


class StatsheetAbility(models.Model):
    statshetid = models.ForeignKey(Statsheet, models.DO_NOTHING, db_column='statshetId')  # Field name made lowercase.
    abilityid = models.ForeignKey(Ability, models.DO_NOTHING, db_column='abilityId')  # Field name made lowercase.
    adjustment = models.IntegerField(blank=True, null=True)
    value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'statsheet_ability'


class StatsheetDamageType(models.Model):
    statshetid = models.ForeignKey(Statsheet, models.DO_NOTHING, db_column='statshetId')  # Field name made lowercase.
    damagetypeid = models.ForeignKey(DamageType, models.DO_NOTHING, db_column='damageTypeId')  # Field name made lowercase.
    vulnerable = models.BooleanField(blank=True, null=True)
    resistant = models.BooleanField(blank=True, null=True)
    immune = models.BooleanField(blank=True, null=True)
    source = models.CharField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statsheet_damage_type'


class StatsheetProficiency(models.Model):
    statshetid = models.ForeignKey(Statsheet, models.DO_NOTHING, db_column='statshetId')  # Field name made lowercase.
    skillid = models.ForeignKey(Skill, models.DO_NOTHING, db_column='skillId', blank=True, null=True)  # Field name made lowercase.
    adjustment = models.IntegerField(blank=True, null=True)
    custom = models.CharField(blank=True, null=True)
    source = models.CharField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statsheet_proficiency'


class StatsheetSavingthrow(models.Model):
    statshetid = models.ForeignKey(Statsheet, models.DO_NOTHING, db_column='statshetId')  # Field name made lowercase.
    abilityid = models.ForeignKey(Ability, models.DO_NOTHING, db_column='abilityId')  # Field name made lowercase.
    advantage = models.BooleanField(blank=True, null=True)
    source = models.CharField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statsheet_savingthrow'


class Tag(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    color = models.CharField(blank=True, null=True)
    icon = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tag'


class TagSharedUsers(models.Model):
    tagid = models.ForeignKey(Tag, models.DO_NOTHING, db_column='tagId', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    sharedwithid = models.ForeignKey('User', models.DO_NOTHING, db_column='sharedWithId', related_name='tagsharedusers_sharedwithid_set', blank=True, null=True)  # Field name made lowercase.
    sharedate = models.DateTimeField(db_column='shareDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tag_shared_users'


class User(models.Model):
    username = models.CharField(unique=True, blank=True, null=True)
    email = models.CharField(unique=True, blank=True, null=True)
    fname = models.CharField(db_column='fName', blank=True, null=True)  # Field name made lowercase.
    lname = models.CharField(db_column='lName', blank=True, null=True)  # Field name made lowercase.
    lastonline = models.DateTimeField(db_column='lastOnline', blank=True, null=True)  # Field name made lowercase.
    created = models.DateTimeField(blank=True, null=True)
    password = models.CharField(blank=True, null=True)
    salt = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserCharacters(models.Model):
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    characterid = models.ForeignKey(Character, models.DO_NOTHING, db_column='characterId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_characters'


class UserRequest(models.Model):
    expiry = models.DateTimeField(blank=True, null=True)
    content = models.CharField(blank=True, null=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_request'


class UserRole(models.Model):
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    roleid = models.ForeignKey(Role, models.DO_NOTHING, db_column='roleId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_role'


class UserSetting(models.Model):
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(blank=True, null=True)
    value = models.CharField(blank=True, null=True)
    toggle = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_setting'
