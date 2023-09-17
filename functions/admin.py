from aiogram import types
from aiogram.dispatcher import FSMContext
from laguages import *
from keyborads import *
from utils import *
from utils import get_admins


async def add_admin_handler(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    username = await get_username(message, lang)
    
    if username:
        if message.from_id in get_admins():
            await message.answer(admin["already_exist"][lang])
        else:
            await message.answer(admin["added"][lang], reply_markup = await main_menu(message, lang))
            await state.finish()


            