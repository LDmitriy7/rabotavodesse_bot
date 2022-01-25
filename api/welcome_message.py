from contextlib import suppress

from aiogram.utils.exceptions import TelegramAPIError

import config
import keyboards as kb
import texts
from loader import bot
from models import documents


async def replace_welcome_message(chat_id: int):
    new_msg = await bot.send_photo(
        chat_id=chat_id,
        photo=config.GROUP_RULES_PHOTO_URL,
        caption=texts.group_rules,
        reply_markup=kb.ChannelUrl(),
    )

    welcome_msg = documents.WelcomeMessage.objects().first()

    if welcome_msg:
        with suppress(TelegramAPIError):
            await bot.delete_message(chat_id, welcome_msg.message_id)
        welcome_msg.message_id = new_msg.message_id
    else:
        welcome_msg = documents.WelcomeMessage(message_id=new_msg.message_id)

    welcome_msg.save()
