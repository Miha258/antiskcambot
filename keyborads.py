from laguages import *
from aiogram import types
from utils import get_admins, get_su_admins


async def main_menu(message: types.Message, lang: str):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
    is_admin = str(message.from_id) in get_admins()
    menu_buttons = menu[lang] + admin_menu[lang] if is_admin else menu[lang]
    is_su_admin = str(message.from_id) in get_su_admins()
    if is_su_admin:
        menu_buttons = su_admin_menu[lang] + admin_menu[lang] + menu[lang]
    
    keyboard.add(*menu_buttons)
    return keyboard
  
def back_to_menu(lang: str):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(back[lang]))
    return keyboard

def skip_kb(lang: str):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(skip[lang]), types.KeyboardButton(back[lang]))
    return keyboard

def send_kb(lang: str):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(send[lang]))
    return keyboard

def premium_options_1(lang: str):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(premium_options["description_btn"][lang]), types.KeyboardButton(premium_options["order"][lang]))
    return keyboard

def premium_options_2(lang: str):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(premium_options["auto_delete"][lang]), types.KeyboardButton(premium_options["scammer_cleaning"][lang]))
    return keyboard