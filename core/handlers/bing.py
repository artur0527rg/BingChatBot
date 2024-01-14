from aiogram import Bot
from aiogram.types import Message
from aiogram.filters import CommandObject
from re_edge_gpt import ImageGenAsync

from core.utils.chatbot import Chatbot


async def get_bing_message(message: Message, bot: Bot, chat: Chatbot):
  try:
    result = await chat.answer_tg(message, bot)
  except Exception as ex:
    await message.answer('😢Looks like something went wrong. Try again after a few seconds.')
    return
  for msg in result['messages']:
    for i in range(0, len(msg), 4095):
      await message.answer(msg[i:i+4095])

async def get_reset(message: Message, bot: Bot, chat: Chatbot):
  await chat.reset()
  await message.answer('🔥New converation created!')

async def get_image(
    message: Message,
    img_chat: ImageGenAsync,
    command: CommandObject,
  ):
  if command.args is None:
    await message.answer(
      'Looks like you forgot to write a request.\n'\
      'Example:\n'\
      '`/image The cat is driving a car`'
    )
    return
  tmp = await message.answer('⌛Processing')
  links = []
  try:
    links.extend(await img_chat.get_images(command.args, max_generate_time_sec=20))
  except Exception as ex:
    pass
  
  if links:
    for link in links:
      if link.startswith('http'):
        await message.answer(link, parse_mode=None)
  else:
    await message.answer('😢Looks like something went wrong. Try another query.')
  await tmp.delete()