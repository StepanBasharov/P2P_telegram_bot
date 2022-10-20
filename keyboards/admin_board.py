from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


statistics = KeyboardButton("📈 Статистика")
add_paymethod = KeyboardButton("➕ Добавить платежку")
add_admin = KeyboardButton("➕ Добавить нового администратора")
cancel = KeyboardButton("❌ Отменить")
admin_board = ReplyKeyboardMarkup(resize_keyboard=True).row(statistics, add_paymethod).row(add_admin).row(cancel)


cancel = KeyboardButton("❌ Отменить")
cancel_board = ReplyKeyboardMarkup(resize_keyboard=True).row(cancel)