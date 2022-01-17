from aiogram import types
from aiogram.types import ChatType

import keyboards as kb
import texts
from loader import dp


@dp.message_handler(button=kb.Main.TECH_SUPPORT, chat_type=ChatType.PRIVATE)
async def tech_support_info(msg: types.Message):
    await msg.answer(texts.tech_support_info)
