from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import ChatType

import config


class CheckAccess(BaseMiddleware):

    @staticmethod
    async def on_pre_process_message(msg: types.Message, *_):
        if msg.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            if msg.chat.id not in config.WHITELIST_CHATS_IDS:
                raise CancelHandler
