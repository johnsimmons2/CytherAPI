from api.model.damage_type import DamageType
from extensions import db
from sqlalchemy.orm import Query


class DamageTypeService:
    @classmethod
    def init_default_damage_types(cls):
        defaults = [
            DamageType(name="Acid", description="A corrosive substance that dissolves matter and causes chemical burns.", icon="acid"),
            DamageType(name="Bludgeoning", description="Damage from blunt force impacts, such as clubs, maces, or falling.", icon="hammer"),
            DamageType(name="Cold", description="Blistering ice that numb and shred flesh.", icon="cold"),
            DamageType(name="Fire", description="Burning flames, intense heat, and scorching wounds.", icon="fire"),
            DamageType(name="Force", description="Pure magical energy or telekinetic force that crushes or propels targets.", icon="force"),
            DamageType(name="Lightning", description="Electricity, intense arcs of power that shock and burn.", icon="lightning"),
            DamageType(name="Necrotic", description="Malevolent energies draining life force or vitality", icon="necrotic"),
            DamageType(name="Piercing", description="Puncturing attacks from arrows, spears, or other pointed weapons.", icon="piercing"),
            DamageType(name="Poison", description="Toxic substances that contaminate and damage biological systems.", icon="poison"),
            DamageType(name="Psychic", description="Mental assaults, illusions, or telepathic damage.", icon="psychic"),
            DamageType(name="Radiant", description="Holy or divine light that sears and purifies.", icon="radiant"),
            DamageType(name="Slashing", description="Cuts from bladed or edged weapons such as swords or claws.", icon="slashing"),
            DamageType(name="Thunder", description="Concussive blasts of sound or shockwaves.", icon="thunder"),
        ]
        
        existing_by_name = {
            row[0] for row in db.session.query(DamageType.name).all()
        }
        
        for dt in defaults:
            if dt.name not in existing_by_name:
                db.session.add(dt)

        db.session.commit()
    
    @classmethod
    def getAll(cls):
        return db.session.query(DamageType).all()
    