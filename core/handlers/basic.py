from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Message

async def send_welcome(message: Message, bot:Bot):
    msg = "<b>Bing Chat Bot</b>\n"\
        "/help - Show help message\n"\
        "/reset - Reset conversation\n"\
        "/switch - Switch conversation style (creative,balanced,precise)\n"
    await message.answer(msg)