from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram_utils.keyboards import InlineKeyboardButton


class Main(ReplyKeyboardMarkup):
    TECH_SUPPORT = 'Написать в техподдержку'
    CONTACTS_INFO = 'Сколько контактов осталось?'

    def __init__(self):
        super().__init__(resize_keyboard=True, row_width=1)
        self.add(self.TECH_SUPPORT, self.CONTACTS_INFO)


class ChannelUrl(InlineKeyboardMarkup):
    URL = InlineKeyboardButton(text='«HoReCa | Job in Odessa»', url='https://t.me/+5sXbtxiiMiU2NzQy')

    def __init__(self):
        super().__init__()

        self.row(self.URL)
