from contextlib import suppress
import platform
import logging
import json

import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command

from core.settings import settings
from core.utils.commands import set_commands
from core.handlers import basic, bing
from core.middlewares.permissionmiddleware import Permission
from core.middlewares.chatmiddleware import Chat


if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def start_bot(bot:Bot):
  await set_commands(bot)
  await bot.send_message(settings.bots.admin_id, 'Бот запущен!')

async def stop_bot(bot:Bot):
  await bot.send_message(settings.bots.admin_id, 'Бот остановлен!')

async def start():
  logging.basicConfig(
    level=logging.INFO,
    format = '%(asctime)s - [%(levelname)s] - %(name)s'
             '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'  
  )
  bot = Bot(settings.bots.bot_token, parse_mode='Markdown')
  dp = Dispatcher()
  # Middlewares
  dp.message.middleware.register(Permission(settings.bots.allowed_users))
  chat_middleware = Chat(json.loads(open('cookie.json').read()))
  dp.message.middleware.register(chat_middleware)
  dp.callback_query.middleware.register(chat_middleware)
  # Handlers
  dp.message.register(basic.get_welcome, Command(commands=['start', 'help']))
  dp.message.register(bing.get_reset, Command(commands=['reset']))
  dp.message.register(bing.get_switch, Command(commands=['switch']))
  dp.message.register(bing.get_image, Command(commands=['image']))
  dp.message.register(bing.get_bing_message)
  dp.callback_query.register(bing.select_suggestion)
  # Sys
  dp.startup.register(start_bot)
  dp.shutdown.register(stop_bot)

  try:
      await dp.start_polling(bot)
  finally:
    await bot.session.close()
    await chat_middleware.close()

if __name__ == "__main__":
  with suppress(KeyboardInterrupt, SystemExit):
    asyncio.run(start())