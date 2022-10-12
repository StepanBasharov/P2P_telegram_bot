from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.pay_methods import pay_methods

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

# Кнопки выбора криптовалюты
choose_btc = InlineKeyboardButton("BTC", callback_data="BTC")
choose_usdt = InlineKeyboardButton("USDT(TRC20)", callback_data="USDT")
choose_xmr = InlineKeyboardButton("XMR", callback_data="XMR")

choose_p2p_crypto_board = InlineKeyboardMarkup().row(choose_btc).row(choose_usdt).row(choose_xmr)

# Кнопка выбора способа оплаты
bank_transfer = InlineKeyboardButton("Банковский перевод", callback_data="bank")
online_wallet = InlineKeyboardButton("Электронные деньги", callback_data="online_wallet")
world_transfer = InlineKeyboardButton("Международные переводы", callback_data="world")
crypto = InlineKeyboardButton("Другая Криптовалюта", callback_data="crypto")
other = InlineKeyboardButton("Другое", callback_data="other")

choose_p2p_paytype = InlineKeyboardMarkup().row(bank_transfer, online_wallet).row(world_transfer, crypto).row(other)

# Выбор метода оплаты
def choose_p2p_paymethod(fiat, method):
    pay_methods_board = InlineKeyboardMarkup()
    for i in pay_methods[fiat][method]:
        pay_methods_board.row(InlineKeyboardButton(i, callback_data=i))
    return pay_methods_board




