from .db import UserTable, db
from datetime import datetime
import uuid



class Adds(UserTable):
    table = "adds"
    
    @classmethod
    async def init_table(cls):
        await db.create_table(cls.table, {
            "id": "INT",
            "text": "TEXT",
            "date": "DATATIME",
            "count": "INT",
            "media": "BLOB",
        })

    @classmethod
    async def all(cls):
        return await db.get_all_records(cls.table)

    @classmethod
    async def add(cls, id: int, text: str, date: datetime, count: int, media: bytes, media_type: str):
        await db.create_record(cls.table, id = id, text = text, date = date, count = count, media = media, media_type = media_type)

    @classmethod
    async def set_count(cls, id: int, new_count: int):
        return await db.update_record(cls.table, "id", id, count = new_count)

    @classmethod
    async def remove(cls, id: int):
        await db.delete_record(cls.table, id)



class AddsShown():
    table = "adds_shown"

    @classmethod
    async def init_table(cls):
        await db.create_table(cls.table, {
            "id": "INT",
            "adds_id": "INT",
            "user_id": "INT"
        })

    @classmethod
    async def show_for(cls, user_id: int, adds_id: int):
        return await db.create_record(cls.table, id = int(str(uuid.uuid4().int)[:16]), user_id = user_id, adds_id = adds_id)
    

    @classmethod
    async def is_shown_for(cls, user_id: int, adds_id: int):
        adds = await db.read_record(cls.table, "adds_id", adds_id, True)
        if adds:
            return list(filter(lambda user: user['user_id'] == user_id, adds))
