from config.config import TOKEN, support_acount
from config.addreses import BTC_address, USDT_address, XMR_address

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from adminpanel.admins import admins

from keyboards.mainboard import mainboard
from keyboards.p2p_board import p2p_base_board
from keyboards.balance_board import balance_base_board, take_off_crypto_board, take_on_crypro_board, board_success_btc, \
    board_success_usdt, board_success_xmr
from keyboards.settings_board import settings_board
from keyboards.fiat_board import fiat_board
from keyboards.p2p_board import show_ads_board, buy_or_sell_board, choose_p2p_crypto_board, choose_p2p_paytype, \
    choose_p2p_paymethod, choose_order_paymethod
from keyboards.pay_methods import check_all_data, check_all_data_order
from keyboards.p2p_board import create_order_board, choose_p2p_paytype_order, show_ads_to_create_order_board
from keyboards.p2p_board import start_exthenge, is_paid, confirm_paid_from_maker, confirm_requisites_buttons, \
    is_paid_maker, confirm_paid_from_taker

from database.balancedb import wallet, get_balance, add_btc, add_usdt, add_xmr
from database.check_hash import checker_hash
from database.settingsdb import settings_starts, change_fiat
from database.addb import *
from database.orders import *

from states.hash_state import Check_hash_btc, Check_hash_usdt, Check_hash_xmr
from states.output_crypto import output_btc, output_xmr, output_usdt
from states.ad_state import get_ad_data
from states.order_state import Order

from utils.btcscan import btc_hash_scaner
from utils.tronscan import tron_hash_scaner
from utils.xmrscan import xmr_hash_scaner
from utils.binancegetprice import getprice

import requests

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


# Переход в админку
@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    if message.from_user.id in admins:
        await bot.send_message(message.from_user.id,
                               f"Администратор {message.from_user.id} Добро пожаловать в админ панель!")
        hook = requests.post('http://127.0.0.1:5003/admin')
        await bot.send_message(message.from_user.id, f"{hook.text}")


# Старт бота
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    settings_starts(message.from_user.id)
    await message.reply(
        "Привет!\n\nВ этом боте вы сомжете совершать сделки с людьми, а бот выступит в качестве гаранта.",
        reply_markup=mainboard)


# Ввод или вывод валюты
@dp.callback_query_handler(text=["take_on", "take_off"])
async def balance(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == "take_on":
        await bot.send_message(callback.from_user.id, "Выберете валюту для ввода:", reply_markup=take_on_crypro_board)

    elif callback.data == "take_off":
        await bot.send_message(callback.from_user.id, "Выберете валюту для вывода:", reply_markup=take_off_crypto_board)


# Выбор крипты для ввода
@dp.callback_query_handler(text=['btc_on', 'btc_off', 'usdt_on', 'usdt_off', 'xmr_on', 'xmr_off'])
async def balance_change(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == "btc_on":
        await bot.send_message(callback.from_user.id, f"Отправьте BTC на этот адрес <code>{BTC_address}</code>",
                               parse_mode=types.ParseMode.HTML, reply_markup=board_success_btc)
    elif callback.data == "usdt_on":
        await bot.send_message(callback.from_user.id, f"Отправьте USDT на этот адрес <code>{USDT_address}</code>",
                               parse_mode=types.ParseMode.HTML, reply_markup=board_success_usdt)
    elif callback.data == "xmr_on":
        await bot.send_message(callback.from_user.id, f"Отправьте XMR на этот адрес <code>{XMR_address}</code>",
                               parse_mode=types.ParseMode.HTML, reply_markup=board_success_xmr)
    elif callback.data == "btc_off":
        btc_output_balance = get_balance(callback.from_user.id)[0]
        await bot.send_message(callback.from_user.id,
                               f"{btc_output_balance} BTC доступно для вывода\n\nВведите адресс на который будут отправлены BTC: ")
        await output_btc.send_to.set()
    elif callback.data == "usdt_off":
        usdt_output_balance = get_balance(callback.from_user.id)[1]
        await bot.send_message(callback.from_user.id,
                               f"{usdt_output_balance} USDT доступно для вывода\n\nВведите адресс на который будут отправлены USDT:")
        await output_usdt.send_to.set()
    elif callback.data == "xmr_off":
        xmr_output_balance = get_balance(callback.from_user.id)[2]
        await bot.send_message(callback.from_user.id,
                               f"{xmr_output_balance} XMR доступно для вывода\n\nВведите адресс на который будут отправлены XMR:")
        await output_xmr.send_to.set()


# Начала блока состояний для указания сумы отправки и адреса отправки
@dp.message_handler(state=output_btc.send_to)
async def btc_send_address(message: types.Message, state: FSMContext):
    await state.update_data(btc_address=message.text)
    await message.answer("Введите сумму отправки: ")
    await output_btc.next()


@dp.message_handler(state=output_btc.amount)
async def btc_send_amount(message: types.Message, state: FSMContext):
    await state.update_data(amount_send=message.text)
    data = await state.get_data()
    if float(data['amount_send']) > float(get_balance(message.from_user.id)[0]):
        await bot.send_message(message.from_user.id, "❌ Недостаточно средств для перевода")
    else:
        await bot.send_message(-748498807,
                               f"Адрес вывода BTC: <code>{data['btc_address']}</code>\n\nСумма к отправке: <code>{data['amount_send']}</code>\n\nПользователь: {message.from_user.id}",
                               parse_mode=types.ParseMode.HTML)
        add_btc(message.from_user.id, -float(data['amount_send']))
        await bot.send_message(message.from_user.id, "Скоро средства поступят на кошелек")
    await state.finish()


@dp.message_handler(state=output_usdt.send_to)
async def usdt_send_address(message: types.Message, state: FSMContext):
    await state.update_data(usdt_address=message.text)
    await message.answer("Введите сумму отправки: ")
    await output_usdt.next()


@dp.message_handler(state=output_usdt.amount)
async def usdt_send_amount(message: types.Message, state: FSMContext):
    await state.update_data(amount_send=message.text)
    data = await state.get_data()
    if float(data['amount_send']) > float(get_balance(message.from_user.id)[1]):
        await bot.send_message(message.from_user.id, "❌ Недостаточно средств для перевода")
    else:
        await bot.send_message(-748498807,
                               f"Адрес вывода USDT: <code>{data['usdt_address']}</code>\n\nСумма к отправке: <code>{data['amount_send']}</code>\n\nПользователь: {message.from_user.id}",
                               parse_mode=types.ParseMode.HTML)
        add_usdt(message.from_user.id, -float(data['amount_send']))
        await bot.send_message(message.from_user.id, "Скоро средства поступят на кошелек")
    await state.finish()


@dp.message_handler(state=output_xmr.send_to)
async def xmr_send_address(message: types.Message, state: FSMContext):
    await state.update_data(xmr_address=message.text)
    await message.answer("Введите сумму отправки: ")
    await output_xmr.next()


@dp.message_handler(state=output_xmr.amount)
async def xmr_send_amount(message: types.Message, state: FSMContext):
    await state.update_data(amount_send=message.text)
    data = await state.get_data()
    if float(data['amount_send']) > float(get_balance(message.from_user.id)[2]):
        await bot.send_message(message.from_user.id, "❌ Недостаточно средств для перевода")
    else:
        await bot.send_message(-748498807,
                               f"Адрес вывода XMR: <code>{data['xmr_address']}</code>\n\nСумма к отправке: <code>{data['amount_send']}</code>\n\nПользователь: {message.from_user.id}",
                               parse_mode=types.ParseMode.HTML)
        add_xmr(message.from_user.id, -float(data['amount_send']))
        await bot.send_message(message.from_user.id, "Скоро средства поступят на кошелек")
    await state.finish()


# Конец блока состояний для указания сумы отправки и адреса отправки


# Проверка hash транзакции
@dp.callback_query_handler(text=["btc_success", "usdt_success", "xmr_success"])
async def check_hash(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == "btc_success":
        await bot.send_message(callback.from_user.id, "Отправьте пожалуйста hash для проверки")
        await Check_hash_btc.user_hash_btc.set()
    if callback.data == "usdt_success":
        await bot.send_message(callback.from_user.id, "Отправьте пожалуйста hash для проверки")
        await Check_hash_usdt.user_hash_usdt.set()
    if callback.data == "xmr_success":
        await bot.send_message(callback.from_user.id, "Отправьте пожалуйста hash для проверки")
        await Check_hash_xmr.user_hash_xmr.set()


# Блок зачисления крипты на счет пользователя
@dp.message_handler(state=Check_hash_btc.user_hash_btc)
async def get_btc_hash(message: types.Message, state: FSMContext):
    await state.update_data(hash=message.text)
    data = await state.get_data()
    hash = data['hash']
    await state.finish()
    checker = checker_hash(hash, int(message.from_user.id))

    if checker:
        amount = btc_hash_scaner(hash, BTC_address)
        if not amount:
            await bot.send_message(message.from_user.id, "Вы используете неккоректный hash")
        else:
            await bot.send_message(message.from_user.id, f"Скоро {amount} BTC будут зачислены на ваш счет")
            add_btc(message.from_user.id, amount)
            await bot.send_message(message.from_user.id, "Проверьте свой баланс")
    else:
        await bot.send_message(message.from_user.id, "Вы пытаетесь использовать hash повторно")


@dp.message_handler(state=Check_hash_usdt.user_hash_usdt)
async def get_usdt_hash(message: types.Message, state: FSMContext):
    await state.update_data(hash=message.text)
    data = await state.get_data()
    hash = data['hash']
    await state.finish()
    checker = checker_hash(hash, int(message.from_user.id))
    if checker:
        amount = tron_hash_scaner(hash, USDT_address)
        if not amount:
            await bot.send_message(message.from_user.id, "Вы используете неккоректный hash")
        else:
            await bot.send_message(message.from_user.id, f"Скоро {amount} USDT будут зачислены на ваш счет")
            add_usdt(message.from_user.id, amount)
            await bot.send_message(message.from_user.id, "Проверьте свой баланс")

    else:
        await bot.send_message(message.from_user.id, "Вы пытаетесь использовать hash повторно")


@dp.message_handler(state=Check_hash_xmr.user_hash_xmr)
async def get_xmr_hash(message: types.Message, state: FSMContext):
    await state.update_data(hash=message.text)
    data = await state.get_data()
    hash = data['hash']
    await state.finish()
    checker = checker_hash(hash, int(message.from_user.id))

    if checker:
        amount = xmr_hash_scaner(hash)
        if not amount:
            await bot.send_message(message.from_user.id, "Вы используете неккоректный hash")
        else:
            await bot.send_message(message.from_user.id, f"Скоро {amount} XMR будут зачислены на ваш счет")
            add_xmr(message.from_user.id, amount)
            await bot.send_message(message.from_user.id, "Проверьте свой баланс")
    else:
        await bot.send_message(message.from_user.id, "Вы пытаетесь использовать hash повторно")


# Конец блока зачисления крипты на счет пользователя


# Вывод объявлений и добавление новых
@dp.callback_query_handler(text=['ad'])
async def p2p_board_ad(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == 'ad':
        await bot.send_message(callback.from_user.id, "Здесь находятся все ваши объявления",
                               reply_markup=show_ads_board(callback.from_user.id))


# Блок добавления объявления
@dp.callback_query_handler(text=['add_new_ad'])
async def p2p_add_new_ad(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == 'add_new_ad':
        creationad(callback.from_user.id)
        await bot.send_message(callback.from_user.id, "Выберете тип объявления", reply_markup=buy_or_sell_board)


@dp.callback_query_handler(text=["create_buy_ad", "create_sell_ad", "back_to"])
async def p2p_choose_type(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == "create_buy_ad":
        update_adtype(callback.from_user.id, "BUY")
        await bot.send_message(callback.from_user.id, "Выбор криптовалюты", reply_markup=choose_p2p_crypto_board)
    elif callback.data == "create_sell_ad":
        update_adtype(callback.from_user.id, "SELL")
        await bot.send_message(callback.from_user.id, "Выбор криптовалюты", reply_markup=choose_p2p_crypto_board)
    elif callback.data == "back_to":
        await bot.send_message(callback.from_user.id, "Здесь находятся все ваши объявления",
                               reply_markup=show_ads_board(callback.from_user.id))


@dp.callback_query_handler(text=["BTC", "USDT", "XMR"])
async def p2p_choose_crypto(callback: types.CallbackQuery):
    await callback.message.delete()
    update_adcrypto(callback.from_user.id, callback.data)
    update_fiat(callback.from_user.id)
    await bot.send_message(callback.from_user.id, "Выбор способа оплаты", reply_markup=choose_p2p_paytype)


@dp.callback_query_handler(text=["other", "crypto", "world", "online_wallet", "bank"])
async def p2p_choose_paytype(callback: types.CallbackQuery):
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, "Выбор метода оплаты",
                           reply_markup=choose_p2p_paymethod(check_fiat(callback.from_user.id)[0], callback.data))


@dp.callback_query_handler(text=check_all_data())
async def p2p_choose_methods(callback: types.CallbackQuery):
    await callback.message.delete()
    update_pay_method(callback.from_user.id, callback.data)
    await bot.send_message(callback.from_user.id, "Напишите реквизиты для получения/отправки оплаты",
                           reply_markup=types.ReplyKeyboardRemove())
    await get_ad_data.get_requisites.set()


@dp.message_handler(state=get_ad_data.get_requisites)
async def p2p_get_requisites(message: types.Message, state: FSMContext):
    await state.update_data(requisites=message.text)
    await bot.send_message(message.from_user.id, "Укажите количество криптовалюты")
    await get_ad_data.next()


@dp.message_handler(state=get_ad_data.get_limits)
async def p2p_get_limits(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    update_price(message.from_user.id, message.text)
    limit = float(check_amount(message.from_user.id)[0]) * float(check_price(message.from_user.id)[0])
    if check_ad_type(message.from_user.id)[0] == "SELL":
        await bot.send_message(message.from_user.id, f"Укажите лимиты\nДоступно: 1-{limit}")
    else:
        await bot.send_message(message.from_user.id, f"Укажите лимиты\nПример: 1-1000")
    await get_ad_data.next()


@dp.message_handler(state=get_ad_data.get_amount)
async def p2p_get_amount(message: types.Message, state: FSMContext):
    if check_crypto_balance(message.from_user.id)[0] == "BTC":
        balance = get_balance(message.from_user.id)[0]
    elif check_crypto_balance(message.from_user.id)[0] == "USDT":
        balance = get_balance(message.from_user.id)[1]
    elif check_crypto_balance(message.from_user.id)[0] == "XMR":
        balance = get_balance(message.from_user.id)[2]
    if float(balance) < float(message.text) and check_ad_type(message.from_user.id)[0] == "SELL":
        await bot.send_message(message.from_user.id, "На вашем балансе не достаточно криптовалюты")
        await get_ad_data.get_amount.set()
    else:
        await state.update_data(amount=message.text)
        update_amount(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, "Укажите цену (1% от суммы сделки в криптовалюте забирает сервис)")
        await get_ad_data.next()


@dp.message_handler(state=get_ad_data.get_price)
async def p2p_get_price(message: types.Message, state: FSMContext):
    global limit1
    try:
        limit1 = float(message.text.split("-")[1])
    except:
        await bot.send_message(message.from_user.id, "Лимиты указаны некоректно", reply_markup=mainboard)
        await state.finish()
    limit = float(check_amount(message.from_user.id)[0]) * float(check_price(message.from_user.id)[0])
    if limit1 > limit and check_ad_type(message.from_user.id)[0] == "SELL":
        await bot.send_message(message.from_user.id, "Выставленные лимиты превышают допустимое значение",
                               reply_markup=mainboard)
        await state.finish()
    else:
        await state.update_data(limits=message.text)
        data = await state.get_data()
        await state.finish()
        update_requisites(message.from_user.id, data["requisites"])
        update_limits(message.from_user.id, data["limits"])
        update_price(message.from_user.id, data["price"])
        update_amount(message.from_user.id, data["amount"])
        new_ad(message.from_user.id)
        await bot.send_message(message.from_user.id, "Объявление создано!", reply_markup=mainboard)


# Конец блока создания объявлений


# Блок взаимодействия пользователей
@dp.callback_query_handler(text=['buy', 'sell'])
async def start_p2p_extend(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == 'buy':
        set_order_ad_type(callback.from_user.id, "SELL")
        await bot.send_message(callback.from_user.id, "Выберете криптовалюту", reply_markup=create_order_board)
    elif callback.data == 'sell':
        set_order_ad_type(callback.from_user.id, "BUY")
        await bot.send_message(callback.from_user.id, "Выберете криптовалюту", reply_markup=create_order_board)


@dp.callback_query_handler(text=["btc_order", "usdt_order", "xmr_order"])
async def set_p2p_crypro_and_fiat(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == "btc_order":
        set_order_crypto(callback.from_user.id, "BTC")
        set_order_fiat(callback.from_user.id, check_fiat(callback.from_user.id)[0])
        await bot.send_message(callback.from_user.id, "Выбор типа оплаты: ", reply_markup=choose_p2p_paytype_order)
    elif callback.data == "usdt_order":
        set_order_crypto(callback.from_user.id, "USDT")
        set_order_fiat(callback.from_user.id, check_fiat(callback.from_user.id)[0])
        await bot.send_message(callback.from_user.id, "Выбор типа оплаты: ", reply_markup=choose_p2p_paytype_order)
    elif callback.data == "xmr_order":
        set_order_crypto(callback.from_user.id, "XMR")
        set_order_fiat(callback.from_user.id, check_fiat(callback.from_user.id)[0])
        await bot.send_message(callback.from_user.id, "Выбор типа оплаты: ", reply_markup=choose_p2p_paytype_order)


@dp.callback_query_handler(text=["other_order", "crypto_order", "world_order", "online_wallet_order", "bank_order"])
async def set_p2p_paytype(callback: types.CallbackQuery):
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, "Выбор метода оплаты",
                           reply_markup=choose_order_paymethod(check_fiat(callback.from_user.id)[0], callback.data))


@dp.callback_query_handler(text=check_all_data_order())
async def set_p2p_pay_method(callback: types.CallbackQuery):
    await callback.message.delete()
    set_order_paymethod(callback.from_user.id, callback.data.split("_")[0])
    await bot.send_message(callback.from_user.id, "Выберите объявление",
                           reply_markup=show_ads_to_create_order_board(callback.from_user.id))


@dp.callback_query_handler(Text(startswith="ad_"))
async def choose_ad_and_exchange(callback: types.CallbackQuery):
    await callback.message.delete()
    data = get_ad_data_order(callback.data)
    text = f"Объявление ID: {callback.data}\n\nЦена: {data[0]}\n\nКриптовалюта: {data[2]}\n\n Метод оплаты: {data[1]}\n\n Пользователь: user{data[3]}"
    order = start_order(callback.from_user.id, data[3], callback.data)
    await bot.send_message(callback.from_user.id, text, reply_markup=start_exthenge(order))
    await Order.get_order_id.set()


@dp.callback_query_handler(Text(startswith="order_"), state=Order.get_order_id)
async def new_order_start(callback: types.CallbackQuery, state: FSMContext):
    get_ad = get_ad_id(callback.data)
    get_limits = check_limits_order(get_ad)
    await bot.send_message(callback.from_user.id, f"Укажите сумму покупки\nЛимиты: {get_limits}")
    await state.update_data(order_id=callback.data)
    await state.update_data(main_limit=get_limits)
    await Order.next()


@dp.message_handler(state=Order.get_amount)
async def get_order_user_limits(message: types.Message, state: FSMContext):
    await state.update_data(user_amount=message.text)
    data = await state.get_data()
    if float(data["user_amount"]) < float(data["main_limit"].split("-")[0]) or float(data["user_amount"]) > float(
            data["main_limit"].split("-")[1]):
        await bot.send_message(message.from_user.id, "Выход за пределы лимитов\n\nУкажите лимиты заново")
        await Order.get_amount.set()
    else:
        get_ad = get_ad_id(data["order_id"])
        get_ad_type = check_ad_type_order(get_ad)
        if get_ad_type == "BUY":
            crypto = check_crypto_order(get_ad)
            price = check_price_to_order(get_ad)
            if crypto == "BTC":
                is_balance = get_balance(message.from_user.id)[0]
            elif crypto == "USDT":
                is_balance = get_balance(message.from_user.id)[1]
            elif crypto == "XMR":
                is_balance = get_balance(message.from_user.id)[2]
            if float(is_balance) * float(price) < float(data["user_amount"]):
                await bot.send_message(message.from_user.id,
                                       f"Внимание!\nНедостаточно средств\nДоступно: {round(float(is_balance) * float(price), 1)}")
            else:
                set_order_amount(data["order_id"], data['user_amount'])
                await bot.send_message(message.from_user.id, "Отправьте реквизиты для получения оплаты")
                await Order.get_requisites.set()
            # await bot.send_message(message.from_user.id, "Пожалуйста, введите реквизиты")
            # await Order.get_requisites.set()
        else:
            get_requisites = check_requsites_order(get_ad)
            maker = get_maker_and_taker(data["order_id"])[0]
            set_order_amount(data["order_id"], data['user_amount'])
            await bot.send_message(message.from_user.id, f"Отправьте {data['user_amount']} на {get_requisites}",
                                   reply_markup=is_paid(data['order_id']))
            await bot.send_message(maker,
                                   f"Ожидайте получения оплаты от {message.from_user.id}\nСумма: {data['user_amount']}")
            await state.finish()


@dp.message_handler(state=Order.get_requisites)
async def get_order_requisites(message: types.Message, state: FSMContext):
    await state.update_data(taker_requisites=message.text)
    data = await state.get_data()
    await bot.send_message(message.from_user.id, f"Верно ли указаны реквизиты: {data['taker_requisites']}",
                           reply_markup=confirm_requisites_buttons(data["order_id"], data["taker_requisites"],
                                                                   data["user_amount"]))
    await state.finish()


@dp.callback_query_handler(Text(startswith="req_done_"))
async def confirm_requisites(callback: types.CallbackQuery):
    requisit = callback.data.split("req_done_")[1].split("_")[0]
    maker = get_maker_and_taker(
        callback.data.split("req_done_")[1].split("_")[2] + "_" + callback.data.split("req_done_")[1].split("_")[3])[0]
    amount = callback.data.split("req_done_")[1].split("_")[1]
    await bot.send_message(maker, f"Новый заказ от user{callback.from_user.id}\n\n Отправьте {amount} на {requisit}",
                           reply_markup=is_paid_maker(callback.data.split("req_done_")[1].split("_")[2] + "_" +
                                                      callback.data.split("req_done_")[1].split("_")[3]))
    await bot.send_message(callback.from_user.id, f"Ожидайте оплату")


@dp.callback_query_handler(Text(startswith="is_paid_maker_"))
async def confirm_paid_taker(callback: types.CallbackQuery):
    taker = get_maker_and_taker(callback.data.split("is_paid_maker_")[1])[1]
    await bot.send_message(taker, f"Заказ отмечен как оплаченый", reply_markup=confirm_paid_from_taker(callback.data.split("is_paid_maker_")[1]))

@dp.callback_query_handler(Text(startswith="paid_confirm_taker_"))
async def withdraw_to_taker(callback: types.CallbackQuery):
    maker = get_maker_and_taker(callback.data.split("paid_confirm_taker_")[1])[0]
    taker = get_maker_and_taker(callback.data.split("paid_confirm_taker_")[1])[1]
    amount = get_order_amount(callback.data.split("paid_confirm_taker_")[1])
    get_ad = get_ad_id(callback.data.split("paid_confirm_taker_")[1])
    crypto = check_crypto_order(get_ad)
    price = check_price_to_order(get_ad)
    to_withdraw = float(amount) / float(price)
    if crypto == "BTC":
        add_btc(maker, to_withdraw)
        add_btc(taker, -to_withdraw)
    elif crypto == "USDT":
        add_usdt(maker, to_withdraw)
        add_usdt(taker, -to_withdraw)
    elif crypto == "XMR":
        add_xmr(maker, to_withdraw)
        add_xmr(taker, -to_withdraw)
    await bot.send_message(taker, f"С вашего {crypto} кошелька выведено {to_withdraw} {crypto}")
    await bot.send_message(maker, f"На ваш {crypto} кошелек поступило {to_withdraw} {crypto}")

@dp.callback_query_handler(Text(startswith="req_fail_"))
async def unconfirm_requisites(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, "Создание оредра остановлено")


@dp.callback_query_handler(Text(startswith="is_paid_taker_"))
async def confirm_paid_maker(callback: types.CallbackQuery):
    maker = get_maker_and_taker(callback.data.split("is_paid_taker_")[1])[0]
    await bot.send_message(maker, f"Заказ от {callback.from_user.id} отмечен как оплаченый",
                           reply_markup=confirm_paid_from_maker(callback.data.split("is_paid_taker_")[1]))
    await bot.send_message(callback.from_user.id, "Ожидайте зачисления средств на ваш счет")


@dp.callback_query_handler(Text(startswith="paid_confirm_"))
async def withdraw_to_taker(callback: types.CallbackQuery):
    maker = get_maker_and_taker(callback.data.split("paid_confirm_")[1])[0]
    taker = get_maker_and_taker(callback.data.split("paid_confirm_")[1])[1]
    amount = get_order_amount(callback.data.split("paid_confirm_")[1])
    get_ad = get_ad_id(callback.data.split("paid_confirm_")[1])
    crypto = check_crypto_order(get_ad)
    price = check_price_to_order(get_ad)
    to_withdraw = float(amount) / float(price)
    if crypto == "BTC":
        add_btc(maker, -to_withdraw)
        add_btc(taker, to_withdraw)
    elif crypto == "USDT":
        add_usdt(maker, -to_withdraw)
        add_usdt(taker, to_withdraw)
    elif crypto == "XMR":
        add_xmr(maker, -to_withdraw)
        add_xmr(taker, to_withdraw)
    await bot.send_message(maker, f"С вашего {crypto} кошелька выведено {to_withdraw} {crypto}")
    await bot.send_message(taker, f"На ваш {crypto} кошелек поступило {to_withdraw} {crypto}")


# Настройки
@dp.callback_query_handler(text=['lang', 'fiat'])
async def settings(callback: types.CallbackQuery):
    if callback.data == 'fiat':
        await bot.send_message(callback.from_user.id, "Фиат доступный на данный момент: ", reply_markup=fiat_board)


# Смена валюты
@dp.callback_query_handler(text=['USD', 'KZT', 'UAH', 'CNY', 'VND', 'BRL', 'IRR', 'RUB', 'TRY', 'AED', 'SAR', 'EGP'])
async def choose_fiat(callback: types.CallbackQuery):
    fiats = ['USD', 'KZT', 'UAH', 'CNY', 'VND', 'BRL', 'IRR', 'RUB', 'TRY', 'AED', 'SAR', 'EGP']
    if callback.data in fiats:
        change_fiat(callback.from_user.id, callback.data)
        fiat = check_fiat(callback.from_user.id)
        await bot.send_message(callback.from_user.id, f"Настройки изменены {fiat[0]}")


@dp.message_handler()
async def speak(msg: types.Message):
    if msg.text == '🔄 P2P Обмен':
        await bot.send_message(msg.from_user.id,
                               "В этом разаделе вы можете соверишить p2p сделку, а бот выступит в качестве гаранта.",
                               reply_markup=p2p_base_board)
        search_order(msg.from_user.id)
    elif msg.text == '💰 Баланс':
        wallet_creat = wallet(msg.from_user.id)
        if wallet_creat == "Success":
            await bot.send_message(msg.from_user.id, f"Создан новый кошелек для пользователя {msg.from_user.id}")
        else:
            await bot.send_message(msg.from_user.id, "Отлично! У вас уже есть кошелек")
        balances = get_balance(msg.from_user.id)
        fiat = check_fiat(msg.from_user.id)
        btc_to_fiat = getprice("BTC", fiat[0]) * balances[0]
        usdt_to_fiat = getprice("USDT", fiat[0]) * balances[1]
        xmr_to_fiat = getprice("XMR", fiat[0]) * balances[2]
        overall_balance = btc_to_fiat + usdt_to_fiat + xmr_to_fiat
        await bot.send_message(msg.from_user.id,
                               f"Общий баланс ≈ {overall_balance} {fiat[0]}\n{balances[0]} BTC ≈ {btc_to_fiat}\n{balances[1]} USDT(TRC20) ≈ {usdt_to_fiat}\n{balances[2]} XMR ≈ {xmr_to_fiat}",
                               reply_markup=balance_base_board)
    elif msg.text == '⚙ Настройки':
        user = msg.from_user.id
        await bot.send_message(msg.from_user.id, f"Настройки пользователя /{user}", reply_markup=settings_board)
    elif msg.text == '🚨 Поддержка':
        await bot.send_message(msg.from_user.id,
                               f"Если у вас возникли проблемы или вопросы вы можете связаться с поддержкой\n\n Аккаунт поддрежки: {support_acount}")
    elif msg.text == '📌 FAQ':
        await bot.send_message(msg.from_user.id, "FAQ: Полное и подробное руководство по работе с системой.")
    else:
        await bot.send_message(msg.from_user.id, "Извините, но я вас не понимаю")


if __name__ == '__main__':
    executor.start_polling(dp)
