from aiogram import Bot
from aiogram.types import Message

from core.utils.chatbot import Chatbot
from core.utils.exeptions import ChatException


async def get_bing_message(message: Message, bot: Bot, chat: Chatbot):
  try:
    result = await chat.answer_tg(message, bot)
  except Exception:
    raise ChatException()
  for msg in result['messages']:
    for i in range(0, len(msg), 4095):
      await message.answer(msg[i:i+4095])

async def get_reset(message: Message, bot: Bot, chat: Chatbot):
  try:
    await chat.reset()
  except Exception:
    raise ChatException()
  await message.answer('🔥New converation created!')