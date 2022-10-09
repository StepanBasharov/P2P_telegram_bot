from aiogram.dispatcher.filters.state import StatesGroup, State

class output_btc(StatesGroup):
    send_to = State()
    amount = State()

class output_usdt(StatesGroup):
    send_to = State()
    amount = State()

class output_xmr(StatesGroup):
    send_to = State()
    amount = State()
