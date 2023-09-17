from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os, dotenv

dotenv.load_dotenv()
bot = Bot(token = os.environ["TOKEN"])
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)

