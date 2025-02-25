from api.model.character import CharacterCondition
from api.model.condition import Condition, ConditionEffect
from extensions import db
from sqlalchemy.orm import Query


class ConditionsService:
    @classmethod
    def init_default_conditions(cls):
        defaults = [
            [
                Condition(name="Blinded",
                    description="A blinded creature can't see and automatically fails any ability check that requires sight."),
                ConditionEffect(
                    description="Attack rolls against the creature have advantage, and the creature's attack rolls have disadvantage.",
                    rollType="attack",
                    rollDisadvantage=True
                ),
                ConditionEffect(
                    description="The creature fails any ability check that requires sight.",
                    rollType="ability",
                    rollDisadvantage=True
                )
            ],
            [
                Condition(name="Charmed",
                    description="A charmed creature can't attack the charmer or target the charmer with harmful abilities or magical effects."),
                ConditionEffect(
                    description="The charmer has advantage on any ability check to interact socially with the creature.",
                    rollType="ability",
                    rollAdvantage=True
                )
            ],
            [
                Condition(name="Deafened",
                    description="A deafened creature can't hear and automatically fails any ability check that requires hearing."),
                ConditionEffect(
                    description="The creature has disadvantage on any ability check that requires hearing.",
                    rollType="ability",
                    rollDisadvantage=True
                )
            ],
            [
                Condition(name="Frightened",
                    description="A frightened creature has disadvantage on ability checks and attack rolls while the source of its fear is within line of sight."),
                ConditionEffect(
                    description="The creature has disadvantage on ability checks while the source of its fear is in sight.",
                    rollType="ability",
                    rollDisadvantage=True
                ),
                ConditionEffect(
                    description="The creature has disadvantage on attack rolls while the source of its fear is in sight.",
                    rollType="attack",
                    rollDisadvantage=True
                ),
                ConditionEffect(
                    description="The creature can't willingly move closer to the source of its fear.",
                )
            ],
            [
                Condition(name="Grappled",
                    description="A grappled creature's speed becomes 0, and it can't benefit from any bonus to its speed."),
            ],
            [
                Condition(name="Incapacitated",
                    description="An incapacitated creature can't take actions or reactions."),
            ],
            [
                Condition(name="Invisible",
                    description="An invisible creature is impossible to see without the aid of magic or a special sense."),
                ConditionEffect(
                    description="An invisible creature is heavily obscured for the purpose of hiding."
                ),
                ConditionEffect(
                    description="An invisible creature has advantage on attack rolls.",
                    rollType="attack",
                    rollAdvantage=True
                ),
                ConditionEffect(
                    description="An invisible creature has disadvantage on attack rolls against it.",
                )
            ],
            [
                Condition(
                    name="Paralyzed",
                    description="A paralyzed creature is incapacitated and can't move or speak.",
                ),
                ConditionEffect(
                    description="The creature automatically fails Strength and Dexterity saving throws.",
                    rollType="save",
                    rollDisadvantage=True
                ),
                ConditionEffect(
                    description="Attack rolls against the creature have advantage.",
                ),
                ConditionEffect(
                    description="Any attack that hits the creature is a critical hit if the attacker is within 5 feet of the creature.",
                )
            ],
            [
                Condition(
                    name="Petrified",
                    description="A petrified creature is transformed, along with any nonmagical object it is wearing or carrying, into a solid inanimate substance (usually stone)."
                ),
                ConditionEffect(
                    description="The creature is incapacitated, can't move or speak, and is unaware of its surroundings.",
                ),
                ConditionEffect(
                    description="The creature automatically fails Strength and Dexterity saving throws.",
                    rollType="save",
                    rollDisadvantage=True
                ),
                ConditionEffect(
                    description="The creature has resistance to all damage.",
                ),
                ConditionEffect(
                    description="The creature is immune to poison and disease, although a poison or disease already in its system is suspended, not neutralized.",
                )
            ],
            [
                Condition(
                    name="Poisoned",
                    description="A poisoned creature has disadvantage on attack rolls and ability checks."
                ),
                ConditionEffect(
                    description="The creature has disadvantage on attack rolls.",
                    rollType="attack",
                    rollDisadvantage=True
                ),
                ConditionEffect(
                    description="The creature has disadvantage on ability checks.",
                    rollType="ability",
                    rollDisadvantage=True
                )
            ],
            [
                Condition(
                    name="Prone",
                    description="A prone creature's only movement option is to crawl, unless it stands up and thereby ends the condition."
                ),
                ConditionEffect(
                    description="The creature has disadvantage on attack rolls.",
                    rollType="attack",
                    rollDisadvantage=True
                ),
                ConditionEffect(
                    description="An attack roll against the creature has advantage if the attacker is within 5 feet of the creature. Otherwise, the attack roll has disadvantage.",
                )
            ],
            [
                Condition(
                    name="Restrained",
                    description="A restrained creature's speed becomes 0, and it can't benefit from any bonus to its speed."
                ),
                ConditionEffect(
                    description="Attack rolls against the creature have advantage.",
                ),
                ConditionEffect(
                    description="The creature's attack rolls have disadvantage.",
                    rollType="attack",
                    rollDisadvantage=True
                ),
                ConditionEffect(
                    description="The creature has disadvantage on Dexterity saving throws.",
                    rollType="save",
                    rollDisadvantage=True
                )
            ],
            [
                Condition(
                    name="Stunned",
                    description="A stunned creature is incapacitated, can't move, and can speak only falteringly."
                ),
                ConditionEffect(
                    description="The creature automatically fails Strength and Dexterity saving throws.",
                    rollType="save",
                    rollDisadvantage=True
                ),
                ConditionEffect(
                    description="Attack rolls against the creature have advantage.",
                )
            ],
            [
                Condition(
                    name="Unconscious",
                    description="An unconscious creature is incapacitated, can't move or speak, and is unaware of its surroundings."
                ),
                ConditionEffect(
                    description="The creature drops whatever it's holding and falls prone.",
                ),
                ConditionEffect(
                    description="The creature automatically fails Strength and Dexterity saving throws.",
                    rollType="save",
                    rollDisadvantage=True
                ),
                ConditionEffect(
                    description="Attack rolls against the creature have advantage.",
                ),
                ConditionEffect(
                    description="Any attack that hits the creature is a critical hit if the attacker is within 5 feet of the creature.",
                )
            ],
            [
                Condition(
                    name="Exhaustion (1)",
                    description="Disadvantage on ability checks."
                )
            ],
            [
                Condition(
                    name="Exhaustion (2)",
                    description="Speed halved."
                )
            ],
            [
                Condition(
                    name="Exhaustion (3)",
                    description="Disadvantage on attack rolls and saving throws."
                ),
                ConditionEffect(
                    description="The creature has disadvantage on attack rolls.",
                    rollType="attack",
                    rollDisadvantage=True
                ),
                ConditionEffect(
                    description="The creature has disadvantage on all saving throws.",
                    rollType="save",
                    rollDisadvantage=True
                )
            ],
            [
                Condition(
                    name="Exhaustion (4)",
                    description="Hit point maximum halved." # Plummet the user's constitution
                )
            ],
            [
                Condition(
                    name="Exhaustion (5)",
                    description="Speed reduced to 0."
                )
            ],
            [
                Condition(
                    name="Exhaustion (6)",
                    description="Death."
                )
            ]
        ]
        
        for group in defaults:
            condition_obj = group[0]  # First element is always the Condition
            effect_objs = group[1:]   # Subsequent elements are ConditionEffects

            # 1) Check if condition already exists by name
            existing_condition = db.session.query(Condition).filter_by(
                name=condition_obj.name
            ).first()

            if existing_condition:
                condition_record = existing_condition
            else:
                db.session.add(condition_obj)
                db.session.flush()  # ensures condition_obj.id is available
                condition_record = condition_obj

            # 2) For each ConditionEffect, check if it already exists for this Condition
            for eff_obj in effect_objs:
                existing_effect = db.session.query(ConditionEffect).filter_by(
                    conditionId=condition_record.id,
                    description=eff_obj.description
                ).first()

                if not existing_effect:
                    eff_obj.conditionId = condition_record.id
                    db.session.add(eff_obj)

        db.session.commit()
    
    @classmethod
    def getAll(cls):
        return db.session.query(Condition).all()
    
    @classmethod
    def getEffectsFor(cls, id: str):
        return db.session.query(ConditionEffect).filter(ConditionEffect.conditionId == id).all()

    @classmethod
    def get(cls, id: str):
        return db.session.query(Condition).filter(Condition.id == id).first()
    
    @classmethod
    def getByName(cls, name: str):
        return db.session.query(Condition).filter(Condition.name == name).first()
    
    @classmethod
    def createCondition(cls, condition: Condition) -> Condition | None:
        if cls.getByName(condition.name) is not None:
            return None
        
        newCondition = Condition()
        newCondition.name = condition.name
        newCondition.description = condition.description
        newCondition.source = condition.source
        
        db.session.add(newCondition)
        db.session.commit()
        
        return newCondition
    
    @classmethod
    def addEffectToCondition(cls, effect: ConditionEffect) -> ConditionEffect | None:
        existing_condition = cls.get(effect.conditionId)
        
        if not existing_condition:
            return None
        
        newEffect = ConditionEffect()
        newEffect.conditionId = effect.conditionId
        newEffect.description = effect.description
        newEffect.vulnerableId = effect.vulnerableId
        newEffect.resistantId = effect.resistantId
        newEffect.immuneId = effect.immuneId
        newEffect.abilityId = effect.abilityId
        newEffect.abilityAdj = effect.abilityAdj
        newEffect.skillId = effect.skillId
        newEffect.skillAdj = effect.skillAdj
        newEffect.rollAdvantage = effect.rollAdvantage
        newEffect.rollDisadvantage = effect.rollDisadvantage
        newEffect.rollType = effect.rollType
        
        db.session.add(newEffect)
        db.session.commit()
        return newEffect
    
    @classmethod
    def removeEffectFrom(cls, conditionId: str, effectId: str) -> bool:
        effect = db.session.query(ConditionEffect).filter(
            ConditionEffect.conditionId == conditionId,
            ConditionEffect.id == effectId
        ).first()
        
        if not effect:
            return False
        
        db.session.delete(effect)
        db.session.commit()
        return True
    
    @classmethod
    def addConditionToCharacter(cls, conditionId: str, characterId: str, source: str, duration: str, stacks: int) -> bool:
        newCondition = CharacterCondition()
        newCondition.characterId = characterId
        newCondition.conditionId = conditionId
        newCondition.source = source
        newCondition.duration = duration
        newCondition.stacks = stacks
        
        db.session.add(newCondition)
        db.session.commit()
        return True
    
    @classmethod
    def updateCondition(cls, condition: Condition) -> Condition | None:
        existing_condition = cls.get(condition.id)
        
        if not existing_condition:
            return None
        
        existing_condition.name = condition.name
        existing_condition.description = condition.description
        existing_condition.source = condition.source
        
        db.session.commit()
        return existing_condition
    
    @classmethod
    def updateConditionEffect(cls, conditionEffect: ConditionEffect) -> ConditionEffect | None:
        existing_effect = db.session.query(ConditionEffect).filter(
            ConditionEffect.conditionId == conditionEffect.conditionId,
            ConditionEffect.id == conditionEffect.id
        ).first()
        
        if not existing_effect:
            return None
        
        existing_effect.description = conditionEffect.description
        existing_effect.vulnerableId = conditionEffect.vulnerableId
        existing_effect.resistantId = conditionEffect.resistantId
        existing_effect.immuneId = conditionEffect.immuneId
        existing_effect.abilityId = conditionEffect.abilityId
        existing_effect.abilityAdj = conditionEffect.abilityAdj
        existing_effect.skillId = conditionEffect.skillId
        existing_effect.skillAdj = conditionEffect.skillAdj
        existing_effect.rollAdvantage = conditionEffect.rollAdvantage
        existing_effect.rollDisadvantage = conditionEffect.rollDisadvantage
        existing_effect.rollType = conditionEffect.rollType
        
        db.session.commit()
        return existing_effect
    
    @classmethod
    def updateCharacterCondition(cls, characterCondition: CharacterCondition) -> CharacterCondition | None:
        existing_condition = db.session.query(CharacterCondition).filter(
            CharacterCondition.characterId == characterCondition.characterId,
            CharacterCondition.conditionId == characterCondition.conditionId
        ).first()
        
        if not existing_condition:
            return None
        
        existing_condition.source = characterCondition.source
        existing_condition.duration = characterCondition.duration
        existing_condition.stacks = characterCondition.stacks
        
        db.session.commit()
        return existing_condition
    
    @classmethod
    def removeConditionFromCharacter(cls, conditionId: str, characterId: str):
        condition = db.session.query(CharacterCondition).filter(
            CharacterCondition.characterId == characterId,
            CharacterCondition.conditionId == conditionId
        ).first()
        
        if not condition:
            return False
        
        db.session.delete(condition)
        db.session.commit()
        return True
    
    @classmethod
    def getConditionsForCharacter(cls, characterId: str) -> Query:
        return db.session.query(CharacterCondition).filter(CharacterCondition.characterId == characterId)