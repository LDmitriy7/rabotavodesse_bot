import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from motor import motor_asyncio

import config

client = motor_asyncio.AsyncIOMotorClient()
db = client.rabota_v_od

bot = Bot(config.Bot.token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)
lh = logging.StreamHandler()
lh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
for h in logger.handlers:
    logger.removeHandler(h)
logger.addHandler(lh)

lock = asyncio.Lock()
