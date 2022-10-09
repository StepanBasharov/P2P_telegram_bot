from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_p2p = KeyboardButton('🔄 P2P Обмен')
button_balance = KeyboardButton('💰 Баланс')
button_settings = KeyboardButton('⚙ Настройки')
button_support = KeyboardButton('🚨 Поддержка')
button_faq = KeyboardButton('📌 FAQ')


mainboard = ReplyKeyboardMarkup(resize_keyboard=True)
mainboard.row(button_p2p, button_balance).row(button_settings).row(button_support, button_faq)