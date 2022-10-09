from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

buy_button = InlineKeyboardButton("🟢 Купить", callback_data='buy')
sell_button = InlineKeyboardButton("🟥 Продать", callback_data='sell')
my_ad = InlineKeyboardButton("📄 Мои объявления", callback_data='ad')
orders = InlineKeyboardButton("🪧 Открытые сделки", callback_data='orders')

p2p_base_board = InlineKeyboardMarkup().row(buy_button, sell_button).row(my_ad).row(orders)

add_ad = InlineKeyboardButton("➕ Разместить новое объявление", callback_data='add_new_ad')

add_ad_board = InlineKeyboardMarkup().row(add_ad)