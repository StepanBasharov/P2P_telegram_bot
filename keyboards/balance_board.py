from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from handless.translater import get_json_text

# Базовая клавиатура
def take_off_on(user_id):
    take_on = InlineKeyboardButton(get_json_text("buttons_text", "input_button", user_id), callback_data='take_on')
    take_off = InlineKeyboardButton(get_json_text("buttons_text", "output_button", user_id), callback_data='take_off')

    balance_base_board = InlineKeyboardMarkup().row(take_on, take_off)
    return balance_base_board

# Выбор для ввода

btc_on = InlineKeyboardButton("BTC", callback_data='btc_on')
btc_off = InlineKeyboardButton("BTC", callback_data='btc_off')

usdt_on = InlineKeyboardButton("USDT", callback_data='usdt_on')
usdt_off = InlineKeyboardButton("USDT", callback_data='usdt_off')

xmr_on = InlineKeyboardButton("XMR", callback_data='xmr_on')
xmr_off = InlineKeyboardButton("XMR", callback_data='xmr_off')

take_on_crypro_board = InlineKeyboardMarkup().row(btc_on).row(usdt_on).row(xmr_on)
take_off_crypto_board = InlineKeyboardMarkup().row(btc_off).row(usdt_off).row(xmr_off)


def btc_is_send(user_id):
    button_success_btc = InlineKeyboardButton(f"BTC {get_json_text('buttons_text', 'is_send', user_id)}",
                                              callback_data="btc_success")

    board_success_btc = InlineKeyboardMarkup().row(button_success_btc)

    return board_success_btc


def usdt_is_send(user_id):
    button_success_usdt = InlineKeyboardButton(f"USDT {get_json_text('buttons_text', 'is_send', user_id)}", callback_data="usdt_success")

    board_success_usdt = InlineKeyboardMarkup().row(button_success_usdt)

    return board_success_usdt


def xmr_is_send(user_id):
    button_success_xmr = InlineKeyboardButton(f"XMR {get_json_text('buttons_text', 'is_send', user_id)}", callback_data="xmr_success")

    board_success_xmr = InlineKeyboardMarkup().row(button_success_xmr)

    return board_success_xmr
