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
from keyborads import main_menu


async def show_adds_for_user(message: types.Message):
    adds = list(filter(lambda add: datetime.now() > datetime.strptime(add.get("date"), "%Y-%m-%d %H:%M:%S"), await Adds.all()))
    if adds:
        add = adds[0]
        if not await AddsShown.is_shown_for(message.from_id, add["id"]):
            if add.get("count") == 0:
                await Adds.remove(add.get("id"))
            else:
                if datetime.now() > datetime.strptime(add.get("date"), "%Y-%m-%d %H:%M:%S"):
                    media = add.get("media")
                    text = add.get("text")
                    await Adds.set_count(add.get("id"), add.get("count") - 1)
                    await AddsShown.show_for(message.from_id, add["id"])
                    if media:
                        media_type = add["media_type"]
                        if media_type == 'photo':
                            await message.answer_photo(media, text)
                        elif media_type == 'video':
                            await message.answer_video(media, text)
                    else:
                        await message.answer(text)


async def verify_user(message: types.Message, state: FSMContext):
    await state.finish()
    lang = get_language(message.from_id)
    username = await get_username(message)
    user_id = await get_user_id(message.text, True)
    
    await show_adds_for_user(message)
    if not username and not user_id:
        await message.answer(user["invalid_data"][lang])
    else:
        target = await search_user(username)
        if target: 
            target = await Blacklist.get_by_id(target)
            if target:
                id = target.get("id")
                usarname = target.get("username")
                added_in = target.get("added_in")
                link = target.get("link")
                return await message.answer(blacklist[lang](usarname if usarname else message.from_user.full_name, id, added_in, link), parse_mode = "html", reply_markup = await main_menu(message, lang))
            else:
                return await message.answer(user["not_found"][lang], reply_markup = await main_menu(message, lang))
        else:
            if isinstance(user_id, list):
                await message.answer(user["not_found"][lang], reply_markup = await main_menu(message, lang))
            elif isinstance(user_id, str):
                target = await Blacklist.get_by_id(target)
                if target:
                    id = target.get("id")
                    usarname = target.get("username")
                    added_in = target.get("added_in")
                    link = target.get("link")
                    return await message.answer(blacklist[lang](usarname if usarname else message.from_user.full_name, id, added_in, link), parse_mode = "html", reply_markup = await main_menu(message, lang))
                else:
                    return await message.answer(user["not_found"][lang], reply_markup = await main_menu(message, lang))
            else:
                await message.answer(user["not_found"][lang], reply_markup = await main_menu(message, lang))


async def add_to_database(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    username = await get_username(message)
    user_id = await get_user_id(message.text, True)

    if not re.search(r'(https:\/\/\S+)', message.text):
        return await message.answer(user["invalid_link"][lang])
    
    link = message.text.split('-')[1]
    target = None
    target_id = None
    if username:
        target_id = await search_user(username)
        if not target_id:
            return await message.answer(user["username_not_found"][lang])
        target = await Blacklist.get_by_id(target_id)
    elif user_id:
        target_id = user_id
        target = await Blacklist.get_by_id(user_id)
    if target:
        await message.answer(user["already_exsists"][lang], reply_markup = await main_menu(message, lang))
    else:
        await Blacklist.add(target_id, username, link)
        await message.answer(user["added"][lang], reply_markup = await main_menu(message, lang))
    await state.finish()


async def delete_from_database(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    username = await get_username(message)
    user_id = await get_user_id(message.text, True)
    
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
        await show_adds_for_user(message)


def register_users(dp: Dispatcher):
    dp.register_message_handler(verify_user, state = BotStates.VERIFY_USER)
    dp.register_message_handler(add_to_database, state = BotStates.ADD_USER)
    dp.register_message_handler(delete_from_database, state = BotStates.DELETE_USER)
    dp.register_message_handler(detect_scammer, lambda m: m.chat.type == "supergroup" or m.chat.type == "group")