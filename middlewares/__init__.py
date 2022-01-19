from aiogram_utils import middlewares

from loader import dp
from .check_access import CheckAccess


def setup():
    dp.setup_middleware(middlewares.AnswerAnyQuery())
    dp.setup_middleware(CheckAccess())
