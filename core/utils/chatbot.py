from re_edge_gpt import Chatbot, ConversationStyle
from re_edge_gpt.chathub import ChatHub
from re_edge_gpt.conversation import Conversation


class Chatbot(Chatbot):
  @staticmethod
  async def create(
    proxy: str | None = None,
    cookies: list[dict] | None = None,
  ):
    self = Chatbot.__new__(Chatbot)
    self.conversation_style = ConversationStyle.balanced
    self.proxy = proxy
    self.chat_hub = ChatHub(
        await Conversation.create(self.proxy, cookies=cookies),
        proxy=self.proxy,
        cookies=cookies,
    )
    return self
