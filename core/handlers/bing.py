from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandObject
from re_edge_gpt import ImageGenAsync, ConversationStyle

from core.utils.chatbot import Chatbot
from core.keyboards.inline import suggestions_builder


async def get_bing_message(message: Message, bot: Bot, chat: Chatbot):
  try:
    result = await chat.answer_tg(message.text, bot)
  except Exception as ex:
    await message.answer('😢Looks like something went wrong. Try again after a few seconds.')
    return
  # Empty answer
  if not result['message']:
    await message.answer(
      'Looks like Bing ended the chat😢.\n'\
      'To start new conversation use - /reset',
    )
  # Answer
  for i in range(0, len(result['message']), 4095):
    if i+4095<len(result['message']):
      await message.answer(result['message'][i:i+4095])
    else:
      await message.answer(
        result['message'][i:i+4095],
        reply_markup=suggestions_builder(result['suggestions']).as_markup()
      )

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
    links.extend(await img_chat.get_images(command.args, max_generate_time_sec=60))
  except Exception as ex:
    pass
  
  if links:
    for link in links:
      if link.startswith('http'):
        await message.answer(link, parse_mode=None)
  else:
    await message.answer('😢Looks like something went wrong. Try another query.')
  await tmp.delete()

async def select_suggestion(call: CallbackQuery, bot:Bot, chat:Chatbot):
  promt = call.data.replace('_', ' ')
  try:
    result = await chat.answer_tg(promt, bot)
  except Exception as ex:
    await bot.send_message(
      call.from_user.id,
      '😢Looks like something went wrong. Try again after a few seconds.'
    )
    return
  # Empty answer
  if not result['message']:
    await bot.send_message(
      call.from_user.id,
      'Looks like Bing ended the chat😢.\n'\
      'To start new conversation use - /reset',
    )
  # Answer
  for i in range(0, len(result['message']), 4095):
    if i+4095<len(result['message']):
      await bot.send_message(
        call.from_user.id,
        result['message'][i:i+4095]
      )
    else:
      await bot.send_message(
        call.from_user.id,
        result['message'][i:i+4095],
        reply_markup=suggestions_builder(result['suggestions']).as_markup()
      )

async def get_switch(
    message: Message,
    chat: Chatbot,
    command: CommandObject,
  ):
  style = ''
  if command.args:
    style = command.args.lower().strip()
    
  if style == 'creative':
    chat.conversation_style = ConversationStyle.creative
    await message.answer('🎨Changed to Creative')
  elif style == 'balanced':
    chat.conversation_style = ConversationStyle.balanced
    await message.answer('⚖️Changed to Balanced')
  elif style == 'precise':
    chat.conversation_style = ConversationStyle.precise
    await message.answer('🎯Changed to Precise')
  else: 
    await message.answer(
      'Сhoose one communication option:\n'\
      'creative|balanced|precise\n'
      '\nExample:\n'\
      '`/switch balanced`'
    )