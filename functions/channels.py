from aiogram import types, Dispatcher
from states import BotStates
from aiogram.dispatcher import FSMContext
from laguages import *
from keyborads import *
from utils import *


async def channels_list(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    
    await message.answer(channels["list"][lang](view_channels()), reply_markup = await main_menu(message, lang))
    await state.finish()

async def add_channel(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    channel = message.text 
    
    if channel in view_channels():
        await message.answer(channels["already_exist"][lang])
    else:
        update_channel(channel)
        await message.answer(channels["added"][lang], reply_markup = await main_menu(message, lang))
        await state.finish()

 

def register_channels(dp: Dispatcher):
    dp.register_message_handler(add_channel, state = BotStates.ADD_CHANNEL)