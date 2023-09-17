from .db import UserTable, db
from datetime import datetime

class Adds(UserTable):
    table = "adds"
    
    @classmethod
    async def init_table(cls):
        await db.create_table(cls.table, {
            "id": "INT",
            "text": "TEXT",
            "date": "DATATIME",
            "count": "INT",
            "media": "BLOB"
        })

    @classmethod
    async def all(cls):
        return await db.get_all_records(cls.table)

    @classmethod
    async def add(cls, id: int, text: str, date: datetime, count: int, media: bytes):
        await db.create_record(cls.table, id = id, text = text, date = date, count = count, media = media)

    @classmethod
    async def set_count(cls, id: int, new_count: int):
        return await db.update_record(cls.table, "id", id, count = new_count)

    @classmethod
    async def remove(cls, id: int):
        await db.delete_record(cls.table, id)
