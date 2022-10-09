from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

lang = InlineKeyboardButton("Language", callback_data='lang')
fiat = InlineKeyboardButton("Fiat", callback_data='fiat')

settings_board = InlineKeyboardMarkup().row(lang).row(fiat)
