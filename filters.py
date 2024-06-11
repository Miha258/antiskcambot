from aiogram.dispatcher.filters import BoundFilter
from laguages import *
from utils import *
from aiogram import types 

class IsAdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_myself):
        self.is_myself = is_myself

    async def check(self, message: types.Message):
        admins = get_admins() 
        return str(message.from_id) in admins 
    

class IsSuperAdminFilter(BoundFilter):
    key = 'is_super_admin'

    async def check(self, message: types.Message):
        su_admins = get_su_admins() 
        return str(message.from_id) in su_admins


class IsDM(BoundFilter):
    key = 'is_dm'

    def __init__(self, is_dm):
        self.is_dm = is_dm

    async def check(self, message: types.Message):
        if self.is_dm:
            return message.chat.type == "private" or message.text == "/chat_id"
        return False
