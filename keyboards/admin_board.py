from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

statistics = KeyboardButton("📈 Статистика")
all_users = KeyboardButton("👥 Пользователи")
add_paymethod = KeyboardButton("➕ Добавить платежку")
add_admin = KeyboardButton("➕ Добавить нового администратора")
withdraw_btc = KeyboardButton("Вывести BTC")
withdraw_usdt = KeyboardButton("Вывести USDT")
withdraw_xmr = KeyboardButton("Вывести XMR")
cancel = KeyboardButton("❌ Отменить")
admin_board = ReplyKeyboardMarkup(resize_keyboard=True).row(statistics, all_users, add_paymethod).row(add_admin).row(
    withdraw_btc, withdraw_usdt, withdraw_xmr).row(cancel)

cancel = KeyboardButton("❌ Отменить")
cancel_board = ReplyKeyboardMarkup(resize_keyboard=True).row(cancel)
