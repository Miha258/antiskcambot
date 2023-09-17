from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from db.blacklist import *
from laguages import *
from states import *
from utils import *
from keyborads import *
from client import *
from db.blacklist import Blacklist
from db.adds import *
from random import randint
from keyborads import main_menu

async def verify_user(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    username = await get_username(message)
    user_id = await get_user_id(message.text)
    
    if not username and not user_id:
        await message.answer(user["invalid_data"][lang])
    else:
        target = await Blacklist.get_by_username(username) or await Blacklist.get_by_id(user_id)
        if target: 
            id = target.get("id")
            usarname = target.get("username")
            added_in = target.get("added_in")
            await message.answer(blacklist[lang](usarname if usarname else message.from_user.full_name, id, added_in), parse_mode = "html", reply_markup = await main_menu(message, lang))
        else:
            await message.answer(user["not_found"][lang], reply_markup = await main_menu(message, lang))
        await state.finish()


async def add_to_database(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    username = await get_username(message)
    user_id = await get_user_id(message.text)
    
    if not re.search(r'(@\w+ - https:\/\/\S+)', message.text):
        return await message.answer(user["invalid_link"][lang])
    
    link = message.text.split('-')[0]
    target = None
    target_id = None
    if username:
        target_id = await search_user(username)
        target = await Blacklist.get_by_id(target_id)
    elif user_id:
        target_id = user_id
        target = await Blacklist.get_by_id(user_id)
    if target:
        await message.answer(user["already_exsists"][lang], reply_markup = await main_menu(message, lang))
    else:
        await Blacklist.add(target_id, link, username)
        await message.answer(user["added"][lang], reply_markup = await main_menu(message, lang))
    await state.finish()


async def delete_from_database(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    username = await get_username(message)
    user_id = await get_user_id(message.text)
    
    target = None
    target_id = None
    if username:
        target_id = await search_user(username)
        target = await Blacklist.get_by_id(target_id)
    elif user_id:
        target_id = user_id
        target = await Blacklist.get_by_id(user_id)
        
    if target:
        await Blacklist.remove(target_id)
        await message.answer(user["deleted"][lang], reply_markup = await main_menu(message, lang))
    else:
        await message.answer(user["not_found"][lang], reply_markup = await main_menu(message, lang))
    
    await state.finish()
  

async def detect_scammer(message: types.Message):
    lang = get_language(message.from_id)
    username = message.from_user.mention
    target = await Blacklist.get_by_username(username) or await Blacklist.get_by_id(message.from_id)
    
    if target:
        id = target.get("id")
        usarname = target.get("username")
        added_in = target.get("added_in")
        await message.reply(blacklist[lang](usarname if usarname else message.from_user.full_name, id, added_in), parse_mode = "html")
        
        adds = list(filter(lambda add: datetime.now() > datetime.strptime(add.get("date"), "%Y-%m-%d %H:%M:%S"), await Adds.all()))
        show = randint(0, 4)
        
        if adds and not show:
            add = adds[0]
            if add.get("count") == 0:
                await Adds.remove(add.get("id"))
            else:
                if datetime.now() > datetime.strptime(add.get("date"), "%Y-%m-%d %H:%M:%S"):
                    media = add.get("media")
                    await Adds.set_count(add.get("id"), add.get("count") - 1)
                    if media:
                        await message.answer_photo(media, add.get("text"))
                    else:
                        await message.answer(add.get("text"))


def register_users(dp: Dispatcher):
    dp.register_message_handler(verify_user, state = BotStates.VERIFY_USER)
    dp.register_message_handler(add_to_database, state = BotStates.ADD_USER)
    dp.register_message_handler(delete_from_database, state = BotStates.DELETE_USER)
    dp.register_message_handler(detect_scammer, lambda m: m.chat.type == "supergroup" or m.chat.type == "group")