from aiogram import types
from aiogram.utils import exceptions

from loader import dp


@dp.errors_handler(exception=exceptions.BotBlocked)
@dp.errors_handler(exception=exceptions.MessageNotModified)
@dp.errors_handler(exception=exceptions.CantRestrictChatOwner)
@dp.errors_handler(exception=exceptions.UserIsAnAdministratorOfTheChat)
async def ignore(*_):
    return True


@dp.errors_handler(exception=exceptions.NotEnoughRightsToRestrict)
async def ask_to_promote_me(update: types.Update, *_):
    if update.message:
        await update.message.reply('Не могу ограничить пользователя, нужны права администратора')
        return True
