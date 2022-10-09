from aiogram.dispatcher.filters.state import StatesGroup, State


class Check_hash_btc(StatesGroup):
    user_hash_btc = State()

class Check_hash_usdt(StatesGroup):
    user_hash_usdt = State()

class Check_hash_xmr(StatesGroup):
    user_hash_xmr = State()