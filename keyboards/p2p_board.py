from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

buy_button = InlineKeyboardButton("🟢 Купить", callback_data='buy')
sell_button = InlineKeyboardButton("🟥 Продать", callback_data='sell')
my_ad = InlineKeyboardButton("📄 Мои объявления", callback_data='ad')
orders = InlineKeyboardButton("🪧 Открытые сделки", callback_data='orders')

p2p_base_board = InlineKeyboardMarkup().row(buy_button, sell_button).row(my_ad).row(orders)

add_ad = InlineKeyboardButton("➕ Разместить новое объявление", callback_data='add_new_ad')

add_ad_board = InlineKeyboardMarkup().row(add_ad)

#Кнопка возврата к прошолому выбору
back_button = InlineKeyboardButton("❌ Назад", callback_data="back_to")

# Кнопки выбора типа объявления ( Buy or Sell)
buy_ad_create = InlineKeyboardButton("🟢 Купить", callback_data="create_buy_ad")
sell_ad_create = InlineKeyboardButton("🟥 Продать", callback_data="create_sell_ad")

buy_or_sell_board = InlineKeyboardMarkup().row(buy_ad_create, sell_ad_create).row(back_button)