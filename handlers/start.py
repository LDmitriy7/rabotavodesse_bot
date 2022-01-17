from aiogram import types
from aiogram.types import ChatType

import commands
import keyboards as kb
import texts
from loader import dp


@dp.message_handler(commands=commands.START, chat_type=ChatType.PRIVATE)
async def welcome(msg: types.Message):
    await msg.answer(texts.welcome, reply_markup=kb.Main())
