from dataclasses import dataclass
from extensions import db
from sqlalchemy.sql.sqltypes import Text, String, Integer


@dataclass
class Feat(db.Model):
    __tablename__ = 'feat'
    id: int = db.Column(Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(String)
    description: str = db.Column(String)
    requirements: str = db.Column(Text)