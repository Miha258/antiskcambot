import asyncio
from telethon import TelegramClient, events
from telethon.tl.patched import Message
import asyncio
from utils import view_channels
from utils import get_user_id
from random import randint
import os, dotenv
from db.blacklist import Blacklist
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.patched import MessageService

dotenv.load_dotenv()
       
api_id = os.environ["API_ID"]
api_hash = os.environ["API_HASH"]
phone_number = os.environ["PHONE_NUMBER"]
main_chat = os.environ["CHAT"]

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
        user_ids = await get_user_id(user_id)
        targets = []
        if user_ids:
            for id in user_ids:
                user_id = int(id)
                target = await Blacklist.get_by_id(user_id)
                if not target:
                    targets.append(id)
        if targets:
            message = (await client.forward_messages(main_chat, messages = messages))[-1]
            for target in targets:
                await Blacklist.add(target, "", f"https://t.me/c/{message.peer_id.channel_id}/{message.id}")


async def copy_messages(client: TelegramClient):
    for chat in view_channels():
        target_messages = await client.get_messages(chat, limit = 1000)
        for message in target_messages:
            # try:
                message_text = message.message
                if isinstance(message_text, str) or isinstance(message_text, bytes):
                    user_ids = await get_user_id(message_text)
                    targets = []
                    if user_ids:
                        for id in user_ids:
                            user_id = int(id)
                            target = await Blacklist.get_by_id(user_id)
                            if not target:
                                targets.append(user_id)
                        if targets:
                            target_messages[0]
                            messages = list(filter(lambda m: m.grouped_id == message.grouped_id and not isinstance(m, MessageService), target_messages))
                            for m in messages:
                                print(m.grouped_id)
                            if messages:
                                message = (await client.forward_messages(main_chat, messages = messages))[-1]
                                for target in targets:
                                    await Blacklist.add(target, "", f"https://t.me/c/{message.peer_id.channel_id}/{message.id}")
                                await asyncio.sleep(randint(60, 180))
            # except TypeError as e:
            #     print(e)

async def main():
    async with TelegramClient('./session_file.session', api_id, api_hash) as client: 
        for chat in view_channels():
            try:
                await client(JoinChannelRequest(chat))
            except Exception as e:
                print(f'Cant join to {chat}')
        
        asyncio.get_event_loop().create_task(copy_messages(client))
        @client.on(events.Album(chats = view_channels()))
        async def event_handler(event: events.Album.Event):
            await process_message(client, event.messages)

        @client.on(events.NewMessage(chats = view_channels()))
        async def event_handler(event: events.NewMessage.Event):
            await process_message(client, [event.message])
        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())