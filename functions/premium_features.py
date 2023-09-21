from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import os
from keyborads import *
import aiohttp
from states import *
from db.channels import Channels
from db.blacklist import Blacklist
from main import bot
from datetime import datetime, timedelta
import asyncio

headers = {
    'Host': 'pay.crypt.bot',
    'Crypto-Pay-API-Token': os.environ['CRYPTO_WALLET']
}

     
async def premium_features_description(message: types.Message):
    lang = get_language(message.from_id)
    await message.answer(premium_options["description"][lang], parse_mode = "html")
 

async def premium_features_order(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    kb = premium_options_2(lang)
    kb.add(back_to_menu(lang).keyboard[0][0])
    
    await message.answer(choose_option[lang], reply_markup = kb)
    await state.set_state(BotStates.SELECT_OPTION)

    
async def premium_select_option(message: types.Message, state: FSMContext):
    lang = get_language(message.from_id)
    await state.set_data({"option": message.text})  
    
    await message.answer(premium_options["enter_chat_id"][lang], reply_markup = back_to_menu(lang), parse_mode = "html")
    await state.set_state(BotStates.CHAT_ID)


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

        price = 9.99
        if option == premium_options["auto_delete"][lang]:
            price = 19.99
            sub = (await Channels.get_by_id(chat.id)).get("subscription_to")
            if sub:
                return await message.answer(premium_options["subscription_exist"][lang](sub.split(" ")[0]), parse_mode = "html")

        async with aiohttp.ClientSession(headers = headers) as session:
            async with session.get(f'https://pay.crypt.bot/api/createInvoice?asset=USDT&amount={price}3&allow_anonymous=False') as response:
                response = await response.json()
                check = response["result"]
                url = check.get("pay_url")
                check_id = check.get('invoice_id')

                reply_markup = types.InlineKeyboardMarkup(inline_keyboard = [
                    [types.InlineKeyboardButton(check_button[lang], callback_data = f"check_invoice_{check_id}")]
                ])
                await message.answer(premium_options["pay_link"][lang](url), reply_markup = reply_markup, parse_mode = "html")
        await state.set_state(BotStates.PAYNAMENT)


async def check_invoice(callback_query: types.CallbackQuery, state: FSMContext):
    lang = get_language(callback_query.from_user.id)
    check_id = callback_query.data.split('_')[-1]
    async with aiohttp.ClientSession(headers = headers) as session:
        async with session.get(f'https://pay.crypt.bot/api/getInvoices?invoice_id={check_id}') as response:
            data = await state.get_data()
            option = data.get("option")
            
            channel_id = data.get("id")
            chat = await bot.get_chat(channel_id)
            response = await response.json()
            paynament = response['result']['items'][0]
            if paynament['status'] == 'paid':
                if option in premium_options["auto_delete"].values():
                    await callback_query.message.answer(premium_options["auto_delete_paynamnet"][lang](chat.title), parse_mode = "html")
                    if not await Channels.get_by_id(channel_id):
                        await Channels.add(channel_id, callback_query.message.from_id, datetime.now() + timedelta(minutes = 1))
                    else:
                        await Channels.set_sub(channel_id, datetime.now() + timedelta(days = 31))
                
                elif option in premium_options["scammer_cleaning"].values():
                    await callback_query.message.answer(premium_options["scammer_cleaning_paynamnet"][lang](chat.title), parse_mode = "html")
                    blacklist = await Blacklist.all()
                    counter = 0
                    for user in blacklist:
                        await asyncio.sleep(1) 
                        try:
                            member = await bot.get_chat_member(channel_id, user.get("id"))
                            if member.is_chat_member():
                                await bot.ban_chat_member(channel_id, user.get("id"))
                                await callback_query.message.answer(premium_options["scammer_removed"][lang](member.user.mention), parse_mode = "html")
                                counter += 1
                        except:
                            pass
                    await callback_query.message.answer(premium_options["total_removed"][lang](counter), parse_mode = "html")
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
                        await bot.ban_chat_member(message.chat.id, member.id)
                        await message.answer(premium_options["scammer_removed"][lang](member.user.mention), parse_mode = "html")
            else:
                await Channels.set_sub(message.chat.id, None)
                await message.answer(premium_options["subscription_ended"][lang](member.user.mention), parse_mode = "html")


def register_premium(dp: Dispatcher):   
    dp.register_message_handler(on_member_chat_join, content_types = types.ContentTypes.NEW_CHAT_MEMBERS) 
    dp.register_message_handler(premium_features_description, lambda m: m.text in premium_options["description_btn"].values())
    dp.register_message_handler(premium_features_order, lambda m: m.text in premium_options["order"].values())
    dp.register_message_handler(premium_select_option, state = BotStates.SELECT_OPTION)
    dp.register_message_handler(premium_set_channel, state = BotStates.CHAT_ID)
    dp.register_callback_query_handler(check_invoice, state = BotStates.PAYNAMENT)           