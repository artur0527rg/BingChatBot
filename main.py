import logging

import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command

from core.settings import settings
from core.utils.commands import set_commands
from core.handlers import basic
from core.middlewares.permissionmiddleware import Permission


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
  bot = Bot(settings.bots.bot_token, parse_mode='HTML')
  dp = Dispatcher()
  # Middlewares
  dp.message.middleware.register(Permission(settings.bots.allowed_users))
  # Handlers
  # dp.message.register(basic.foo)
  # Sys
  dp.startup.register(start_bot)
  dp.shutdown.register(stop_bot)

  try:
    await dp.start_polling(bot)
  finally:
    await bot.session.close()

if __name__ == "__main__":
  asyncio.run(start())