from aiogram.utils.exceptions import TelegramAPIError

import config
import keyboards as kb
import texts
from loader import bot
from loader import log
from models import documents
from loader import lock


async def _replace_welcome_message(chat_id: int):
    new_msg = await bot.send_photo(
        chat_id=chat_id,
        photo=config.GROUP_RULES_PHOTO_URL,
        caption=texts.group_rules,
        reply_markup=kb.ChannelUrl(),
    )

    welcome_msg = documents.WelcomeMessage.objects().first()

    if welcome_msg:
        try:
            await bot.delete_message(chat_id, welcome_msg.message_id)
        except TelegramAPIError as e:
            log.exception(e)

        welcome_msg.message_id = new_msg.message_id
    else:
        welcome_msg = documents.WelcomeMessage(message_id=new_msg.message_id)

    welcome_msg.save()


async def replace_welcome_message(chat_id: int):
    async with lock:
        await _replace_welcome_message(chat_id)
