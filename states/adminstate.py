from aiogram.dispatcher.filters.state import StatesGroup, State


class new_admin(StatesGroup):
    get_id = State()


class new_pay_mehod(StatesGroup):
    get_admin_fiat = State()
    get_admin_methods = State()
    get_admin_method = State()


class withdraw_btc(StatesGroup):
    get_amount = State()


class withdraw_usdt(StatesGroup):
    get_amount = State()


class withdraw_xmr(StatesGroup):
    get_amount = State()
