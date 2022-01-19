from aiogram import types
from aiogram.types import ChatType

import keyboards as kb
import texts
from loader import dp
from models import documents


@dp.message_handler(button=kb.Main.CONTACTS_INFO, chat_type=ChatType.PRIVATE)
async def contacts_info(msg: types.Message):
    user = documents.User.objects(id=msg.from_user.id).first() or documents.User(id=msg.from_user.id)
    await msg.answer(texts.invited_contacts_info.format(count=len(user.invited_users_ids)))
