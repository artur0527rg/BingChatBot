from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from core.utils.chatbot import Chatbot
from core.utils.exeptions import ChatException


class Chat(BaseMiddleware):
  def __init__(self, cookie):
    super().__init__()
    self.cookie = cookie
    self.edges = dict()

  async def __call__(
    self,
    handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
    event: Message,
    data: Dict[str, Any]
  ) -> Any:
    if not self.edges.get(event.from_user.id):
      self.edges[event.from_user.id] = await Chatbot.create(
        cookies=self.cookie,
      )
    data['chat'] = self.edges[event.from_user.id]
    try:
      return await handler(event, data)
    except ChatException:
      return await event.answer('Something went wrong, try again later.')
  
  async def close(self):
    for chat in self.edges.values():
      await chat.close()