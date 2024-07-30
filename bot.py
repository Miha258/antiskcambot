import logging, subprocess
from main import dp
from aiogram import executor
from aiogram import types
from aiogram.dispatcher import FSMContext
from db.blacklist import *
from functions.users import *
from functions.links import *
from functions.premium_features import *
from functions.adds import *
from functions.subscribes import *
from functions.admin import *
from functions.report import *
from functions.channels import *
from laguages import *
from keyborads import *
from utils import *
from functions.adds import *
from states import *
from filters import *
from db.blacklist import Blacklist
from db.users import Users
from db.channels import Channels
from db.adds import Adds
from client import main_chat


class SqlStatementFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        match = re.search(r"\(.+?, '(.+?)', .+?\)", message)
        if match:
            return match.group(1)
        return message

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger('aiogram')
sqlite_logger = logging.getLogger('aiosqlite')
sqlite_logger.setLevel(10)
sqlite_handler = logging.StreamHandler()
sqlite_handler.setFormatter(SqlStatementFormatter())
sqlite_logger.addHandler(sqlite_handler)


@dp.message_handler(IsDM(True), commands = ["start"])
async def start_command(message: types.Message):
    lang = get_language(message.from_id)
    if not await Users.get_by_id(message.from_id):
        await Users.add(message.from_id, message.from_user.username)
    await message.answer(greeting[lang], reply_markup = await main_menu(message, lang)) 


@dp.message_handler(IsDM(True), commands = ["chat_id"])
async def start_command(message: types.Message):
    lang = get_language(message.from_id)
    await message.answer(chat_id[lang](message.chat.id), parse_mode = "html") 



@dp.message_handler(IsDM(True), lambda m: m.text in back.values(), content_types = types.ContentTypes.TEXT, state = "*")
async def main_options(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    await message.answer(choose_option[lang], reply_markup = await main_menu(message, lang)) 
    await state.finish()


@dp.message_handler(IsDM(True), lambda m: m.text in menu[get_language(m.from_id)] + admin_menu[get_language(m.from_id)] + su_admin_menu[get_language(m.from_id)], content_types = types.ContentTypes.TEXT)
async def process_button_click(message: types.Message, state: FSMContext):
    option = message.text
    lang = get_language(message.from_id) 
    match option:
        case "🇬🇧 Изменить язык на EN":
            lang = "EN"
            set_user_language(message.from_id, lang)
            await message.answer(change_language[lang], reply_markup = await main_menu(message, lang))
        case "🇷🇺 Change language on RU":
            lang = "RU"
            set_user_language(message.from_id, lang)
            await message.answer(change_language[lang], reply_markup = await main_menu(message, lang))
        case "📈 Добавить блэклист" | "📈 Add blacklist":
            await state.set_state(BotStates.ADD_CHANNEL)
            await message.answer(channels["enter"][lang], reply_markup = back_to_menu(lang), parse_mode = "html")
        case "📉 Удалить блэклист" | "📉 Remove blacklist":
            await state.set_state(BotStates.REMOVE_CHANNEL)
            await message.answer(channels["enter_username"][lang], reply_markup = back_to_menu(lang), parse_mode = "html")
        case "📁 Список блэклистов" | "📁 Blacklists":
            await channels_list(message, state)
        case "➕ Добавить в базу" | "➕ Add to Database":
            await state.set_state(BotStates.ADD_USER)
            await message.answer(user["enter_username_with_url"][lang], reply_markup = back_to_menu(lang), parse_mode = "html")
        case "➖ Удалить из базы" | "➖ Delete from Database":
            await state.set_state(BotStates.DELETE_USER)
            await message.answer(user["enter_username"][lang], reply_markup = back_to_menu(lang))
        case "📢 Рекламное сообщение" | "📢 Send Advertisement":
            await state.set_state(SendInfo.SET_TIME)
            await message.answer(adds["set_time"][lang], reply_markup = get_calendar(lang), parse_mode = "html")
            await state.set_data({"type": "users"})
        case "🌚 Рекламное сообщение в реакциях" | "🌚 Send Advertisement in Reactions":
            await message.answer(adds["send_media"][lang], reply_markup = skip_kb(lang))
            await state.set_state(SendInfo.SET_MEDIA)
            await state.set_data({"type": "channels"})
        case "👤 Подписки юзеров" | "👤 Subscribtions on Bot":
            await subscribe_to_bot(message)
        case "👁️‍🗨️ Подписки бота в чатах" | "👁️‍🗨️ Subscribtions in Chats":
            await subscribe_to_bot_chats(message)
        case "👁️ Добавить администратора" | "👁️ Add Administrator":
            await state.set_state(BotStates.ADD_ADMIN)
            await message.answer(admin["enter_username"][lang], reply_markup = back_to_menu(lang))
        case "⛔ Удалить администратора" | "⛔ Remove Administrator":
            await state.set_state(BotStates.REMOVE_ADMIN)
            await message.answer(admin["enter_username"][lang], reply_markup = back_to_menu(lang))
        case "🔎 Проверить пользователя" | "🔎 Verify User":
            await state.set_state(BotStates.VERIFY_USER)
            await message.answer(user["enter_username"][lang], reply_markup = back_to_menu(lang))
        case "📨 Подать жалобу" | "📨 Submit Complaint":
            await state.set_state(BotStates.REPORT_USER)
            await message.answer(user["enter_username"][lang], reply_markup = back_to_menu(lang))
        case "⭐️ Премиум возможности" | "⭐️ Premium Features":
            kb = premium_options_1(lang)
            kb.add(back_to_menu(lang).keyboard[0][0])
            await message.answer(choose_option[lang], reply_markup = kb)
        case "👨‍💻 Поддержка" | "👨‍💻 Support":
            await support(message, state)
        case "💬 Наш чат" | "💬 Our Chat":
            await our_chat(message)
        case "🏴‍☠️ Наши проекты" | "🏴‍☠️ Our Projects":
            await our_projects(message)                  
        case _:
            await message.answer(choose_option[lang], reply_markup = await main_menu(message, lang))


async def on_startup(d):
    await Adds.init_table()
    await Users.init_table() 
    await Blacklist.init_table()
    await Channels.init_table()
    await AddsShown.init_table()

if __name__ == '__main__':
    register_users(dp)
    register_premium(dp)
    register_adds(dp)
    register_report(dp)
    register_channels(dp)
    register_admins(dp)
    register_links(dp)
    
    dp.register_message_handler(add_admin_handler, lambda m: m.text not in (back["RU"], back["EN"]), state = BotStates.ADD_ADMIN)
    subprocess.Popen(['python3', 'client.py'])
    executor.start_polling(dp, skip_updates = True, on_startup = on_startup)  