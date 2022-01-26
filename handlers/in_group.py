from aiogram import types
from aiogram.types import ChatType, ContentType
from aiogram_utils.content_types import UserMessageContentTypes

import api
import config
from loader import dp
from models import documents


@dp.message_handler(content_types=ContentType.NEW_CHAT_MEMBERS, chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def on_new_chat_members(msg: types.Message):
    await api.replace_welcome_message(msg.chat.id)

    user_inviter = documents.User.objects(id=msg.from_user.id).first() or documents.User(id=msg.from_user.id)

    for member in msg.new_chat_members:
        user = documents.User.objects(id=member.id).first() or documents.User(id=member.id)

        if len(user.invited_users_ids) < config.USERS_TO_INVITE_COUNT:
            await api.restrict_writing(msg.chat, member)

        if user.id != user_inviter.id:  # user joined the group not himself
            if user.id not in user_inviter.invited_users_ids:
                user_inviter.invited_users_ids.append(user.id)

    if len(user_inviter.invited_users_ids) >= config.USERS_TO_INVITE_COUNT:
        await api.unrestrict_writing(msg.chat, msg.from_user)

    user_inviter.save()


@dp.message_handler(content_types=UserMessageContentTypes, chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def restrict(msg: types.Message):
    user = documents.User.objects(id=msg.from_user.id).first() or documents.User(id=msg.from_user.id)

    if len(user.invited_users_ids) < config.USERS_TO_INVITE_COUNT:
        await api.restrict_writing(msg.chat, msg.from_user)
        await msg.delete()
    else:
        await api.restrict_writing(msg.chat, msg.from_user, for_time=config.RESTRICT_TIME)
