import json

def get_language(id: int):
    with open("config.json", "r", encoding = "utf-8") as file:
        language_data = json.load(file)

    lang = language_data.get(str(id))

    if lang:
        return lang
    else:
        set_user_language(id, "RU")
        return "RU"

def set_user_language(id: str, language: str):
    with open("config.json", "r", encoding = "utf-8") as file:
        language_data = json.load(file)
    
    language_data[id] = language

    with open("config.json", "w", encoding="utf-8") as file:
        json.dump(language_data, file, ensure_ascii = True, indent = 2)


greeting = {
    "EN": """
🤖 Hello! I'm here to combat people who deceive and engage in scams 🛡️
My mission is to protect you from scammers and prevent fraud in the chat 🛡️

😃 Welcome, users! I'm delighted to be on your defense! If you come across any deception or scams in the chat, just let me know, and I'll take action 🛡️

🚫 Together, we'll make your chat safe and secure! We won't let scammers harm you or other users! 🚫
""",
    "RU": """
🤖 Привет! Я здесь, чтобы бороться с людьми, которые обманывают и занимаются скамом 🛡️
Моя миссия - защитить вас от мошенников и предотвратить мошенничество в чате 🛡️

😃 Добро пожаловать, пользователи! Рад быть на вашей защите! Если вы столкнетесь с обманом или скамом в чате, просто сообщите мне, и я предприму меры 🛡️

🚫 Вместе мы сделаем ваш чат безопасным и защищенным! Не дадим шансов мошенникам причинить вам или другим пользователям вред! 🚫"""
}

chat_id = {
    "EN": lambda id: f"Айди чата: {id}",
    "RU": lambda id: f"Chat id: {id}"
}
    
choose_option = {
    "EN": "Choose option:",
    "RU": "Виберете опцию:"
}

back = {
    "EN": "← Back",
    "RU": "← Назад"
}

skip = {
    "EN": "Skip",
    "RU": "Попустить"
}


menu = {
  "EN": [
    "Change language on RU",
    "Verify User",
    "Submit Complaint",
    "Premium Features",
    "Support",
    "Our Chat",
    "Our Projects",
  ],
  "RU": [
    "Изменить язык на EN",
    "Проверить пользователя",
    "Подать жалобу",
    "Премиум возможности",
    "Поддержка",
    "Наш чат",
    "Наши проекты",
  ]
}


admin_menu = {
    "EN": [
        "Add to Database",
        "Channel list"
        "Delete from Database",
        "Subscribtions on Bot",
        "Subscribtions in Chats",
        "Send Advertisement",
        "Add Administrator",
        "Add Channel",
        "Channel list",
        "Send Advertisement in Reactions",
    ],
    "RU": [
        "Добавить в базу",
        "Добавить канал",
        "Удалить из базы",
        "Подписки юзеров",
        "Подписки бота в чатах",
        "Рекламное сообщение",
        "Добавить администратора",
        "Добавить канал",
        "Список каналов",
        "Рекламное сообщение в реакциях",
    ]
}
    

user = {
    "enter_username": {
        "EN": "Enter target @username or id:",
        "RU": "Введите @username или id человека:"
    },
    "enter_username_with_url": {
        "EN": "Enter mesage in format: <b>(target @username or id) - 'link to blacklist'</b>:",
        "RU": "Введите cообщения в формате: <b>(@username или id человека) - 'ссылка на блек'</b>:"
    },
    "invalid_data": {
        "EN": "Invalid username or id.Try again:",
        "RU": "Неправильный username или id"
    },
    "already_exsists":{
        "EN": "User already in database",
        "RU": "Человек уже есть в базе"
    },
    "not_found":{
        "EN": "User not found",
        "RU": "Человек не найден в базе"
    },
    "added": {
        "EN": "User saved in database",
        "RU": "Человек успешно сохранен в бд"
    },
    "reason": {
        "EN": "Enter reason:",
        "RU": "Введите причину:"
    },
    "deleted": {
        "EN": "User removed from database",
        "RU": "Человек был успешно удален с бд"
    },    
    "invalid_link": {
        "EN": "Invalid blacklist url.Try again:",
        "RU": "Неверная ссылка на сообщение.Попробуйте еще раз:"
    },
}


admin = {
    "enter_username": {
        "EN": "Enter admin @username:",
        "RU": "Введите @username админа:"
    },
    "already_exist": {
        "EN": "Admin is already in list.Try again:",
        "RU": "Админ уже есть в списке.Поробуйте еще раз:"
    },
    "added": {
        "EN": "Admin added successfully",
        "RU": "Админ успешно добавлен"
    }
}


channels = {
    "enter": {
        "EN": "Enter channel <b>@name</b>",
        "RU": "Введите <b>@названиe</b> канала"
    },
    "list": {
        "EN": lambda channels_list: f"Channel list: {channels_list}",
        "RU": lambda channels_list: f"Список канолов: {channels_list}"
    },
    "already_exist": {
        "EN": "Channel is already in list.Try again:",
        "RU": "Канал уже есть в списке.Поробуйте еще раз:"
    },
    "added": {
        "EN": "Channel added successfully",
        "RU": "Канал успешно добавлен"
    }
}


blacklist = {
    "EN": lambda username, id, added_in, url: f"<b>{username} has been found in scammers database!</b> \nId: {id}\nAdded in: {added_in}\nBlacklist url: {url}",
    "RU": lambda username, id, added_in, url: f"<b>{username} был найден в бд скамеров!</b>: \nАйди: {id}\nДобавлен: {added_in}\nCсылка на блек: {url}"
}


premium_options = {
    "description": {
    "EN": """
The premium features of the bot include connection to the chat "cleansing from scammers" for $10 and
monthly payment in the form of $20
for "autodeletion of scammers". 
<b>Payment is accepted in BTC, ETH, USDT TRC20 and other cryptocurrencies</b>
""",
    "RU": """
В премиум возможности бота входит подключение к чату "чистки от скамеров" за 10$ и
ежемесячная оплата в виде 20$
за "автоудаление скамеров".
<b>Оплата приимается в BTC, ETH, USDT TRC20 и прочих криптовалютах.</b>
"""},
    "description_btn": {
        "EN": "Description",
        "RU": "Описание"
    },
    "order": {
        "EN": "Order",
        "RU": "Заказать"
    },
    "auto_delete": {
        "EN": "Auto delete scammers",
        "RU": "Автоудаление скамеров"
    },
    "scammer_cleaning": {
        "EN": "Clean scammers",
        "RU": "Очистку чата от скамеров"
    },
    "enter_chat_id": {
        "EN": "Now enter your channel id\n<b>To get your chat id use /chat_id in your channel</b>",
        "RU": "Теперь введите айди вашего чата.<b>Чтобы получить айди чата, используйте /chat_id на своем канале</b>"
    },
    "chat_error": {
        "EN": "Can`t find this chat.Maybe I'm not a member of this chat",
        "RU": "Не могу найти чат.Возможно я не участник этого чата"
    },
    "chat_not_found": {
        "RU": "Я должен быть участником этого канала",
        "EN": "I must be particpant of this channel"
    },  
    "admin_error": {
        "EN": "I must be administartor in this channel",
        "RU": "Я должен быть администратором в этом канале"
    },
    "pay_link": {
        "EN": lambda url: f'Folow this <a href="{url}">link</a> to pay',
        "RU": lambda url: f'Перейдите по <a href="{url}">ссылке</a> для оплаты'
    },
    "scammer_removed": {
        "EN": lambda mention: f"<b>Scammer {mention} was removed from your channel!</b>",
        "RU": lambda mention: f"<b>Скамер {mention} был удален с вашеого канала!</b>"
    },
    "total_removed": {
        "EN": lambda count: f"Total removed: <b>{count} scammers</b>",
        "RU": lambda count: f"Всеого удалено: <b>{count} скамеров</b>"
    },
    "auto_delete_paynamnet": {
        "EN": lambda channel: f"You <b>succesfully</b> bought \"auto deleting scammers\" in channel: <b>{channel}</b>",
        "RU": lambda channel: f"Вы <b>успешно</b> купили \"чистку от скамеров\" в канале: <b>{channel}</b>"
    },
    "scammer_cleaning_paynamnet": {
        "EN": lambda channel: f"You <b>succesfully</b> bought \"scammer cleaning\" in channel: <b>{channel}</b>",
        "RU": lambda channel: f"Вы <b>успешно</b> купили \"чистку от скамеров\" в канале:  <b>{channel}</b>"
    },
    "subscription_exist": {
        "EN": lambda to: f"You already have auto deleting subscription to: <b>{to}</b>",
        "RU": lambda to: f"У вас уже есть автоматическое удаление подписки до: <b>{to}</b>"
    },
    "subscription_ended": {
        "EN": "<b>Your premium subscription on auto deleting has been ended</b>",
        "RU": "<b>Ваша премиальная подписка на автоматическое удаление завершена</b>"
    }
}

check_button = {
    "EN": "Check paynament",
    "RU": "Проверить оплату"
}


about_urls = {
    "support": {
        "EN": "Our support",
        "RU": "Наша поддержка"
    },
    "chat": {
        "EN": "Our chat",
        "RU": "Наш чат"
    },
    "projects": {
        "EN": "Our projects",
        "RU": "Наши проекты"
    },
    "folow": {
        "EN": "Folow",
        "RU": "Перйти"
    },
}

adds = {
    "send_media": {
        "EN": "Send the photo/video of advertisement",
        "RU": "Отправьте фото/видео объявление"
    },
    "send_text": {
        "EN": "Send the advertisement text",
        "RU": "Отправьте текст объявление"
    },
    "set_time": {
        "RU": "Теперь введите время отправки объявление в формате «2023.06.03 22:23» (например, 14:30).",
        "EN": "Now enter the time to send the advertisement in the format '2023.06.03 22:23' (eg 14:30)."
    },
    "set_time_error": {
        "RU": "Time format must be 00:00",
        "EN": "Формат времени должен быть 00:00"
    },
    "set_date": {
        "RU": "Enter shows count",
        "EN": "Введите количество показов"
    },
    "set_count": {
        "EN": "Enter shows count",
        "RU": "Введите количество показов"
    },
    "choose_date": {
        "EN": lambda date: f"You chose date: {date}",
        "RU": lambda date: f"Вы выбрали дату: {date}"
    },
    "created": {
        "EN": lambda date: f"Advertiment will be published at <b>{date}</b>",
        "RU": lambda date: f"Объявление будет опубликовано <b>{date}</b>",
    }
} 

reports = {
    "report_url": {
        "EN": "Enter report reason:",
        "RU": "Введите причину репорта:"
    },
    "report_media": {
        "EN": "Send photo/video proofs (optional):",
        "RU": "Скиньте фото/видео доказательства (если есть):"
    },
    "report_sended": {
        "EN": "Your report has been sended. Wait for approve",
        "RU": "Ваш репорт отправлен. Дождитесь одобрения"
    },
    "report_form": {
        "EN": lambda t_id, t_username, u_id, u_username, url, time: f"{f'Target Username: {t_username}' if t_username else f'Target ID: <b>{t_id}</b>'}\nAuthor ID: <b>{u_id}</b>\nAuthor Username: {u_username}\nBlackilist link <b>{url}</b>\n Adding date: <b>{time}</b>",
        "RU": lambda t_id, t_username, u_id, u_username, url, time: f"{f'Юзернейм скамера: {t_username}' if t_username else f'Айди скамера: <b>{t_id}</b>'}\nАйди автора: <b>{u_id}</b>\nЮзернейм автора: {u_username}\nСсылка на блек: <b>{url}</b>\nДата добавления: <b>{time}</b>"
    }
}

months = {
    "EN": ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    "RU": ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
} 

months_buttons = {
    "previous": {
        "EN": "Previous month",
        "RU": "Предыдущий месяц"
    },
    "next": {
        "EN": "Next month",
        "RU": "Следующий месяц"
    }
}

subscribes = {
    "channels": {
        "EN": lambda amount: f"Subscribtions count: <b>{amount}</b>",
        "RU": lambda amount: f"Количество подписок: <b>{amount}</b>"
    },
    "users": {
        "EN": lambda amount: f"Users count: <b>{amount}</b>",
        "RU": lambda amount: f"Количество юзеров: <b>{amount}</b>"
    }
}

change_language = {
    "EN": "Language changed!",
    "RU": "Язык изменен!"
}