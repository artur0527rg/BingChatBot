from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

links_markup = InlineKeyboardMarkup(inline_keyboard=[
  [
    InlineKeyboardButton(
      text='Github(author)',
      url='https://github.com/artur0527rg/BingChatBot',
    )
  ],
  [
    InlineKeyboardButton(
      text='Github(reference)',
      url='https://github.com/pininkara/BingChatBot',
    )
  ],
])

def suggestions_builder(suggestions:list[str]):
    builder = InlineKeyboardBuilder()
    for suggestion in suggestions:
        suggestion = suggestion[:64]
        callback = suggestion.lower().replace(' ', '_')
        builder.button(text=suggestion, callback_data=callback)
    builder.adjust(1)
    return builder