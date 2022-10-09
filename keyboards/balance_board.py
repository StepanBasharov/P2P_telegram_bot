from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# Базовая клавиатура
take_on = InlineKeyboardButton("Ввод", callback_data='take_on')
take_off = InlineKeyboardButton("Вывод", callback_data='take_off')

balance_base_board = InlineKeyboardMarkup().row(take_on, take_off)

# Выбор для ввода

btc_on = InlineKeyboardButton("BTC", callback_data='btc_on')
btc_off = InlineKeyboardButton("BTC", callback_data='btc_off')

usdt_on = InlineKeyboardButton("USDT", callback_data='usdt_on')
usdt_off = InlineKeyboardButton("USDT", callback_data='usdt_off')

xmr_on = InlineKeyboardButton("XMR", callback_data='xmr_on')
xmr_off = InlineKeyboardButton("XMR", callback_data='xmr_off')

take_on_crypro_board = InlineKeyboardMarkup().row(btc_on).row(usdt_on).row(xmr_on)
take_off_crypto_board = InlineKeyboardMarkup().row(btc_off).row(usdt_off).row(xmr_off)

button_success_btc = InlineKeyboardButton("BTC отправлены", callback_data="btc_success")

board_success_btc = InlineKeyboardMarkup().row(button_success_btc)

button_success_usdt = InlineKeyboardButton("USDT отправлены", callback_data="usdt_success")

board_success_usdt = InlineKeyboardMarkup().row(button_success_usdt)

button_success_xmr = InlineKeyboardButton("XMR отправлены", callback_data="xmr_success")

board_success_xmr = InlineKeyboardMarkup().row(button_success_xmr)

