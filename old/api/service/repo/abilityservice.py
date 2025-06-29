# Abilities and ability score calculations perchance


from api.model.ability import Ability
from extensions import db
from sqlalchemy.orm import Query


class AbilityService:
    @classmethod
    def init_default_abilities(cls):
        defaults = [
            Ability(name="Strength", abbreviation="STR", min=1, max=20, description="Strength measures bodily power, athletic training, and the extent to which you can exert raw physical force."),
            Ability(name="Dexterity", abbreviation="DEX", min=1, max=20, description="Dexterity measures agility, reflexes, and balance."),
            Ability(name="Constitution", abbreviation="CON", min=1, max=20, description="Constitution measures health, stamina, and vital force."),
            Ability(name="Intelligence", abbreviation="INT", min=1, max=20, description="Intelligence measures mental acuity, accuracy of recall, and the ability to reason."),
            Ability(name="Wisdom", abbreviation="WIS", min=1, max=20, description="Wisdom reflects how attuned you are to the world around you and represents perceptiveness and intuition."),
            Ability(name="Charisma", abbreviation="CHA", min=1, max=20, description="Charisma measures your ability to interact effectively with others. It includes such factors as confidence and eloquence, and it can represent a charming or commanding personality.")
        ]
        
        existing_by_name = {
            row[0] for row in db.session.query(Ability.name).all()
        }
        
        for ability in defaults:
            if ability.name not in existing_by_name:
                db.session.add(ability)

        db.session.commit()
    
    @classmethod
    def get(cls, ability_id):
        return db.session.query(Ability).filter(Ability.id == ability_id).first()
    
    @classmethod
    def getAll(cls):
        return db.session.query(Ability).all()
    
    @classmethod
    def get_ability_by_abbreviation(cls, abbr: str) -> Ability:
        return db.session.query(Ability).filter_by(abbreviation=abbr).first()
