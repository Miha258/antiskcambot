from aiogram import types
from laguages import *

async def support(message: types.Message):
    lang = get_language(message.from_id)
    await message.answer(about_urls["support"][lang], reply_markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(about_urls["folow"][lang], url = "https://telegram.org/apps")],
        
    ]))


async def our_chat(message: types.Message):
    lang = get_language(message.from_id)
    await message.answer(about_urls["chat"][lang], reply_markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(about_urls["folow"][lang], url = "https://telegram.org/apps")],
        
    ]))


async def our_projects(message: types.Message):
    lang = get_language(message.from_id)
    await message.answer(about_urls["projects"][lang], reply_markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(about_urls["folow"][lang], url = "https://telegram.org/apps")],
    ]))