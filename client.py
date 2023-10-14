import asyncio
from telethon import TelegramClient, events
from telethon.tl.patched import Message
import asyncio
from utils import view_channels
from utils import get_user_id
from random import randint
import os, dotenv
from db.blacklist import Blacklist


dotenv.load_dotenv()
       
api_id = os.environ["API_ID"]
api_hash = os.environ["API_HASH"]
phone_number = os.environ["PHONE_NUMBER"]
main_chat = os.environ['CHAT']

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

async def process_message(client: TelegramClient, messages: list[Message]):
    message_text = messages[0].message  
    user_id = await get_user_id(message_text)
    if user_id:
        user_id = int(user_id)
        target = await Blacklist.get_by_id(user_id)
        if not target:
            
            m = (await client.forward_messages(main_chat, messages = messages))[0]
            await Blacklist.add(user_id, "", f"https://t.me/c/{m.peer_id.channel_id}/{m.id}")
            return m

async def main():
    async with TelegramClient('./session_file.session', api_id, api_hash) as client: 
        for chat in view_channels():
            for message in await client.get_messages(chat, limit=500):
                try:
                    user_id = await get_user_id(message.message)
                    if user_id:
                        user_id = int(user_id)
                        target = await Blacklist.get_by_id(user_id)
                        if not target:
                            m = (await client.forward_messages(main_chat, messages = [message]))[0]
                            await Blacklist.add(user_id, "", f"https://t.me/c/{m.peer_id.channel_id}/{m.id}")
                            await asyncio.sleep(randint(15, 30))
                except Exception as e:
                    print(e)
        @client.on(events.Album(chats = view_channels()))
        async def event_handler(event: events.Album.Event):
            await process_message(client, event.messages)

        @client.on(events.NewMessage(chats = view_channels()))
        async def event_handler(event: events.NewMessage.Event):
            await process_message(client, [event.message])
        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())