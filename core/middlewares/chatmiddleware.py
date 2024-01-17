import asyncio
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from re_edge_gpt import ImageGenAsync

from core.utils.chatbot import Chatbot


class Chat(BaseMiddleware):
  def __init__(self, cookie):
    super().__init__()
    self.cookie = cookie
    self.edges = dict()
    self.img_edges = dict()

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
    if not self.img_edges.get(event.from_user.id):
      self.img_edges[event.from_user.id] = ImageGenAsync(
        all_cookies = self.cookie,
      )
    data['chat'] = self.edges[event.from_user.id]
    data['img_chat'] = self.img_edges[event.from_user.id]
    return await handler(event, data)
  
  async def close(self):
    await asyncio.gather(
    *[chat.close() for chat in self.edges.values()],
    *[chat.session.aclose() for chat in self.img_edges.values()]
    )