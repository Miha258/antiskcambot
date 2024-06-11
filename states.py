from aiogram.dispatcher.filters.state import State, StatesGroup

class BotStates(StatesGroup):
    ADD_ADMIN = State()
    REMOVE_ADMIN = State()
    ADD_CHANNEL = State()
    REMOVE_CHANNEL = State()
    VERIFY_USER = State()
    ADD_USER = State()
    SET_REASON = State()
    DELETE_USER = State()
    SELECT_OPTION = State()
    CHAT_ID = State()
    PAYNAMENT = State()
    REPORT_USER = State()
    REPORT_TEXT = State()
    REPORT_MEDIA = State()
    SEND_REPORT = State()
    SELECT_CURRENCY = State()
    
class SendInfo(StatesGroup):
    SET_FORWARD_MESSAGE = State()
    SET_MEDIA = State()
    SET_TEXT = State()
    SET_TIME = State()
    SET_COUNT = State()