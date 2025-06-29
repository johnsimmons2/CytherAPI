from dataclasses import dataclass
from extensions import db
from sqlalchemy import Boolean, DateTime, Integer, String, Text


# External content to host on the same API service (to be cheap), does not affect CytherNet.
@dataclass
class Ext_Content(db.Model):
    __tablename__ = 'ext_content'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)

    # The key used to reference the row. "example_key_name"
    key: str = db.Column(String(255))

    # The readable text name to be displayed. "Example Key Name"
    name: str = db.Column(String(255))

    # Extra content to be displayed, can be json format.
    content: str = db.Column(Text)
    
    userId: int = db.Column(Integer)
    characterId: int = db.Column(Integer)
    value: int = db.Column(Integer)
    previousValue: int = db.Column(Integer)
    active: bool = db.Column(Boolean)
    created: str = db.Column(DateTime)
    updated: str = db.Column(DateTime)