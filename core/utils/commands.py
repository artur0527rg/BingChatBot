from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
  commands = [
    BotCommand(
      command='help',
      description='Bot info',
    ),
    BotCommand(
      command='reset',
      description='Reset conversation',
    ),
    BotCommand(
      command='switch',
      description='Select conversation style',
    ),
  ]
  
  await bot.set_my_commands(commands, BotCommandScopeDefault())
