from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

russian = InlineKeyboardButton("🇷🇺 Русский", callback_data="ru")
english = InlineKeyboardButton("🇺🇸 English", callback_data="en")
arab = InlineKeyboardButton("العربية 🇦🇪", callback_data="ar")
farsi = InlineKeyboardButton("فارسی", callback_data="fa")

lang_board = InlineKeyboardMarkup().row(arab).row(english).row(russian).row(farsi)