from aiogram.types import InlineKeyboardMarkup
from aiogram_utils.keyboards import InlineKeyboardButton


class ChannelUrl(InlineKeyboardMarkup):
    URL = InlineKeyboardButton(text='«HoReCa | Job in Odessa»', url='https://t.me/+5sXbtxiiMiU2NzQy')

    def __init__(self):
        super().__init__()

        self.row(self.URL)
