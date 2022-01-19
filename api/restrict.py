import time

from aiogram import types


async def restrict_writing(chat: types.Chat, user: types.User, for_time: int = 0):
    perms = types.ChatPermissions(can_send_messages=False, can_invite_users=True)
    await chat.restrict(
        user_id=user.id,
        permissions=perms,
        until_date=int(time.time()) + for_time,
    )


async def unrestrict_writing(chat: types.Chat, user: types.User):
    perms = types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_invite_users=True,
    )
    await chat.restrict(user_id=user.id, permissions=perms)
