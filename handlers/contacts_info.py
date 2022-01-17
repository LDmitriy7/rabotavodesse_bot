from aiogram import types
from aiogram.types import ChatType

import keyboards as kb
from loader import dp


@dp.message_handler(button=kb.Main.CONTACTS_INFO, chat_type=ChatType.PRIVATE)
async def contacts_info(msg: types.Message):
    await msg.answer('Приглашено:')
