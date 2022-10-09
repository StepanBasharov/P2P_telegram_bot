from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

buy_button = InlineKeyboardButton("🟢 Купить", callback_data = 'buy')
sell_button = InlineKeyboardButton("🟥 Продать", callback_data = 'sell')
my_ad = InlineKeyboardButton("📄 Мои объявления", callback_data = 'ad')
orders = InlineKeyboardButton("🪧 Открытые сделки", callback_data = 'orders')

p2p_base_board = InlineKeyboardMarkup().row(buy_button, sell_button).row(my_ad).row(orders)