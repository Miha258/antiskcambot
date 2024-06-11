from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from states import BotStates
from laguages import *
from keyborads import *
from filters import IsSuperAdminFilter
from utils import get_admins
from client import search_user
from utils import *


async def add_admin_handler(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    username = await get_username(message)
    if username:
        user_id = await search_user(username)
        if user_id:
            if username in get_admins():
                await message.answer(admin["already_exist"][lang])
            else:
                add_admin(user_id)
                await message.answer(admin["added"][lang], reply_markup = await main_menu(message, lang))
                await state.finish()
        else:
            await message.answer(admin["username_not_found"][lang])
    else:
        await message.answer(admin["username_not_found"][lang])


async def remove_admin_handler(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    username = await get_username(message)
    print(username)
    if username:
        user_id = await search_user(username)
        if user_id:
            if str(message.from_id) not in get_admins():
                await message.answer(admin["not_exist"][lang])
            else:
                delete_admin(user_id)
                await message.answer(admin["removed"][lang], reply_markup = await main_menu(message, lang))
                await state.finish()
        else:
            await message.answer(admin["username_not_found"][lang])
    else:
        await message.answer(admin["username_not_found"][lang])



def register_admins(dp: Dispatcher):
    dp.register_message_handler(add_admin_handler, IsSuperAdminFilter(), state = BotStates.ADD_ADMIN)
    dp.register_message_handler(remove_admin_handler, IsSuperAdminFilter(), state = BotStates.REMOVE_ADMIN)