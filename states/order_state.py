from aiogram.dispatcher.filters.state import StatesGroup, State

class Order(StatesGroup):
    get_order_id = State()
    get_amount = State()
    get_requisites = State()
