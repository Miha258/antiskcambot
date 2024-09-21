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

send = {
    "EN": 'Send',
    "RU": 'Отправить'
}

menu = {
  "EN": [
    "🔎 Verify User",
    "📨 Submit Complaint",
    "⭐️ Premium Features",
    "👨‍💻 Support",
    "💬 Our Chat",
    "🏴‍☠️ Our Projects",
    "🇷🇺 Change language on RU",
  ],
  "RU": [
    "🔎 Проверить пользователя",
    "📨 Подать жалобу",
    "⭐️ Премиум возможности",
    "👨‍💻 Поддержка",
    "💬 Наш чат",
    "🏴‍☠️ Наши проекты",
    "🇬🇧 Изменить язык на EN",
  ]
}

su_admin_menu = {
    "EN": [
        "👁️ Add Administrator",
        "⛔ Remove Administrator",
        "📈 Add blacklist",
        "📉 Remove blacklist",
        "📁 Blacklists",
        "📢 Send Advertisement",
        "🌚 Send Advertisement in Reactions",
    ],
    "RU": [
        "👁️ Добавить администратора",
        "⛔ Удалить администратора",
        "📁 Список блэклистов",
        "📈 Добавить блэклист",
        "📉 Удалить блэклист",
        "📢 Рекламное сообщение",
        "🌚 Рекламное сообщение в реакциях",
    ]
}

admin_menu = {
    "EN": [
        "➕ Add to Database",
        "➖ Delete from Database",
        "👤 Subscribtions on Bot",
        "👁️‍🗨️ Subscribtions in Chats",
    ],
    "RU": [
        "➕ Добавить в базу",
        "➖ Удалить из базы",
        "👤 Подписки юзеров",
        "👁️‍🗨️ Подписки бота в чатах",
    ]
}
    

user = {
    "username_not_found": {
        "EN": "Can`t find user with this username.Try again:",
        "RU": "Не могу найти юзера с таким юзернеймом.Попробуйте еще раз:"
    },
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
    "already_exsists": {
        "EN": "User already in database",
        "RU": "Человек уже есть в базе"
    },
    "not_found": {
        "EN": "User not found",
        "RU": "Человек не найден в базе"
    },
    "added": {
        "EN": "User saved in database",
        "RU": "Человек успешно сохранен в базу"
    },
    "reason": {
        "EN": "Enter reason:",
        "RU": "Введите причину:"
    },
    "deleted": {
        "EN": "User removed from database",
        "RU": "Человек был успешно удален с базы"
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
    "not_exist": {
        "EN": "This user is not admin",
        "RU": "Пользователь не является админом"
    },
    "added": {
        "EN": "Admin added successfully",
        "RU": "Админ успешно добавлен"
    },
    "removed": {
        "EN": "Admin removed successfully",
        "RU": "Админ успешно удален"
    },
    "username_not_found": {
        "EN": "Username not found.Try again:",
        "RU": "Юзернейм не найден.Попробуйте еще раз:"
    }
}


channels = {
    "enter": {
        "EN": "Enter blacklist invite link:",
        "RU": "Введите инвайт на блэклист:"
    },
    "enter_username": {
        "EN": "Enter blacklist username:",
        "RU": "Введите юзернейм блеклиста:"
    },
    "not_exist": {
        "EN": "Can`t found this blacklist in list.Try again:",
        "RU": "Не могу найти такой бэклист в списке.Поробуйте еще раз:"
    },
    "list": {
        "EN": lambda channels_list: f"Channel list: {channels_list}",
        "RU": lambda channels_list: f"Список канолов: {channels_list}"
    },
    "already_exist": {
        "EN": "Blacklist is already in list.Try again:",
        "RU": "Блэклист уже есть в списке.Поробуйте еще раз:"
    },
    "invalid_url": {
        "EN": "Invalid invite url or expired.Try again:",
        "RU": "Неверный URL приглашения или срок его действия истек. Повторите попытку:"
    },
    "already_in_chat": {
        "EN": "Can`t joint to chat because I'm already is participant",
        "RU": "Не могу присоединиться к блэклисту, потому что я уже участник"
    },
    "added": {
        "EN": "Blacklist added successfully",
        "RU": "Блэклист успешно добавлен"
    },
    "removed": {
        "EN": "Blacklist removed successfully",
        "RU": "Блэклист успешно удален"
    }
}


blacklist = {
    "EN": lambda username, id, added_in, url: f"<b>{username} has been found in scammers database!</b> \nId: {id}\nAdded in: {added_in}\nBlacklist url: {url}",
    "RU": lambda username, id, added_in, url: f"<b>{username} был найден в бд скамеров!</b>: \nАйди: {id}\nДобавлен: {added_in}\nCсылка на блек: {url}"
}


premium_options = {
    "description": {
    "EN": """
The premium features of the bot include connection to the group "cleansing from scammers" for $10 and
monthly payment in the form of $20
for "autodeletion of scammers". 
<b>Payment is accepted in BTC, ETH, USDT TRC20 and other cryptocurrencies</b>
""",
    "RU": """
В премиум возможности бота входит подключение к группе "чистки от скамеров" за 10$ и
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
        "RU": "Очистку группы от скамеров"
    },
    "choose_currency": {
        "EN": "Select system:",
        "RU": "Выберите систему:"
    },
    "enter_chat_id": {
        "EN": "Now enter your group id.\n<b>To get id use /chat_id in your group</b>",
        "RU": "Теперь введите айди вашей группы.\n<b>Чтобы получить айди, используйте /chat_id в своей группе</b>"
    },
    "chat_error": {
        "EN": "Can`t find this group.Maybe I'm not a member of this group",
        "RU": "Не могу найти группы.Возможно я не участник этого группы"
    },
    "chat_not_found": {
        "RU": "Я должен быть участником этой группы",
        "EN": "I must be particpant of this group"
    },  
    "admin_error": {
        "EN": "I must be administartor in this group",
        "RU": "Я должен быть администратором в этой группе"
    },
    "pay_link": {
        "EN": lambda url: f'Folow this <a href="{url}">link</a> to pay',
        "RU": lambda url: f'Перейдите по <a href="{url}">ссылке</a> для оплаты'
    },
    "scammer_removed": {
        "EN": lambda mention: f"<b>Scammer {mention} was removed from your chat!</b>",
        "RU": lambda mention: f"<b>Скамер {mention} был удален с вашей группы!</b>"
    },
    "total_removed": {
        "EN": lambda count: f"Total removed: <b>{count} scammers</b>",
        "RU": lambda count: f"Всеого удалено: <b>{count} скамеров</b>"
    },
    "not_found": {
        "EN": "Has not found any scammers in your chat!",
        "RU": "В вашем канале не найдено скамеров!"
    },
    "auto_delete_paynamnet": {
        "EN": lambda channel, option: f"You <b>succesfully</b> bought \"{option}\" in group: <b>{channel}</b>",
        "RU": lambda channel, option: f"Вы <b>успешно</b> купили \"{option}\" в группе: <b>{channel}</b>"
    },
    "scammer_cleaning_paynamnet": {
        "EN": lambda channel: f"You <b>succesfully</b> bought \"scammer cleaning\" in group: <b>{channel}</b>",
        "RU": lambda channel: f"Вы <b>успешно</b> купили \"чистку от скамеров\" в группе:  <b>{channel}</b>"
    },
    "auto_delete_paynamnet_bot": {
        "EN": "I'm standing guard here now 🛡",
        "RU": "Тепер я стою здесь на защите 🛡"
    },
    "scammer_cleaning_processing": {
        "EN": "<b>Checking database for scammers in your group...</b>",
        "RU": "<b>Проверка базы данных на скамеров в вашем группе...</b>"
    },
    "subscription_exist": {
        "EN": lambda to: f"You already have auto deleting subscription to: <b>{to}</b>",
        "RU": lambda to: f"У вас уже есть автоматическое удаление подписки до: <b>{to}</b>"
    },
    "subscription_ended": {
        "EN": "<b>Your premium subscription on auto deleting has been ended</b>",
        "RU": "<b>Ваша премиальная подписка на автоматическое удаление завершена</b>"
    },
    "failde_paynament": {
        "EN": "<b>There was a problem, your payment failed!</b>",
        "RU": "<b>Произошла проблема, у вас не прошел платеж!</b>",
    },
    "processing_paynament": {
        "EN": "Your payment is being processed, please try to check it later",
        "RU": "Ваш платеж обрабатывается, попробуйте проверить его чуть позже"
    }
}

check_button = {
    "EN": "Check paynament",
    "RU": "Проверить оплату"
}


pay = {
    "RU": "Оплатить",
    "EN": "Pay"
}


about_urls = {
    "support": {
        "EN": "Discribe your question:",
        "RU": "Опишите ваш вопрос:"
    },
    "support_accepted": {
        "EN": "Your question has been sent to support, please wait for a response!",
        "RU": "Ваш вопрос был передан в саппорт, ждите ответа!"
    },
    "notify_support": {
        "EN": lambda from_user, question: f"Question to support from {from_user}:\n{question}",
        "RU": lambda from_user, question: f"Вопрос в саппорт от {from_user}:\n{question}",
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
     "send_forward_message": {
        "EN": "Forward advertisement message from channel:",
        "RU": "Перешлите пост из канала:"
    },
    "send_media": {
        "EN": "Send the photo/video of advertisement",
        "RU": "Отправьте фото/видео объявление"
    },
    "send_text": {
        "EN": "Send the advertisement text",
        "RU": "Отправьте текст объявление"
    },
    "set_time": {
        "RU": "Теперь виберите время отправки объявление.Потом введите время в формате <strong>HH:MM</strong>",
        "EN": "Now enter the date to send the advertisement.After that enter time in format  <strong>HH:MM</strong>"
    },
    "set_time_error": {
        "RU": "Time format must be 00:00",
        "EN": "Формат времени должен быть 00:00"
    },
    "set_date": {
        "EN": "Enter shows count",
        "RU": "Введите количество показов"
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
    },
    "count": {
        "EN": lambda count: f"The number of successful shipments: <b>{count}</b>",
        "RU": lambda count: f"Количество успешных отправлений <b>{count}</b>",
    },
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
        "EN": lambda t_id, t_username, u_id, u_username, url, time: f"Target Username: {t_username}\nTarget ID: <b>{t_id}</b>\nAuthor ID: <b>{u_id}</b>\nAuthor Username: {u_username}\nBlackilist link <b>{url}</b>\n Adding date: <b>{time}</b>",
        "RU": lambda t_id, t_username, u_id, u_username, url, time: f"Юзернейм скамера: {t_username}\nАйди скамера: <b>{t_id}</b>\nАйди автора: <b>{u_id}</b>\nЮзернейм автора: {u_username}\nСсылка на блек: <b>{url}</b>\nДата добавления: <b>{time}</b>"
    },
    "photo_added": {
        "EN": "Photo have been added",
        "RU": "Фото добавлено"
    },
    "report_approved": {
        "EN": "Report has been approved",
        "RU": "Репорт одобрен успешно"
    },
    "report_approve_btn": {
        "EN": "Approve",
        "RU": "Одобрить"
    },
    "report_disapproved": {
        "EN": "Report has been disapproved",
        "RU": "Репорт успешно отклонен"
    },
    "report_disapprove_btn": {
        "EN": "Disapprove",
        "RU": "Отклонить"
    },
    "report_inactive": {
        "EN": "This report already have been handled",
        "RU": "Этот репорт уже был обработан"
    },
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
    },
    "back": {
        "EN": "Back to menu",
        "RU": "Назад в меню"
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