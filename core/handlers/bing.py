from aiogram import Bot
from aiogram.types import Message

from core.utils.chatbot import Chatbot


async def get_bing_message(message: Message, bot: Bot, chat: Chatbot):
  result = await chat.answer_tg(message, bot)
  for msg in result['messages']:
    for i in range(0, len(msg), 4095):
      await message.answer(msg[i:i+4095])
  chat.chat_hub.cookies = None

async def get_reset(message: Message, bot: Bot, chat: Chatbot):
  await chat.reset()
  await message.answer('🔥New converation created!')