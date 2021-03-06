from aiogram import types
from aiogram.types import ChatType
from aiogram_utils.content_types import UserMessageContentTypes

import config
from loader import dp
from models import documents


@dp.message_handler(content_types=UserMessageContentTypes, chat_type=ChatType.PRIVATE)
async def forward_ticket(msg: types.Message):
    forward = await msg.forward(config.TECH_SUPPORT_CHAT_ID)
    documents.Ticket(
        chat_id=forward.chat.id,
        message_id=forward.message_id,
        user_id=msg.from_user.id,
    ).save()


@dp.message_handler(content_types=UserMessageContentTypes, chat_id=config.TECH_SUPPORT_CHAT_ID, is_reply=True)
async def reply_on_ticket(msg: types.Message, reply: types.Message):
    if reply.from_user.id != dp.bot.id:
        return

    ticket = documents.Ticket.objects(chat_id=reply.chat.id, message_id=reply.message_id).first()

    if not ticket:
        await msg.reply('Адресат сообщения не найден')
        return

    await msg.copy_to(ticket.user_id)
