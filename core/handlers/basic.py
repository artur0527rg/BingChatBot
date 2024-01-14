from aiogram import Bot
from aiogram.types import Message

from core.keyboards import inline

async def get_welcome(message: Message, bot: Bot):
    msg = "**Bing Chat Bot**\n"\
        "/help - Show help message\n"\
        "/reset - Reset conversation\n"\
        "/switch - Switch conversation style (creative,balanced,precise)\n"\
        "/image _query_  - Generate image\n"
    await message.answer(msg, reply_markup=inline.links_markup)