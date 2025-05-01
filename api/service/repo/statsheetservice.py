from api.model.statsheet import Statsheet
from sqlalchemy.orm import Query
from extensions import db

class StatsheetService:
    query = db.Query(Statsheet, db.session)
