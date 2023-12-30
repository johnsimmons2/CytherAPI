import json
from api.model import db
from api.model.ext_content import Ext_Content
from sqlalchemy.orm import Query


class Ext_ContentService:
    query = Query(Ext_Content, db.session)

    @classmethod
    def get(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def getAll(cls):
        return cls.query.all()
    
    @classmethod
    def getByKey(cls, key):
        return cls.query.filter_by(key=key).first()
    
    @classmethod
    def getAllLikeKey(cls, keyLike):
        result = cls.query.filter(Ext_Content.key.like('%' + keyLike + '%')).all()
        print(result)
        return cls.query.filter(Ext_Content.key.like('%' + keyLike + '%')).all()
    
    @classmethod
    def update(cls, id, data):
        if data is None:
            return False
        
        if 'key' not in data or 'name' not in data or 'data' not in data:
            return False

        if id is None:
            if cls.getByKey(data['key']) is None:
                content = Ext_Content()
                db.session.add(content)
            else:
                content = cls.getByKey(data['key'])
        else:
            content = cls.get(id)
            if content is None:
                return False
            
        content.key = data['key']
        content.name = data['name']
        content.content = data['data']
        db.session.commit()
        return True