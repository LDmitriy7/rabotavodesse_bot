from loader import dp
import aiogram_utils.filters
from aiogram.dispatcher.filters.builtin import AdminFilter


def setup():
    aiogram_utils.filters.setup(dp)
