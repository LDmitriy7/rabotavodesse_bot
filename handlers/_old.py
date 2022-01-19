import re
from time import time

from aiogram.types import ContentType, ChatType

import config
import keyboards as kb
import texts
from loader import db, dp, lock
from safecalls import *


# Database setup

# {uid: 123456789, added: [], count: 0} & {last_msg: msg_id, chat_name: str}
# chat = client['chat_' + str(abs(chat_id))]


@dp.message_handler(commands=['start', 'list'])
async def start_handler(message: types.Message):
    if message.get_args() != 'techsupport':
        data = []
        for chat in (await db.list_collection_names(filter={"name": {"$regex": r"chat_\d?"}})):
            user = await db[chat].find_one({'uid': message.from_user.id})
            if user is not None:
                chat = await db[chat].find_one({'chat_name': {'$exists': True}})
                data.append(f'{chat["chat_name"]}: {user["count"]}/{config.INVITE_COUNT}')
        if data:
            await send_message(message.from_user.id, "Приглашено: \n" + "\n".join(data))
        else:
            await send_message(message.from_user.id, "Вы уже можете писать в чате или ещё в него не зашли")
    else:
        await send_message(message.from_user.id, 'Для разговора с техподдержкой напишите сообщение',
                           reply_msg_id=message.message_id)


# @dp.message_handler(commands='add', user_id=[364702722, 433120468])
# async def add_handler(message: types.Message):
#     chat = db['chat_' + str(abs(message.chat.id))]
#
#     file = open('_quantity_invite.csv', 'r')
#     n = 0
#     for entry in file:
#         uid, num = map(int, entry.split(','))
#         if num < 20:
#             await chat.replace_one({'uid': uid},
#                                    {'uid': uid, 'added': [], 'count': num}, upsert=True)
#             print(uid, num)
#             n += 1


@dp.message_handler(content_types=ContentType.NEW_CHAT_MEMBERS)
async def new_member_handler(message: types.Message):
    async with lock:
        if message.chat.id == config.TECH_SUPPORT_CHAT_ID:
            return
        if message.chat.id in config.WHITELIST_CHATS_IDS:
            return
        chat = db['chat_' + str(abs(message.chat.id))]
        user = await chat.find_one({'uid': message.from_user.id})
        # print(message.new_chat_members[0].id, message.from_user.id)
        if message.new_chat_members[0].id == message.from_user.id:
            await chat.replace_one({'uid': message.new_chat_members[0].id},
                                   {'uid': message.new_chat_members[0].id, 'added': [], 'count': 0}, upsert=True)
            await restrict_write(message.chat.id, message.new_chat_members[0].id)
        else:
            cnt = 0
            to_add = []
            for new_member in message.new_chat_members:
                if user is not None:
                    if new_member.id not in user['added']:
                        cnt += 1
                        to_add.append(new_member.id)
                await chat.replace_one({'uid': new_member.id},
                                       {'uid': new_member.id, 'added': [], 'count': 0}, upsert=True)
                await restrict_write(message.chat.id, new_member.id)
            if user is not None:
                if user['count'] + cnt >= config.INVITE_COUNT:
                    await chat.find_one_and_delete({'uid': user['uid']})
                    await unrestrict(message.chat.id, user['uid'])
                else:
                    await chat.find_one_and_update({'uid': user['uid']}, {'$inc': {'count': cnt},
                                                                          '$push': {'added': {'$each': to_add}}})
        chat_config = await chat.find_one({'last_msg': {'$exists': True}})
        msg = await bot.send_photo(message.chat.id, config.GROUP_RULES_PHOTO_URL, caption=texts.group_rules,
                                   parse_mode=types.ParseMode.HTML, reply_markup=kb.ChannelUrl())
        logger.info('new msg: ' + str(msg.message_id))
        if chat_config is not None:
            await delete_message(message.chat.id, chat_config['last_msg'])
            logger.info('deleting:' + str(chat_config['last_msg']))
            await chat.find_one_and_update({'last_msg': {'$exists': True}}, {'$set': {'last_msg': msg.message_id}})
        else:
            await chat.insert_one({'last_msg': msg.message_id, 'chat_name': message.chat.full_name})

# @dp.message_handler(content_types=[ContentType.TEXT, ContentType.PHOTO, ContentType.DOCUMENT])
# async def text_message_handler(msg: types.Message):
# if str(msg.chat.id) == config.TECH_SUPPORT_CHAT_ID:
#     if msg.reply_to_message and bot.id == msg.reply_to_message.from_user.id:
#         if msg.reply_to_message.forward_from is not None:
#             if msg.reply_to_message.forward_from.id != config.Bot.id:
#                 await send_message(msg.reply_to_message.forward_from.id, msg.text)
#         else:
#             search = re.search(r'tg://user\?id=(?P<uid>\d+)', msg.reply_to_message.md_text)
#             if search:
#                 await send_message(int(search.group('uid')), msg.text)
# elif msg.chat.type == ChatType.PRIVATE:
#     await bot.send_message(config.TECH_SUPPORT_CHAT_ID, f"[Сообщение от {msg.from_user.full_name}"
#                                                         f":]"
#                                                         f"(tg://user?id={msg.from_user.id})",
#                            parse_mode=types.ParseMode.MARKDOWN)
#     await msg.forward(config.TECH_SUPPORT_CHAT_ID)
# elif msg.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
#     if msg.from_user.id not in config.WHITELIST:
#         if msg.chat.id in config.WHITELIST_CHATS:
#             return
#         await restrict_write(msg.chat.id, msg.from_user.id, until_time=int(time()) + config.RESTRICT)
