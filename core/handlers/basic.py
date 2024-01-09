from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Message

async def foo(message: Message, bot:Bot):
    await message.answer('Hi')