from sqlalchemy.orm import Query
from api.model.ability import Ability
from extensions import db
from api.model.skill import Skill


class SkillService:
    query = db.Query(Skill, db.session)
    
    @classmethod
    def init_default_skills(cls):
        strength = db.session.query(Ability).filter_by(abbreviation="STR").first()
        dexterity = db.session.query(Ability).filter_by(abbreviation="DEX").first()
        intelligence = db.session.query(Ability).filter_by(abbreviation="INT").first()
        wisdom = db.session.query(Ability).filter_by(abbreviation="WIS").first()
        charisma = db.session.query(Ability).filter_by(abbreviation="CHA").first()
        
        
        defaults = [
            Skill(
                name="Acrobatics",
                description="Your Dexterity (Acrobatics) check covers your attempt to stay on your feet in a tricky situation.",
                abilityId=dexterity.id
            ),
            Skill(
                name="Animal Handling",
                description="When there is any question whether you can calm down a domesticated animal, keep a mount from getting spooked, or intuit an animal's intentions, the DM might call for a Wisdom (Animal Handling) check.",
                abilityId=wisdom.id
            ),
            Skill(
                name="Arcana",
                description="Your Intelligence (Arcana) check measures your ability to recall lore about spells, magic items, eldritch symbols, magical traditions, the planes of existence, and the inhabitants of those planes.",
                abilityId=intelligence.id
            ),
            Skill(
                name="Athletics",
                description="Your Strength (Athletics) check covers difficult situations you encounter while climbing, jumping, or swimming.",
                abilityId=strength.id
            ),
            Skill(
                name="Deception",
                description="Your Charisma (Deception) check determines whether you can convincingly hide the truth, either verbally or through your actions.",
                abilityId=charisma.id
            ),
            Skill(
                name="History",
                description="Your Intelligence (History) check measures your ability to recall lore about historical events, legendary people, ancient kingdoms, past disputes, recent wars, and lost civilizations.",
                abilityId=intelligence.id
            ),
            Skill(
                name="Insight",
                description="Your Wisdom (Insight) check decides whether you can determine the true intentions of a creature, such as when searching out a lie or predicting someone's next move.",
                abilityId=wisdom.id
            ),
            Skill(
                name="Intimidation",
                description="When you attempt to influence someone through overt threats, hostile actions, and physical violence, the DM might ask you to make a Charisma (Intimidation) check.",
                abilityId=charisma.id
            ),
            Skill(
                name="Investigation",
                description="When you look around for clues and make deductions based on those clues, you make an Intelligence (Investigation) check.",
                abilityId=intelligence.id
            ),
            Skill(
                name="Medicine",
                description="A Wisdom (Medicine) check lets you try to stabilize a dying companion or diagnose an illness.",
                abilityId=wisdom.id
            ),
            Skill(
                name="Nature",
                description="Your Intelligence (Nature) check measures your ability to recall lore about terrain, plants and animals, the weather, and natural cycles.",
                abilityId=intelligence.id
            ),
            Skill(
                name="Perception",
                description="Your Wisdom (Perception) check lets you spot, hear, or otherwise detect the presence of something.",
                abilityId=wisdom.id
            ),
            Skill(
                name="Performance",
                description="Your Charisma (Performance) check determines how well you can delight an audience with music, dance, acting, storytelling, or some other form of entertainment.",
                abilityId=charisma.id
            ),
            Skill(
                name="Persuasion",
                description="When you attempt to influence someone or a group of people with tact, social graces, or good nature, the DM might ask you to make a Charisma (Persuasion) check.",
                abilityId=charisma.id
            ),
            Skill(
                name="Religion",
                description="Your Intelligence (Religion) check measures your ability to recall lore about deities, rites and prayers, religious hierarchies, holy symbols, and the practices of secret cults.",
                abilityId=intelligence.id
            ),
            Skill(
                name="Sleight of Hand",
                description="Whenever you attempt an act of legerdemain or manual trickery, such as planting something on someone else or concealing an object on your person, make a Dexterity (Sleight of Hand) check.",
                abilityId=dexterity.id
            ),
            Skill(
                name="Stealth",
                description="Make a Dexterity (Stealth) check when you attempt to conceal yourself",
                abilityId=dexterity.id,
            ),
            Skill(
                name="Survival",
                description="The DM might ask you to make a Wisdom (Survival) check to follow tracks, hunt wild game, guide your group through frozen wastelands, identify signs that owlbears live nearby, predict the weather, or avoid quicksand and other natural hazards.",
                abilityId=wisdom.id
            )
        ]
        
        existing_by_name = {
            row[0] for row in db.session.query(Skill.name).all()
        }
        
        for dt in defaults:
            if dt.name not in existing_by_name:
                db.session.add(dt)

        db.session.commit()

    @classmethod
    def get(cls, id: str):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def getAll(cls):
        return cls.query.all()
    
    
