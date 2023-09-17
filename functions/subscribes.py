from aiogram import types
from db.channels import Channels
from db.users import Users
from laguages import subscribes, get_language


async def subscribe_to_bot(message: types.Message):
    lang = get_language(message.from_id)
    amount = len(await Users.all())
    await message.answer(subscribes["users"][lang](amount), parse_mode = "html")

async def subscribe_to_bot_chats(message: types.Message):
    lang = get_language(message.from_id)
    amount = len(await Channels.all())
    await message.answer(subscribes["channels"][lang](amount), parse_mode = "html")