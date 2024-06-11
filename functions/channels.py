from aiogram import types, Dispatcher
from states import BotStates
from aiogram.dispatcher import FSMContext
from laguages import *
from client import join_to_chat, leave_from_chat
from keyborads import *
from utils import *
from filters import IsSuperAdminFilter
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError, InviteHashExpiredError


async def channels_list(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    
    await message.answer(channels["list"][lang]("\n\n" + "".join(view_channels())), reply_markup = await main_menu(message, lang))
    await state.finish()


async def add_channel(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    channel = message.text 
    try:
        channel = await join_to_chat(message.text)
        if channel in view_channels():
            return await message.answer(channels["already_exist"][lang])
        update_channel(channel)
        await message.answer(channels["added"][lang], reply_markup = await main_menu(message, lang))
    except (InviteHashExpiredError, ValueError):
        await message.answer(channels["invalid_url"][lang])
    except UserAlreadyParticipantError:
        await message.answer(channels["already_in_chat"][lang])
    await state.finish()


async def remove_channel(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    channel = message.text 
    if channel not in view_channels():
        await message.answer(channels["not_exist"][lang])
    else:
        try:
            await leave_from_chat(channel)
            delete_channel(channel)
            await message.answer(channels["removed"][lang], reply_markup = await main_menu(message, lang))
        except Exception as e:
            print(e)
        await state.finish()


def register_channels(dp: Dispatcher):
    dp.register_message_handler(add_channel, IsSuperAdminFilter(), state = BotStates.ADD_CHANNEL)
    dp.register_message_handler(remove_channel, IsSuperAdminFilter(), state = BotStates.REMOVE_CHANNEL)