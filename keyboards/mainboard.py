from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from handless.translater import get_json_text


def show_mainboard(user_id):
    button_p2p = KeyboardButton(f'🔄 {get_json_text("buttons_text", "p2p_button", user_id)}')
    button_balance = KeyboardButton(f'💰 {get_json_text("buttons_text", "balance_button", user_id)}')
    button_settings = KeyboardButton(f'⚙ {get_json_text("buttons_text", "settings_button", user_id)}')
    button_support = KeyboardButton(f'🚨 {get_json_text("buttons_text", "suppotr_button", user_id)}')
    button_faq = KeyboardButton(f'📌 {get_json_text("buttons_text", "faq_button", user_id)}')

    mainboard = ReplyKeyboardMarkup(resize_keyboard=True)
    mainboard.row(button_p2p, button_balance).row(button_settings).row(button_support, button_faq)

    return mainboard
