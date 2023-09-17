from .db import UserTable, db
from datetime import datetime


class Users(UserTable):
    table = "users"

    @classmethod
    async def init_table(cls):
        await db.create_table(cls.table, {
            "id": "INT",
            "username": "TEXT",
            "added_in": "DATE",
        })

    @classmethod
    async def all(cls):
        return await db.get_all_records(cls.table)

    @classmethod
    async def add(cls, id: int, username: str):
        await db.create_record(cls.table, id = id, username = username, added_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
    @classmethod
    async def get_by_id(cls, id: int):
        return await db.read_record(cls.table, "id", id)

    @classmethod
    async def remove(cls, id: int):
        await db.delete_record(cls.table, id)