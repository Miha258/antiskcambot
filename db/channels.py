from .db import UserTable, db
from datetime import datetime

class Channels(UserTable):
    table = "channels"

    @classmethod
    async def init_table(cls):
        await db.create_table(cls.table, {
            "id": "INT",
            "user_id": "TEXT",
            "subscription_to": "DATE",
        })
    @classmethod
    async def all(cls):
        return await db.get_all_records(cls.table)

    @classmethod
    async def add(cls, id: int, user_id: str, subscription_to: datetime = None):
        await db.create_record(cls.table, id = id, user_id = user_id, subscription_to = subscription_to)
            
    @classmethod
    async def get_by_id(cls, id: int):
        return await db.read_record(cls.table, "id", id)
    
    @classmethod
    async def get_by_user_id(cls, user_id: int):
        return await db.read_record(cls.table, "user_id", user_id)
    
    @classmethod
    async def set_sub(cls, id: int, subscription_to: datetime):
        return await db.update_record(cls.table, "id", id, subscription_to = subscription_to  )

    @classmethod
    async def remove(cls, id: int):
        await db.delete_record(cls.table, id)



