from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from client import search_user
from keyborads import *
from states import *
from laguages import *
from utils import *
from db.blacklist import *
from main import bot
from client import main_chat 
from utils import get_admins


async def ask_report_url(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    username = await get_username(message)
    user_id = await get_user_id(message.text, True)
    target = None
    target_id = None

    if not username and not user_id:
        await message.answer(user["invalid_data"][lang], reply_markup = back_to_menu(lang))
    else:
        if username:
            target_id = await search_user(username)
            if not target_id:
                return await message.answer(user["username_not_found"][lang])
            target = await Blacklist.get_by_id(target_id)
        elif user_id:
            target_id = user_id
            target = await Blacklist.get_by_id(user_id)
        if target:
            await message.answer(user["already_exsists"][lang], reply_markup = await main_menu(message.from_id, lang))
        else:
            await state.update_data({"username": username, "user_id": target_id})
            await message.answer(reports["report_url"][lang])
            await state.set_state(BotStates.REPORT_TEXT)


async def ask_report_media(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    await state.update_data({"url": message.text})
    await state.set_state(BotStates.REPORT_MEDIA)
    await message.answer(reports["report_media"][lang], parse_mode = "html", reply_markup = skip_kb(lang))

media = []
async def handle_media(message: types.Message):
    global media
    if media:
        media.append(message.photo[0] if message.photo else None or message.video)
    else:
        media = [message.photo[0] if message.photo else None or message.video]
    lang = get_language(message.from_id)
    await message.answer(reports["photo_added"][lang] + f": <strong>{len(media)}</strong>", parse_mode = "html", reply_markup = send_kb(lang))
async def skip_media(message: types.Message, state: FSMContext):
    await send_report(message, state)

reports_list = {}
async def send_report(message: types.Message, state: FSMContext):
    global media
    async with state.proxy() as data:
        url = data.get('url')
        target_username = data.get('username')
        target_id = data.get('user_id')
        
        lang = get_language(message.from_id)
        report_kb = types.InlineKeyboardMarkup(inline_keyboard = [
            [types.InlineKeyboardButton(reports["report_approve_btn"][lang], callback_data = f'approve_report_{target_id}')],
            [types.InlineKeyboardButton(reports["report_disapprove_btn"][lang], callback_data =  f'disapprove_report_{target_id}')]
        ])
        for admin in get_admins():
            lang = get_language(admin)
            report = reports["report_form"][lang](target_id, target_username, message.from_id, message.from_user.mention, url, datetime.today().strftime("%d.%m.%Y %H:%M"))
            if media:
                if len(media) == 1:
                    media_data = media[0]
                    if isinstance(media_data, types.PhotoSize):
                        report_msg = await bot.send_photo(admin, media_data.file_id, caption = report, parse_mode = "html", reply_markup = report_kb)
                    elif isinstance(media_data, types.Video):
                        report_msg = await bot.send_video(admin, media_data.file_id, caption = report, parse_mode = "html", reply_markup = report_kb)
                    reports_list[target_id] = report_msg
                if len(media) > 1:
                    media_group = types.MediaGroup()
                    for content in media:
                        if isinstance(content, types.PhotoSize):
                            media_group.attach_photo(content.file_id)
                        elif isinstance(content, types.Video):
                            media_group.attach_video(content.file_id)
                    await bot.send_media_group(admin, media_group)
                    await bot.send_message(admin, report, reply_markup = report_kb, parse_mode = "html")
                    reports_list[target_id] = [report, media_group]
            else:
                report_msg = await bot.send_message(admin, report, parse_mode = "html", reply_markup = report_kb)
                reports_list[target_id] = report_msg
        
        lang = get_language(message.from_id)
        await message.answer(reports["report_sended"][lang], reply_markup = await main_menu(message.from_id, lang))
    await state.finish()


async def approve_report(callback_data: types.CallbackQuery):
    lang = get_language(callback_data.from_user.id)
    report_id = int(callback_data.data.split('_')[-1])
    

    if report_id in reports_list.keys():
        message: types.Message | list[types.Message] = reports_list[report_id]
        if isinstance(message, types.Message):
            report_link = await message.forward(main_chat)
            await callback_data.message.answer(reports["report_approved"][lang])
        elif isinstance(message, list):
            report_text: str = message[0]
            media_group: types.MediaGroup = message[1]
            media_group.media[0].parse_mode = "html"
            media_group.media[0].caption = report_text
            report_link = await bot.send_media_group(main_chat, media_group)
            report_link = report_link[0]
        await Blacklist.add(report_id, None, report_link.url)
    else:
        await callback_data.message.answer(reports["report_inactive"][lang])
    await callback_data.message.delete_reply_markup()


async def disapprove_report(callback_data: types.CallbackQuery):
    lang = get_language(callback_data.from_user.id)
    report_id = int(callback_data.data.split('_')[-1])

    if report_id in reports_list.keys():
        del reports_list[report_id]
        await callback_data.message.answer(reports["report_disapproved"][lang])
    else:
        await callback_data.message.answer(reports["report_inactive"][lang])
    await callback_data.message.delete_reply_markup()


def register_report(dp: Dispatcher):
    dp.register_message_handler(ask_report_url, state = BotStates.REPORT_USER)
    dp.register_message_handler(ask_report_media, state = BotStates.REPORT_TEXT)
    dp.register_message_handler(send_report, lambda m: m.text in send.values(), state = BotStates.REPORT_MEDIA)
    dp.register_message_handler(skip_media, lambda m: m.text in skip.values(), state = BotStates.REPORT_MEDIA)
    dp.register_message_handler(handle_media, state = BotStates.REPORT_MEDIA, content_types = types.ContentTypes.PHOTO | types.ContentTypes.VIDEO) 
    dp.register_callback_query_handler(approve_report, lambda cb: "approve_report" in cb.data)
    dp.register_callback_query_handler(disapprove_report, lambda cb: "disapprove_report" in cb.data)