from datetime import datetime

from api.model.classes import *
from api.model.ext_content import *
from api.loghandler.logger import Logger
from sqlalchemy.orm import Query
from api.service.ext_dbservice import Ext_ContentService


class ClassService:
    query = Query(Class, db.session)
    querySubclass = Query(Subclass, db.session)
    queryCSC = Query(ClassSubclasses, db.session)
    queryCT = Query(ClassTable, db.session)

    @classmethod
    def getClassSubclasses(cls, id):
        return cls.query.filter(Class.id == id).first().subclasses

    # Initialize by gathering races from API.
    @classmethod
    def getClassesOnline(cls):
        classRefresh: Ext_Content = Ext_ContentService.getByKey('class_refresh')
        if classRefresh is None:
            # Trigger actual refresh
            # Create the
            # refresh key with the current time
            Ext_ContentService.add(Ext_Content(**{
                'key': 'class_refresh',
                'name': 'Last refresh time for Class table',
                'content': str(datetime.now().timestamp())
            }))
            cls._refresh()
        else:
            # Check if the refresh is older than 1 day
            # If it is, trigger refresh
            # If not, do nothing
            if ((datetime.now().timestamp()) - float(classRefresh.content)) >= 60 * 60 * 24:
                pass
            cls._refresh()

    @classmethod
    def getSubclasses(cls, classId: int):
        return cls.querySubclass.filter_by(classId=classId).all()

    @classmethod
    def getClassTable(cls, classId: int):
        return cls.queryCT.filter_by(classId=classId).first()

    @classmethod
    def getSpellSlotsForLevel(cls, classTable: ClassTable, level: int):
        lv1: list[int] = list(map(lambda x: int(x), str(classTable.level1SpellSlots).split(',')))
        lv2: list[int] = list(map(lambda x: int(x), str(classTable.level2SpellSlots).split(',')))
        lv3: list[int] = list(map(lambda x: int(x), str(classTable.level3SpellSlots).split(',')))
        lv4: list[int] = list(map(lambda x: int(x), str(classTable.level4SpellSlots).split(',')))
        lv5: list[int] = list(map(lambda x: int(x), str(classTable.level5SpellSlots).split(',')))
        lv6: list[int] = list(map(lambda x: int(x), str(classTable.level6SpellSlots).split(',')))
        lv7: list[int] = list(map(lambda x: int(x), str(classTable.level7SpellSlots).split(',')))
        lv8: list[int] = list(map(lambda x: int(x), str(classTable.level8SpellSlots).split(',')))
        lv9: list[int] = list(map(lambda x: int(x), str(classTable.level9SpellSlots).split(',')))

        spellSlots = [
            lv1[level - 1] if len(lv1) >= level else 0,
            lv2[level - 1] if len(lv2) >= level else 0,
            lv3[level - 1] if len(lv3) >= level else 0,
            lv4[level - 1] if len(lv4) >= level else 0,
            lv5[level - 1] if len(lv5) >= level else 0,
            lv6[level - 1] if len(lv6) >= level else 0,
            lv7[level - 1] if len(lv7) >= level else 0,
            lv8[level - 1] if len(lv8) >= level else 0,
            lv9[level - 1] if len(lv9) >= level else 0
        ]
        return spellSlots

    # TODO: Long term project, get this information filled out automatically. For now we pause on the automatic compilation of classes to focus on getting a product out.
    @classmethod
    def updateClassTable(cls, classId, classTableJson):
        classTable = cls.getClassTable(classId)
        if classTable is None:
            classTable = ClassTable()
        if 'profBonus' in classTableJson:
            classTable.profBonus = classTableJson['profBonus']
        if 'cantripsKnown' in classTableJson:
            classTable.cantripsKnown = classTableJson['cantripsKnown']
        if 'spellsKnown' in classTableJson:
            classTable.spellsKnown = classTableJson['spellsKnown']
        if 'level1SpellSlots' in classTableJson:
            classTable.level1SpellSlots = classTableJson['level1SpellSlots']
        if 'level2SpellSlots' in classTableJson:
            classTable.level2SpellSlots = classTableJson['level2SpellSlots']
        if 'level3SpellSlots' in classTableJson:
            classTable.level3SpellSlots = classTableJson['level3SpellSlots']
        if 'level4SpellSlots' in classTableJson:
            classTable.level4SpellSlots = classTableJson['level4SpellSlots']
        if 'level5SpellSlots' in classTableJson:
            classTable.level5SpellSlots = classTableJson['level5SpellSlots']
        if 'level6SpellSlots' in classTableJson:
            classTable.level6SpellSlots = classTableJson['level6SpellSlots']
        if 'level7SpellSlots' in classTableJson:
            classTable.level7SpellSlots = classTableJson['level7SpellSlots']
        if 'level8SpellSlots' in classTableJson:
            classTable.level8SpellSlots = classTableJson['level8SpellSlots']
        if 'level9SpellSlots' in classTableJson:
            classTable.level9SpellSlots = classTableJson['level9SpellSlots']
        db.session.add(classTable)
        db.session.commit()
        return (True, None)
    def delete(cls, classId):
        foundClass = cls.get(classId)

        if not foundClass:
            return False
        try:
            db.session.delete(foundClass)
            db.session.commit()
        except Exception as e:
            Logger.error(e)
            return False, [e.__str__()]
        return True, []

    @classmethod
    def createClass(cls, clazz: Class):
        foundClass = cls.getByName(clazz.name)
        if foundClass is not None:
            return None, ["A class by this name already exists."]

        newClass = Class()
        newClass.description = clazz.description
        newClass.name = clazz.name
        newClass.spellCastingAbility = clazz.spellCastingAbility
        db.session.add(newClass)
        db.session.commit()
        return newClass, []

    @classmethod
    def update(cls, id: int, clazz: Class):
        foundClass = cls.get(id)
        if foundClass:
            if clazz.name:
                foundClass.name = clazz.name
            if clazz.description:
                foundClass.description = clazz.description

            # Spellcasting is nullable, if nothing is sent, it will become nothing.
            foundClass.spellCastingAbility = clazz.spellCastingAbility
            db.session.add(foundClass)
            db.session.commit()
            return foundClass, []
        return None, ["Could not find a class with the given ID"]


    @classmethod
    def _refresh(cls):
        from api.service.dnd5eapiservice import Dnd5eAPIService
        Logger.debug("Refreshing the class database")
        Dnd5eAPIService.getClasses()

    @classmethod
    def getSubclassByName(cls, subclassName: str):
        return cls.querySubclass.filter(Subclass.name.ilike(f"%{subclassName}%")).first()

    @classmethod
    def getByName(cls, className: str):
        return cls.query.filter(Class.name.ilike(f"%{className}%")).first()

    @classmethod
    def getAll(cls):
        cls.getClassesOnline()
        return cls.query.all()

    @classmethod
    def get(cls, id: str):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def getSubclass(cls, id: str):
        return cls.querySubclass.filter_by(id=id).first()
