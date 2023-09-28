from sqlalchemy import String, Float, Boolean, DateTime, Integer
from . import db


class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String)
    description = db.Column(String)
    # 0: Weapon
    # 1: Armor
    # 2: Consumable
    # 3: Tool
    # 4: Misc
    type = db.Column(Integer)


    query = db.Query