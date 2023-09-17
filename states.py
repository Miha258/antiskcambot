from aiogram.dispatcher.filters.state import State, StatesGroup

class BotStates(StatesGroup):
    ADD_ADMIN = State()
    ADD_CHANNEL = State()
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
    
class SendInfo(StatesGroup):
    SET_MEDIA = State()
    SET_TEXT = State()
    SET_TIME = State()
    SET_COUNT = State()