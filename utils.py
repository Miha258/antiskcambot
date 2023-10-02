import json
from aiogram import types
import aiohttp
import re

def add_admin(id: str):
    with open("config.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    
    data["admins"].append(id)

    with open("config.json", "w", encoding = "utf-8") as file:
        json.dump(data, file, ensure_ascii = False, indent = 2)


def get_admins():
    with open("config.json", "r", encoding = "utf-8") as file:
        data = json.load(file)
    
    return data["admins"]


async def get_username(message: types.Message):
    mentions = [entity.get_text(message.text) for entity in message.entities if entity.type == types.MessageEntityType.MENTION]
    if mentions:
        return mentions[0]
    

async def get_user_id(message: str):
    pattern = r'\b\d{9,}\b'
    user_ids = re.findall(pattern, message)
    
    if user_ids:
        return user_ids[0]


async def fetch_media_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            image_bytes = await response.read()
            return image_bytes  
        

channels_file = "channels.txt"

def update_channel(channel):
    with open(channels_file, 'a') as file:
        file.write(channel + "\n")


def remove_channel(channel):
    with open(channels_file, 'r') as file:
        lines = file.readlines()
    with open(channels_file, 'w') as file:
        for line in lines:
            if line.strip() != channel:
                file.write(line)

def view_channels():
    with open(channels_file, 'r') as file:
        channels = file.readlines()
    return [f'{channel}\n' for channel in channels]