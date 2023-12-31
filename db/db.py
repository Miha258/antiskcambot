import aiosqlite
import asyncio
from abc import ABC, abstractclassmethod

class DocumentAlreadyExists(Exception):
    pass

class DocumentNotFound(Exception):
    pass


class DB:
    def __init__(self, db_file):
        self.db_file = db_file

    async def __call__(self):
        self.conn = await aiosqlite.connect(self.db_file, check_same_thread = False)
        self.conn.isolation_level = None
        self.cursor = await self.conn.cursor()
        return self

    async def create_table(self, name: str, schema: dict):
        column_definitions = ', '.join([f'{column} {data_type}' for column, data_type in schema.items()])
        query = f"CREATE TABLE IF NOT EXISTS {name} ({column_definitions})"
        await self.cursor.execute(query)
        
    async def drop_table(self, table: str):
        await self.cursor.execute(f"DROP TABLE IF EXISTS {table}")

    async def create_record(self, table: str, **data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])

        if not await self.read_record(table, "id", data["id"], True):
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            await self.cursor.execute(query, list(data.values()))
        else:
            raise DocumentAlreadyExists

    async def read_record(self, table: str, by: str, value, all: bool = False):
        query = f"SELECT * FROM {table} WHERE {by} = ?"
        await self.cursor.execute(query, (value,))
        records = await self.cursor.fetchall()

        column_names = [column[0] for column in self.cursor.description]
        records_dicts = [dict(zip(column_names, record)) for record in records]

        return records_dicts if all else records_dicts [0] if records_dicts else None
       
    async def get_all_records(self, table: str):
        query = f"SELECT * FROM {table}"
        await self.cursor.execute(query)
        records = await self.cursor.fetchall()
        column_names = [column[0] for column in self.cursor.description]
        records_dicts = [dict(zip(column_names, record)) for record in records]

        return records_dicts


    async def update_record(self, table: str, by, value, **data):
        columns = ', '.join(f"{column} = ?" for column in data.keys())
        if await self.read_record(table, by, value, True):
            query = f"UPDATE {table} SET {columns} WHERE id = ?"
            await self.cursor.execute(query, list(data.values()) + [value])
        else:
            raise DocumentNotFound

    async def delete_record(self, table: str, record_id: int):
        if await self.read_record(table, "id", record_id, True):
            query = f"DELETE FROM {table} WHERE id = ?"
            await self.cursor.execute(query, (record_id,))
        else:
            raise DocumentNotFound



class UserTable(ABC):
    table = "user_table"
    
    @abstractclassmethod
    async def init_table(cls):
        pass

    @abstractclassmethod
    async def add(cls, id: int):
        pass

    @abstractclassmethod
    async def get_by_id(cls, id: int):
        pass

    @abstractclassmethod
    async def remove(cls, id: int):
        pass

loop = asyncio.get_event_loop()
db = loop.run_until_complete(DB("blacklist.db")())