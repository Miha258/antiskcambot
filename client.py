import asyncio
from telethon import TelegramClient, events, types
import asyncio, re
from utils import view_channels
from main import bot
import os, dotenv
from aiogram import types as aitypes

dotenv.load_dotenv()
       
api_id = os.environ["API_ID"]
api_hash = os.environ["API_HASH"]
phone_number = os.environ["PHONE_NUMBER"]
chat = os.environ['CHAT']

async def login(client):
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        code = input('Enter the code you received: ')
        await client.sign_in(phone_number, code)
        await client.session.save()


async def search_user(username):
    async with TelegramClient('./session_file.session', api_id, api_hash) as client:
        await client.connect()
        await login(client)

        try:
            user = await client.get_entity(username)
            return user.id
        except Exception as e:
              print(f"Error: {e}")

async def process_message(message: types.Message):
    message_text = message.message  
    if "id" in message_text:
        id_match = re.search(r'id (\d+)', message_text)
        if id_match:
            
            if message.media:
                await bot.send_media_group("@pos21ds", [aitypes.InputMediaPhoto() for document in message.media])
            else:
                await bot.send_message("@pos21ds", message.text)


async def main():
    async with TelegramClient('./session_file.session', api_id, api_hash) as client:
        @client.on(events.NewMessage(chats = view_channels()))
        async def event_handler(event: events.NewMessage.Event):
            await process_message(event.message)
        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())


