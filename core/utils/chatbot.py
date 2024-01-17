import re

from aiogram import Bot
from aiogram.types import Message
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
  
  async def answer_tg(self, promt:str, bot:Bot):
    is_disengaged = False
    result = {
      'message':'',
      'suggestions':[],
    }
    links = []

    response = await self.ask(
      promt, conversation_style=self.conversation_style
    )
    for message in response['item']['messages'][1:]:
      if not message.get('text'):
        continue
      message_text = re.sub(r'\[\^\d\^]',  '', message['text'])
      # Links
      if message.get('sourceAttributions'):
        for source in message['sourceAttributions']:
          links.append(f"[{source['providerDisplayName']}]({source['seeMoreUrl']})")
      # Suggestions
      if message.get('suggestedResponses'):
        for suggestion in message['suggestedResponses']:
          result['suggestions'].append(suggestion['text'])
      # Text
      result['message']+=message_text
      result['message']+='\n----------\n'

    if links:
      result['message']+='\nLinks:\n'
    for index in range(len(links)):
      result['message']+=f"{index+1}. {links[index]}\n"
    if result['message']:
      max_messages = response['item']['throttling']['maxNumUserMessagesInConversation']
      num_messages = response['item']['throttling']['numUserMessagesInConversation']
      result['message']+= (
        f"\n\n🟢Messages In Conversation : {num_messages} / {max_messages}"
      )
    return result


      
