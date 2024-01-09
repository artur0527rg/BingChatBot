from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message


class Permission(BaseMiddleware):
  def __init__(self, allowed_users:list):
    super().__init__()
    self.allowed_users:list[int]=set(map(int, allowed_users))

  async def __call__(
    self,
    handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
    event: Message,
    data: Dict[str, Any]
  ) -> Any:
    if event.from_user.id in self.allowed_users:
        return await handler(event, data)
    return await data['bot'].send_message(
       event.from_user.id, "⚠️You are not authorized to use this bot⚠️"
      )