from aiogram import types, Dispatcher
from states import SendInfo
from aiogram.dispatcher import FSMContext
from laguages import *
from db.adds import Adds
from db.users import Users
from keyborads import back_to_menu
from datetime import datetime
import re
import asyncio
from main import bot
import calendar
from utils import fetch_media_bytes


async def skip_media(message: types.Message):
    lang = get_language(message.from_id) 
    await SendInfo.next()
    await message.answer(adds["send_text"][lang], reply_markup = back_to_menu(lang))


async def ask_for_text(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id) 
    media = message.photo[0] if message.photo[0] else message.video

    await state.update_data({'media': media})
    await state.set_state(SendInfo.SET_TEXT)
    await message.reply(adds["send_text"][lang], reply_markup = back_to_menu(lang))


def get_calendar(lang: str, month: int = 0):
    inline_markup = types.InlineKeyboardMarkup(row_width=7)
    date = datetime.today()

    if month < 0:
        date = date.replace(year = date.year + 1) 

    start = 1 if month else date.day
    end = calendar.monthrange(date.year, date.month + month)[1]
    for day in range(start, end + 1):
        inline_markup.insert(types.InlineKeyboardButton(str(day), callback_data = f"calendar_day:{date.year}-{date.month + month}-{day}"))

    inline_markup.row(
        types.InlineKeyboardButton(months_buttons["previous"][lang], callback_data = "prev_month"),
        types.InlineKeyboardButton(months[lang][date.month + month - 1], callback_data = "current_month"),
        types.InlineKeyboardButton(months_buttons["next"][lang], callback_data = "next_month"),
    )

    return inline_markup

  
async def set_calendar_month(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        lang = get_language(callback_query.from_user.id) 
        index = data.get("calendar") if data.get("calendar") else 0
        add = index + 1 if callback_query.data == "next_month" else index - 1
        data["calendar"] = add
        await callback_query.message.edit_reply_markup(get_calendar(lang, add))
    

async def choose_date(callback_query: types.CallbackQuery, state: FSMContext):
    date = callback_query.data.split(":")[1]
    lang = get_language(callback_query.from_user.id) 
    await state.update_data({"date": date})
    await callback_query.answer(adds["choose_date"][lang](date))


async def ask_for_time(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id) 
    await state.update_data({"text": message.text})
    await state.set_state(SendInfo.SET_TIME)
    await message.answer(adds["set_time"][lang], reply_markup = get_calendar(lang))


async def ask_for_count(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    date_time_regex = r'\d{2}:\d{2}' 
    async with state.proxy() as data:
        if not data.get("date"):
            return await message.answer(adds["set_date"][lang])
        
        date_obj = datetime.strptime(data['date'], "%Y-%m-%d")
        time_obj = datetime.strptime(message.text, "%H:%M")
        
        if re.search(date_time_regex, message.text): 
            date = datetime.combine(date_obj.date(), time_obj.time())
            await state.update_data({"time": date})
            await state.set_state(SendInfo.SET_COUNT)
            await message.answer(adds["set_count"][lang])
        else:
            await message.answer(adds["set_time_error"][lang])


async def send_adds_to_users(text: str, media: types.PhotoSize | types.Video, date: datetime.date):
    users = await Users.all()
    while datetime.now() < date: await asyncio.sleep(1)
    
    for channel in users:
        if media:
            if isinstance(media, types.PhotoSize):
                await bot.send_photo(channel, media.file_id, text)
            elif isinstance(media, types.Video):
                await bot.send_video(channel, media.file_id, text)
        else:
            await bot.send_message(channel, text)
   

async def send_message_with_delay(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    async with state.proxy() as data:
        type = data.get('type')
        text = data.get('text')
        time = data.get('time')
        media = data.get('media')
        count = int(message.text)
    
        if type == "users":
            loop = asyncio.get_event_loop()
            loop.create_task(send_adds_to_users(text, media, time))
            
        elif type == "channels":
            media_data = None
            if media:
                file = await bot.get_file(media.file_id)
                media_data = await fetch_media_bytes(await file.get_url())
            
            await Adds.add(message.message_id, text, time, count, media_data)

        await message.answer(adds["created"][lang](time), parse_mode = "html")
        await state.finish()

def register_adds(dp: Dispatcher):
    dp.register_callback_query_handler(choose_date, lambda cb: "calendar_day" in cb.data, state = SendInfo.SET_TIME)
    dp.register_callback_query_handler(set_calendar_month, lambda cb: cb.data in ["prev_month", "next_month"], state = SendInfo.SET_TIME)
    dp.register_message_handler(ask_for_count, state = SendInfo.SET_TIME)
    
    dp.register_message_handler(skip_media, lambda m: m.text in skip.values(), state = SendInfo.SET_MEDIA)
    dp.register_message_handler(ask_for_text, state = SendInfo.SET_MEDIA, content_types = types.ContentTypes.PHOTO | types.ContentTypes.VIDEO)
    dp.register_message_handler(ask_for_time, state = SendInfo.SET_TEXT)
    dp.register_message_handler(send_message_with_delay, state = SendInfo.SET_COUNT) 