from aiogram import types, Dispatcher
from laguages import *
from states import *
from utils import get_su_admins
from main import bot
from aiogram.dispatcher import FSMContext

async def support(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    await message.answer(about_urls["support"][lang])
    await state.set_state(BotStates.SEND_REPORT)

async def send_support(message: types.Message):
    lang = get_language(message.from_id)
    await message.answer(about_urls["support_accepted"][lang])
    for admin in get_su_admins():
        await bot.send_message(admin, about_urls["notify_support"][lang](message.from_user.mention, message.text))


async def our_chat(message: types.Message):
    lang = get_language(message.from_id)
    await message.answer(about_urls["chat"][lang], reply_markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(about_urls["folow"][lang], url = "https://t.me/closedlist")],
    ]))


async def our_projects(message: types.Message):
    lang = get_language(message.from_id)
    await message.answer(about_urls["projects"][lang], reply_markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(about_urls["folow"][lang], url = "https://t.me/closedlist")],
    ]))


def register_links(dp: Dispatcher):
    dp.register_message_handler(send_support, state = BotStates.SEND_REPORT)