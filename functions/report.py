from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from client import search_user
from keyborads import *
from states import *
from laguages import *
from utils import *
from db.blacklist import *
from main import bot
from utils import get_admins


async def ask_report_url(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    username = await get_username(message)
    user_id = await get_user_id(message.text)
    target = None
    target_id = None

    if not username and not user_id:
        await message.answer(user["invalid_data"][lang], reply_markup = back_to_menu(lang))
    else:
        if username:
            target_id = await search_user(username)
            target = await Blacklist.get_by_id(target_id)
        elif user_id:
            target_id = user_id
            target = await Blacklist.get_by_id(user_id)
        if target:
            await message.answer(user["already_exsists"][lang], reply_markup = await main_menu(message, lang))
        else:
            await state.update_data({"username": username, "user_id": target_id})
            await state.set_state(BotStates.REPORT_TEXT)
            await message.answer(reports["report_url"][lang])



async def ask_report_media(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    await state.update_data({"url": message.text})
    print(message.text)
    await state.set_state(BotStates.REPORT_MEDIA)
    await message.answer(reports["report_media"][lang], parse_mode = "html", reply_markup = skip_kb(lang))


async def handle_media(message: types.Message, state: FSMContext):
    await state.update_data({"media": message.photo or message.video})
    await send_report(message, state)


async def skip_media(message: types.Message, state: FSMContext):
    await send_report(message, state)


async def send_report(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        url = data.get('url')
        media = data.get('media')
        target_username = data.get('username')
        target_id = data.get('user_id')
        for admin in get_admins():
            lang = get_language(admin)
            report = reports["report_form"][lang](target_id, target_username, message.from_id, message.from_user.mention, url, datetime.today().strftime("%d.%m.%Y %H:%M"))
            if media:
                if isinstance(media, list):
                    await bot.send_photo(admin, media[0].file_id, caption = report, parse_mode = "html")
                elif isinstance(media, types.Video):
                    await bot.send_video(admin, media.file_id, caption = report, parse_mode = "html")
            else:
                await bot.send_message(admin, report, parse_mode = "html")
        lang = get_language(message.from_id)
        await message.answer(reports["report_sended"][lang], reply_markup = await main_menu(message, lang))
    await state.finish()


def register_report(dp: Dispatcher):
    dp.register_message_handler(ask_report_url, state = BotStates.REPORT_USER)
    dp.register_message_handler(ask_report_media, state = BotStates.REPORT_TEXT)
    dp.register_message_handler(skip_media, lambda m: m.text in skip.values(), state = BotStates.REPORT_MEDIA)
    dp.register_message_handler(handle_media, state = BotStates.REPORT_MEDIA, content_types = types.ContentTypes.PHOTO | types.ContentTypes.VIDEO) 