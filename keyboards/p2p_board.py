from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.pay_methods import choose_pay_method_from_json
from database.addb import show_ads
from database.orders import send_data_to_order
from database.addb import get_ad_status

buy_button = InlineKeyboardButton("🟢 Купить", callback_data='buy')
sell_button = InlineKeyboardButton("🟥 Продать", callback_data='sell')
my_ad = InlineKeyboardButton("📄 Мои объявления", callback_data='ad')
orders = InlineKeyboardButton("🪧 Открытые сделки", callback_data='orders')

p2p_base_board = InlineKeyboardMarkup().row(buy_button, sell_button).row(my_ad).row(orders)

btc_order = InlineKeyboardButton("BTC", callback_data="btc_order")
usdt_order = InlineKeyboardButton("USDT(TRC20)", callback_data="usdt_order")
xmr_order = InlineKeyboardButton("XMR", callback_data="xmr_order")

create_order_board = InlineKeyboardMarkup().row(btc_order).row(usdt_order).row(xmr_order)

# Кнопка возврата к прошолому выбору
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

bank_transfer_order = InlineKeyboardButton("Банковский перевод", callback_data="bank_order")
online_wallet_order = InlineKeyboardButton("Электронные деньги", callback_data="online_wallet_order")
world_transfer_order = InlineKeyboardButton("Международные переводы", callback_data="world_order")
crypto_order = InlineKeyboardButton("Другая Криптовалюта", callback_data="crypto_order")
other_order = InlineKeyboardButton("Другое", callback_data="other_order")

choose_p2p_paytype_order = InlineKeyboardMarkup().row(bank_transfer_order, online_wallet_order).row(
    world_transfer_order, crypto_order).row(other_order)


def start_exthenge(order_id):
    start_exthenge_button = InlineKeyboardButton("Начать обмен", callback_data=order_id)
    start_exthenge_board = InlineKeyboardMarkup().row(start_exthenge_button)
    return start_exthenge_board


# Выбор метода оплаты
def choose_p2p_paymethod(fiat, method):
    pay_methods_board = InlineKeyboardMarkup()
    data = choose_pay_method_from_json(fiat, method)
    for i in data:
        pay_methods_board.row(InlineKeyboardButton(i, callback_data=i))
    return pay_methods_board


def choose_order_paymethod(fiat, method):
    pay_methods_board = InlineKeyboardMarkup()
    if method == "online_wallet_order":
        method = method.split("_")[0] + "_wallet"
    else:
        method = method.split("_")[0]
    data = choose_pay_method_from_json(fiat, method)
    for i in data:
        pay_methods_board.row(InlineKeyboardButton(i, callback_data=f"{i}_order"))
    return pay_methods_board


def show_ads_board(user_id):
    my_ads_board = InlineKeyboardMarkup()
    data = show_ads(user_id)
    for i in data:
        if i[4] == "BUY":
            button_text = f"🟢{i[4]}, {i[3]}, {i[2]}, {i[1]}"
        else:
            button_text = f"🟥{i[4]}, {i[3]}, {i[2]}, {i[1]}"
        my_ads_board.row(InlineKeyboardButton(button_text, callback_data=i[0]))
    my_ads_board.row(InlineKeyboardButton("➕ Разместить новое объявление", callback_data='add_new_ad'))
    return my_ads_board


def show_ads_to_create_order_board(user_id):
    ads_to_order_board = InlineKeyboardMarkup()
    data = send_data_to_order(user_id)
    if len(data) == 0:
        ads_to_order_board.row(InlineKeyboardButton("К сожалению объявлений нет", callback_data="ads_none"))
    else:
        for i in data:
            if i[4] == "SELL":
                button_text = f"🟢 {i[3]}, {i[1]}, ({i[5]}), {i[2]}"
            else:
                button_text = f"🟥 {i[3]}, {i[1]}, ({i[5]}), {i[2]}"
            ads_to_order_board.row(InlineKeyboardButton(button_text, callback_data=i[0]))
    return ads_to_order_board


def is_paid(order_id):
    is_paid_board = InlineKeyboardMarkup()
    is_paid_board.row(InlineKeyboardButton("Оплачено", callback_data=f"is_paid_taker_{order_id}"))
    return is_paid_board


def is_paid_maker(order_id):
    is_paid_board = InlineKeyboardMarkup()
    is_paid_board.row(InlineKeyboardButton("Оплачено", callback_data=f"is_paid_maker_{order_id}"))
    return is_paid_board


def confirm_paid_from_maker(order_id):
    confirm_paid_board = InlineKeyboardMarkup()
    confirm_paid_board.row(InlineKeyboardButton("Оплата получена", callback_data=f"paid_confirm_{order_id}"))
    return confirm_paid_board


def confirm_paid_from_taker(order_id):
    confirm_paid_board = InlineKeyboardMarkup()
    confirm_paid_board.row(InlineKeyboardButton("Оплата получена", callback_data=f"paid_confirm_taker_{order_id}"))
    return confirm_paid_board


def confirm_requisites_buttons(order_id, requisit, amount):
    confirm_requisites_board = InlineKeyboardMarkup()
    confirm_requisites_board.row(InlineKeyboardButton("✅", callback_data=f"req_done_{requisit}_{amount}_{order_id}"),
                                 InlineKeyboardButton("❌", callback_data=f"req_fail_{order_id}"))
    return confirm_requisites_board


def my_ad_settings(ad_id):
    settings_ad_board = InlineKeyboardMarkup()
    new_limit = InlineKeyboardButton("📐 Лимиты", callback_data=f"new_limit_{ad_id}")
    new_price = InlineKeyboardButton("💵 Цена", callback_data=f"new_price_{ad_id}")
    new_description = InlineKeyboardButton("📋 Условия", callback_data=f"new_description_{ad_id}")
    new_requisites = InlineKeyboardButton("💸 Реквизиты", callback_data=f"new_requisites_{ad_id}")
    if str(get_ad_status(ad_id)) == "1":
        status_button = InlineKeyboardButton("🟢 Выключить", callback_data=f"off_{ad_id}")
    else:
        status_button = InlineKeyboardButton("🟥 Включить", callback_data=f"on_{ad_id}")
    delete_ad = InlineKeyboardButton("🗑 Удалить", callback_data=f"delete_{ad_id}")
    settings_ad_board.row(new_limit, new_price).row(new_description, new_requisites).row(status_button, delete_ad)
    return settings_ad_board
