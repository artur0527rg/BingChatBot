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
  
  async def answer_tg(self, message:Message, bot:Bot):
    is_disengaged = False
    result = {
      'messages':[],
      'suggestions':[],
    }

    response = await self.ask(
      message.text, conversation_style=self.conversation_style
    )
    for message in response['item']['messages'][1:]:
      if message.get('messageType') == 'Disengaged':
        is_disengaged = True
      if not message.get('text'):
        continue
      message_text = re.sub(r'\[\^\d\^]',  '', message['text'])
      if message.get('sourceAttributions'):
        message_text += "\n\nLinks:\n"
        for source in message['sourceAttributions']:
          message_text += f"[{source['providerDisplayName']}]({source['seeMoreUrl']})\n"
      result['messages'].append(message_text)
      if message.get('suggestedResponses'):
        for suggestion in message['suggestedResponses']:
          result['suggestions'].append(suggestion['text'])

    max_messages = response['item']['throttling']['maxNumUserMessagesInConversation']
    num_messages = response['item']['throttling']['numUserMessagesInConversation']
    result['messages'].append(
      f"🟢Messages In Conversation : {num_messages} / {max_messages}",
    )

    if is_disengaged:
      result['messages'].append(
        'Bing ended the chat😢.\n'\
        'To start new conversation use - /reset',
      )
    return result


      
