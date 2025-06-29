import json
from api.model.ext_content import Ext_Content
from sqlalchemy.orm import Query
from extensions import db


class Ext_ContentService:
    query = Query(Ext_Content, db.session)

    @classmethod
    def get(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def getAll(cls):
        return cls.query.all()

    @classmethod
    def getByKey(cls, key) -> Ext_Content | None:
        return cls.query.filter_by(key=key).first()

    @classmethod
    def getAllLikeKey(cls, keyLike):
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

    @classmethod
    def add(cls, content: Ext_Content):
        if content is None:
            return False

        if cls.getByKey(content.key) is not None:
            return False

        newContent = Ext_Content()
        newContent.key = content.key
        newContent.name = content.name
        newContent.content = content.content

        db.session.add(newContent)
        db.session.commit()
        return True
