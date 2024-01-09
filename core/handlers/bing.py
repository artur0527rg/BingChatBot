from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Message

from core.utils.chatbot import Chatbot

async def bing_message(message: Message, bot:Bot, chat:Chatbot):
    response = await chat.ask(
        message.text,
        conversation_style=chat.conversation_style,
    )
    await message.answer('test response')