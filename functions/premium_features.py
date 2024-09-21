from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyborads import *
import aiohttp
from states import *
from db.channels import Channels
from db.blacklist import Blacklist
from main import bot
from datetime import datetime, timedelta
import asyncio
import os

headers = {'Content-Type': 'application/json'}

     
async def premium_features_description(message: types.Message):
    lang = get_language(message.from_id)
    await message.answer(premium_options["description"][lang], parse_mode = "html")
 

async def premium_features_order(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    kb = premium_options_2(lang)
    kb.add(back_to_menu(lang).keyboard[0][0])
    
    await message.answer(choose_option[lang], reply_markup = kb)
    await state.set_state(BotStates.SELECT_OPTION)


SUPPORTED_METHODS = ('BITCOIN', 'BITCOINCASH', 'LITECOIN', 'ETHEREUM', 'DASH', "TEST")
async def premium_select_option(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    await state.set_data({"option": message.text}) 
    kb = types.InlineKeyboardMarkup()

    async with aiohttp.ClientSession(headers = headers) as session:
        body = {
            "auth_login": os.environ.get('AUTH_LOGIN'),
            "auth_secret": os.environ.get('AUTH_SECRET'),
        }
        async with session.post(f'https://api.crystalpay.io/v2/method/list/', json = body) as response:
            
            tickets = await response.json()
            for method, ticket in list(zip(tickets["methods"].keys(), tickets["methods"].values())):
                if method in SUPPORTED_METHODS:
                    kb.add(types.InlineKeyboardButton(ticket["name"], callback_data = f"set_currency_{method}"))

            await message.answer(premium_options["choose_currency"][lang], reply_markup = kb, parse_mode = "html")
            await state.set_state(BotStates.SELECT_CURRENCY)

async def premium_select_currency(callback_data: types.CallbackQuery, state: FSMContext):
    lang = get_language(callback_data.from_user.id)
    currency = callback_data.data.split("_")[-1]
    await state.update_data({"currency": currency})  
    
    await callback_data.message.answer(premium_options["enter_chat_id"][lang], reply_markup = back_to_menu(lang), parse_mode = "html")
    await state.set_state(BotStates.CHAT_ID)


async def make_invoice(message: types.Message, state: FSMContext, price: int, currency: str, lang: str):
    async with aiohttp.ClientSession() as session:
        print(currency)
        body = {
            "auth_login": os.environ.get('AUTH_LOGIN'),
            "auth_secret": os.environ.get('AUTH_SECRET'),
            "amount": price,
            "amount_currency": "USD",
            "required_method": currency,
            "type": "purchase",
            "description": f"Покупка #{message.from_user.mention}",
            "lifetime": 600
        }
        async with session.post(f'https://api.crystalpay.io/v2/invoice/create/', json = body, headers = headers) as response:
            response = await response.json()
            
            url = response.get("url")
            check_id = response.get("id")
            reply_markup = types.InlineKeyboardMarkup(inline_keyboard = [
                [types.InlineKeyboardButton(pay[lang], url = url)],
                [types.InlineKeyboardButton(check_button[lang], callback_data = f"check_invoice_{check_id}")],
            ])
            await message.answer(premium_options["pay_link"][lang](url), reply_markup = reply_markup, parse_mode = "html")
    await state.set_state(BotStates.PAYNAMENT)


async def premium_set_channel(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    try:
        chat = await bot.get_chat(message.text)
    except:
        await message.answer(premium_options["chat_error"][lang])
    else:
        await state.update_data({"id": chat.id})
        data = await state.get_data()  
        option = data.get("option")
        currency = data.get("currency")

        price = 9.99
        if option == premium_options["auto_delete"][lang]:
            price = 19.99
            channel = await Channels.get_by_id(chat.id)
            if not channel:
                return await make_invoice(message, state, price, currency, lang)
            sub = (await Channels.get_by_id(chat.id)).get("subscription_to")
            if sub:
                return await message.answer(premium_options["subscription_exist"][lang](sub.split(" ")[0]), parse_mode = "html")
        await make_invoice(message, state, price, currency, lang)

async def check_invoice(callback_query: types.CallbackQuery, state: FSMContext):
    lang = get_language(callback_query.from_user.id)
    check_id = callback_query.data.split('_', 2)[-1]
    async with aiohttp.ClientSession(headers = headers) as session:
        body = {
            "auth_login": os.environ.get('AUTH_LOGIN'),
            "auth_secret": os.environ.get('AUTH_SECRET'),
            "id": check_id
        }
        async with session.post(f'https://api.crystalpay.io/v2/invoice/info/', json = body) as response:
            data = await state.get_data()
            option = data.get("option")
            
            channel_id = data.get("id")
            chat = await bot.get_chat(channel_id)
            paynament = await response.json()
            if paynament['state'] != 'paid':
                if option in premium_options["auto_delete"].values():
                    await callback_query.message.answer(premium_options["auto_delete_paynamnet"][lang](chat.title, option), parse_mode = "html")
                    if not await Channels.get_by_id(channel_id):
                        await Channels.add(channel_id, callback_query.message.from_id, datetime.now() + timedelta(days = 31))
                    else:
                        await Channels.set_sub(channel_id, datetime.now() + timedelta(days = 31))
                
                elif option in premium_options["scammer_cleaning"].values():
                    await callback_query.message.answer(premium_options["scammer_cleaning_paynamnet"][lang](chat.title), parse_mode = "html")
                    blacklist = await Blacklist.all()
                    counter = 0
                    await callback_query.message.answer(premium_options["scammer_cleaning_processing"][lang], parse_mode = "html")
                    for user in blacklist:
                        await asyncio.sleep(0.1) 
                        try:
                            member = await bot.get_chat_member(channel_id, user["id"])
                            if member.is_chat_member():
                                await bot.ban_chat_member(channel_id, user["id"])
                                await callback_query.message.answer(premium_options["scammer_removed"][lang](member.user.mention), parse_mode = "html")
                                await bot.send_message(channel_id, premium_options["scammer_removed"][lang](member.user.mention), parse_mode = "html")
                                counter += 1
                        except Exception as e:
                            print(e)
                    await callback_query.message.answer(premium_options["total_removed"][lang](counter), parse_mode = "html")
                    await bot.send_message(channel_id, premium_options["total_removed"][lang](counter), parse_mode = "html")
            elif paynament['state'] == 'processing':
                await callback_query.message.answer(premium_options["processing_paynament"][lang])
            elif paynament['state'] == 'failed':
                await callback_query.message.answer(premium_options["failde_paynament"][lang])

            await callback_query.message.delete()

async def on_member_chat_join(message: types.Message):
    channel = await Channels.get_by_id(message.chat.id)
    if channel:
        if channel.get("subscription_to"):
            if datetime.now() < datetime.strptime(channel["subscription_to"], "%Y-%m-%d %H:%M:%S.%f"):
                lang = get_language(message.from_id)
                new_members = message.new_chat_members
                for member in new_members:
                    user = await Blacklist.get_by_id(member.id)
                    if user:
                        await bot.ban_chat_member(message.chat.id, member.id, timedelta(days=31))
                        await message.answer(premium_options["scammer_removed"][lang](member.mention), parse_mode = "html")
                        await bot.send_message(channel["user_id"], premium_options["scammer_removed"][lang](member.mention), parse_mode = "html")
            else:
                await Channels.set_sub(message.chat.id, None)
                await message.answer(premium_options["subscription_ended"][lang], parse_mode = "html")


def register_premium(dp: Dispatcher):       
    dp.register_message_handler(on_member_chat_join, content_types = types.ContentTypes.NEW_CHAT_MEMBERS) 
    dp.register_message_handler(premium_features_description, lambda m: m.text in premium_options["description_btn"].values())
    dp.register_message_handler(premium_features_order, lambda m: m.text in premium_options["order"].values())
    dp.register_message_handler(premium_select_option, state = BotStates.SELECT_OPTION)
    dp.register_callback_query_handler(premium_select_currency, lambda cb: "set_currency" in cb.data, state = BotStates.SELECT_CURRENCY)
    dp.register_message_handler(premium_set_channel, state = BotStates.CHAT_ID)
    dp.register_callback_query_handler(check_invoice, state = BotStates.PAYNAMENT)