from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from keyboards.pay_methods import choose_pay_method_from_json
from database.addb import show_ads
from database.orders import send_data_to_order
from database.addb import get_ad_status
from handless.translater import get_json_text


def main_p2p_il_board(user_id):
    buy_button = InlineKeyboardButton(f"🟢 {get_json_text('buttons_text', 'buy_button', user_id)}", callback_data='buy')
    sell_button = InlineKeyboardButton(f"🟥 {get_json_text('buttons_text', 'sell_button', user_id)}",
                                       callback_data='sell')
    my_ad = InlineKeyboardButton(f"📄 {get_json_text('buttons_text', 'my_ads_buttond', user_id)}", callback_data='ad')
    orders = InlineKeyboardButton(f"🪧 {get_json_text('buttons_text', 'open_exch', user_id)}", callback_data='orders')

    p2p_base_board = InlineKeyboardMarkup().row(buy_button, sell_button).row(my_ad)
    return p2p_base_board


btc_order = InlineKeyboardButton("BTC", callback_data="btc_order")
usdt_order = InlineKeyboardButton("USDT(TRC20)", callback_data="usdt_order")
xmr_order = InlineKeyboardButton("XMR", callback_data="xmr_order")

create_order_board = InlineKeyboardMarkup().row(btc_order).row(usdt_order).row(xmr_order)


# Кнопка возврата к прошолому выбору
def back_to_button_inl(user_id):
    back_button = InlineKeyboardButton(f"❌ {get_json_text('buttons_text', 'back_to_button', user_id)}",
                                       callback_data="back_to")

    return back_button


def back_to_button(user_id):
    back_button = KeyboardButton(f"❌ {get_json_text('buttons_text', 'back_to_button', user_id)}")
    back_board = ReplyKeyboardMarkup(resize_keyboard=True).row(back_button)
    return back_board


# Кнопки выбора типа объявления ( Buy or Sell)
def choose_type_board(user_id):
    buy_ad_create = InlineKeyboardButton(f"🟢 {get_json_text('buttons_text', 'buy_button', user_id)}",
                                         callback_data="create_buy_ad")
    sell_ad_create = InlineKeyboardButton(f"🟥 {get_json_text('buttons_text', 'sell_button', user_id)}",
                                          callback_data="create_sell_ad")

    buy_or_sell_board = InlineKeyboardMarkup().row(buy_ad_create, sell_ad_create).row(back_to_button_inl(user_id))

    return buy_or_sell_board


# Кнопки выбора криптовалюты
choose_btc = InlineKeyboardButton("BTC", callback_data="BTC")
choose_usdt = InlineKeyboardButton("USDT(TRC20)", callback_data="USDT")
choose_xmr = InlineKeyboardButton("XMR", callback_data="XMR")

choose_p2p_crypto_board = InlineKeyboardMarkup().row(choose_btc).row(choose_usdt).row(choose_xmr)


# Кнопка выбора способа оплаты
def pay_type(user_id):
    bank_transfer = InlineKeyboardButton(get_json_text("buttons_text", 'bank_button', user_id), callback_data="bank")
    online_wallet = InlineKeyboardButton(get_json_text("buttons_text", 'online_wallet_button', user_id),
                                         callback_data="online_wallet")
    world_transfer = InlineKeyboardButton(get_json_text("buttons_text", 'world_button', user_id), callback_data="world")
    crypto = InlineKeyboardButton(get_json_text("buttons_text", 'crypto_pay_button', user_id), callback_data="crypto")
    other = InlineKeyboardButton(get_json_text("buttons_text", 'other_button', user_id), callback_data="other")

    choose_p2p_paytype = InlineKeyboardMarkup().row(bank_transfer, online_wallet).row(world_transfer, crypto).row(other)
    return choose_p2p_paytype


def pay_type_order(user_id):
    bank_transfer_order = InlineKeyboardButton(get_json_text("buttons_text", 'bank_button', user_id),
                                               callback_data="bank_order")
    online_wallet_order = InlineKeyboardButton(get_json_text("buttons_text", 'online_wallet_button', user_id),
                                               callback_data="online_wallet_order")
    world_transfer_order = InlineKeyboardButton(get_json_text("buttons_text", 'world_button', user_id),
                                                callback_data="world_order")
    crypto_order = InlineKeyboardButton(get_json_text("buttons_text", 'crypto_pay_button', user_id),
                                        callback_data="crypto_order")
    other_order = InlineKeyboardButton(get_json_text("buttons_text", 'other_button', user_id),
                                       callback_data="other_order")

    choose_p2p_paytype_order = InlineKeyboardMarkup().row(bank_transfer_order, online_wallet_order).row(
        world_transfer_order, crypto_order).row(other_order)
    return choose_p2p_paytype_order


def start_exthenge(order_id, user_id):
    start_exthenge_button = InlineKeyboardButton(get_json_text("buttons_text", 'start_extch_button', user_id),
                                                 callback_data=order_id)
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
        pay_methods_board.row(InlineKeyboardButton(i, callback_data=f"pay_{i}_order"))
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
    my_ads_board.row(InlineKeyboardButton(f"➕ {get_json_text('buttons_text', 'new_add_button', user_id)}",
                                          callback_data='add_new_ad'))
    return my_ads_board


def show_ads_to_create_order_board(user_id):
    ads_to_order_board = InlineKeyboardMarkup()
    data = send_data_to_order(user_id)
    if len(data) == 0:
        ads_to_order_board.row(InlineKeyboardButton(f"{get_json_text('buttons_text', 'not_ads_button', user_id)}",
                                                    callback_data="ads_none"))
    else:
        for i in data:
            if i[4] == "SELL":
                button_text = f"🟢 {i[3]}, {i[1]}, ({i[5]}), {i[2]}"
            else:
                button_text = f"🟥 {i[3]}, {i[1]}, ({i[5]}), {i[2]}"
            ads_to_order_board.row(InlineKeyboardButton(button_text, callback_data=i[0]))
    return ads_to_order_board


def is_paid(order_id, user_id):
    is_paid_board = InlineKeyboardMarkup()
    is_paid_board.row(InlineKeyboardButton(get_json_text('buttons_text', 'is_paid_button', user_id),
                                           callback_data=f"is_paid_taker_{order_id}"))
    return is_paid_board


def is_paid_maker(order_id, user_id):
    is_paid_board = InlineKeyboardMarkup()
    is_paid_board.row(InlineKeyboardButton(get_json_text('buttons_text', 'is_paid_button', user_id),
                                           callback_data=f"is_paid_maker_{order_id}"))
    return is_paid_board


def confirm_paid_from_maker(order_id, user_id):
    confirm_paid_board = InlineKeyboardMarkup()
    confirm_paid_board.row(InlineKeyboardButton(get_json_text('buttons_text', 'get_paid_button', user_id),
                                                callback_data=f"paid_confirm_{order_id}"))
    return confirm_paid_board


def confirm_paid_from_taker(order_id, user_id):
    confirm_paid_board = InlineKeyboardMarkup()
    confirm_paid_board.row(InlineKeyboardButton(get_json_text('buttons_text', 'get_paid_button', user_id),
                                                callback_data=f"paid_confirm_taker_{order_id}"))
    return confirm_paid_board


def confirm_requisites_buttons(order_id, requisit, amount):
    confirm_requisites_board = InlineKeyboardMarkup()
    confirm_requisites_board.row(InlineKeyboardButton("✅", callback_data=f"req_done_{requisit}_{amount}_{order_id}"),
                                 InlineKeyboardButton("❌", callback_data=f"req_fail_{order_id}"))
    return confirm_requisites_board


def my_ad_settings(ad_id, user_id):
    settings_ad_board = InlineKeyboardMarkup()
    new_limit = InlineKeyboardButton(f"📐 {get_json_text('buttons_text', 'edit_limit_button', user_id)}",
                                     callback_data=f"new_limit_{ad_id}")
    new_price = InlineKeyboardButton(f"💵 {get_json_text('buttons_text', 'edit_price_button', user_id)}",
                                     callback_data=f"new_price_{ad_id}")
    new_description = InlineKeyboardButton(f"📋 {get_json_text('buttons_text', 'edit_description_button', user_id)}",
                                           callback_data=f"new_description_{ad_id}")
    new_requisites = InlineKeyboardButton(f"💸 {get_json_text('buttons_text', 'edit_requisites_button', user_id)}",
                                          callback_data=f"new_requisites_{ad_id}")
    if str(get_ad_status(ad_id)) == "1":
        status_button = InlineKeyboardButton(f"🟢 {get_json_text('buttons_text', 'off_button', user_id)}",
                                             callback_data=f"off_{ad_id}")
    else:
        status_button = InlineKeyboardButton(f"🟥 {get_json_text('buttons_text', 'on_button', user_id)}",
                                             callback_data=f"on_{ad_id}")
    delete_ad = InlineKeyboardButton(f"🗑 {get_json_text('buttons_text', 'delete_button', user_id)}",
                                     callback_data=f"delete_{ad_id}")
    exit_button = InlineKeyboardButton(f"❌ {get_json_text('buttons_text', 'exit_from_edit_button', user_id)}",
                                       callback_data="exit")
    settings_ad_board.row(new_limit, new_price).row(new_description, new_requisites).row(status_button, delete_ad).row(
        exit_button)
    return settings_ad_board
