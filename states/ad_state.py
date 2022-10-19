from aiogram.dispatcher.filters.state import StatesGroup, State


class get_ad_data(StatesGroup):
    get_requisites = State()
    get_amount = State()
    get_limits = State()
    get_price = State()

class get_ad_data_repleace(StatesGroup):
    get_ad_id = State()
    get_new_limits = State()