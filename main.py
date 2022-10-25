from config.config import TOKEN, support_acount
from config.addreses import BTC_address, USDT_address, XMR_address

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.mainboard import show_mainboard
from keyboards.p2p_board import main_p2p_il_board
from keyboards.balance_board import take_off_on, take_off_crypto_board, take_on_crypro_board, btc_is_send, \
    usdt_is_send, xmr_is_send
from keyboards.settings_board import settings_board
from keyboards.fiat_board import fiat_board
from keyboards.p2p_board import show_ads_board, choose_type_board, choose_p2p_crypto_board, pay_type, \
    choose_p2p_paymethod, choose_order_paymethod, back_to_button
from keyboards.pay_methods import check_all_data, add_methods_to_json
from keyboards.p2p_board import create_order_board, pay_type_order, show_ads_to_create_order_board
from keyboards.p2p_board import start_exthenge, is_paid, confirm_paid_from_maker, confirm_requisites_buttons, \
    is_paid_maker, confirm_paid_from_taker, my_ad_settings
from keyboards.admin_board import admin_board, cancel_board
from keyboards.lang_board import lang_board

from database.balancedb import wallet, get_balance, add_btc, add_usdt, add_xmr
from database.check_hash import checker_hash
from database.settingsdb import settings_starts, change_fiat
from database.addb import *
from database.orders import *
from database.admindb import *
from database.settingsdb import change_lang

from states.hash_state import Check_hash_btc, Check_hash_usdt, Check_hash_xmr
from states.output_crypto import output_btc, output_xmr, output_usdt
from states.ad_state import get_ad_data, get_ad_data_repleace
from states.order_state import Order
from states.adminstate import new_admin, new_pay_mehod, withdraw_xmr, withdraw_usdt, withdraw_btc

from utils.btcscan import btc_hash_scaner
from utils.tronscan import tron_hash_scaner
from utils.xmrscan import xmr_hash_scaner
from utils.binancegetprice import getprice

from handless.translater import get_json_text

import requests

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


# Переход в админку
@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    if is_admin(message.from_user.id) == True:
        balance = show_admin_balance()
        await bot.send_message(message.from_user.id,
                               f"Администратор {message.from_user.id} Добро пожаловать в админ панель!\nBTC = {balance[0]}\nUSDT = {balance[1]}\nXMR = {balance[2]}",
                               reply_markup=admin_board)


# Старт бота
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    settings_starts(message.from_user.id)
    await message.reply(
        get_json_text("bot_text", "hello", message.from_user.id),
        reply_markup=show_mainboard(message.from_user.id))


# Ввод или вывод валюты
@dp.callback_query_handler(text=["take_on", "take_off"])
async def balance(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == "take_on":
        await bot.send_message(callback.from_user.id,
                               get_json_text("bot_text", "currency_input", callback.from_user.id),
                               reply_markup=take_on_crypro_board)

    elif callback.data == "take_off":
        await bot.send_message(callback.from_user.id,
                               get_json_text("bot_text", "currency_output", callback.from_user.id),
                               reply_markup=take_off_crypto_board)


# Выбор крипты для ввода
@dp.callback_query_handler(text=['btc_on', 'btc_off', 'usdt_on', 'usdt_off', 'xmr_on', 'xmr_off'])
async def balance_change(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == "btc_on":
        await bot.send_message(callback.from_user.id,
                               f"{get_json_text('bot_text', 'send_btc_to', callback.from_user.id)} <code>{BTC_address}</code>",
                               parse_mode=types.ParseMode.HTML, reply_markup=btc_is_send(callback.from_user.id))
    elif callback.data == "usdt_on":
        await bot.send_message(callback.from_user.id,
                               f"{get_json_text('bot_text', 'send_usdt_to', callback.from_user.id)} <code>{USDT_address}</code>",
                               parse_mode=types.ParseMode.HTML, reply_markup=usdt_is_send(callback.from_user.id))
    elif callback.data == "xmr_on":
        await bot.send_message(callback.from_user.id,
                               f"{get_json_text('bot_text', 'send_xmr_to', callback.from_user.id)} <code>{XMR_address}</code>",
                               parse_mode=types.ParseMode.HTML, reply_markup=xmr_is_send(callback.from_user.id))
    elif callback.data == "btc_off":
        btc_output_balance = get_balance(callback.from_user.id)[0]
        await bot.send_message(callback.from_user.id,
                               f"{btc_output_balance} BTC {get_json_text('bot_text', 'avalibal_to_input', callback.from_user.id)} BTC: ", reply_markup=back_to_button(callback.from_user.id))
        await output_btc.send_to.set()
    elif callback.data == "usdt_off":
        usdt_output_balance = get_balance(callback.from_user.id)[1]
        await bot.send_message(callback.from_user.id,
                               f"{usdt_output_balance} USDT {get_json_text('bot_text', 'avalibal_to_input', callback.from_user.id)} USDT:", reply_markup=back_to_button(callback.from_user.id))
        await output_usdt.send_to.set()
    elif callback.data == "xmr_off":
        xmr_output_balance = get_balance(callback.from_user.id)[2]
        await bot.send_message(callback.from_user.id,
                               f"{xmr_output_balance} XMR {get_json_text('bot_text', 'avalibal_to_input', callback.from_user.id)} XMR:", reply_markup=back_to_button(callback.from_user.id))
        await output_xmr.send_to.set()


# Начала блока состояний для указания сумы отправки и адреса отправки
@dp.message_handler(state=output_btc.send_to)
async def btc_send_address(message: types.Message, state: FSMContext):
    if message.text == f"❌ {get_json_text('buttons_text', 'back_to_button', message.from_user.id)}":
        await bot.send_message(message.from_user.id, "❌", reply_markup=show_mainboard(message.from_user.id))
        await state.finish()
    else:
        await state.update_data(btc_address=message.text)
        await bot.send_message(message.from_user.id, get_json_text('bot_text', 'input_sum_to_send', message.from_user.id),
                               reply_markup=back_to_button(message.from_user.id))
        await output_btc.next()


@dp.message_handler(state=output_btc.amount)
async def btc_send_amount(message: types.Message, state: FSMContext):
    fee = 0.00000001
    if float(get_balance(message.from_user.id)[0]) < fee:
        await bot.send_message(message.from_user.id,
                               get_json_text('bot_text', "insufficient_funds", message.from_user.id), reply_markup=show_mainboard(message.from_user.id))
        await state.finish()
    await state.update_data(amount_send=message.text)
    data = await state.get_data()
    if message.text == f"❌ {get_json_text('buttons_text', 'back_to_button', message.from_user.id)}":
        await bot.send_message(message.from_user.id, "❌", reply_markup=show_mainboard(message.from_user.id))
    elif float(data['amount_send']) > float(get_balance(message.from_user.id)[0]):
        await bot.send_message(message.from_user.id,
                               get_json_text('bot_text', "insufficient_funds", message.from_user.id))
    else:
        await bot.send_message(-748498807,
                               f"Адрес вывода BTC: <code>{data['btc_address']}</code>\n\nСумма к отправке: <code>{data['amount_send']}</code>\n\nПользователь: {message.from_user.id}",
                               parse_mode=types.ParseMode.HTML)
        add_btc(message.from_user.id, -float(data['amount_send']))
        await bot.send_message(message.from_user.id,
                               get_json_text("bot_text", "funds_coming_soon", message.from_user.id), reply_markup=show_mainboard(message.from_user.id))
    await state.finish()


@dp.message_handler(state=output_usdt.send_to)
async def usdt_send_address(message: types.Message, state: FSMContext):
    if message.text == f"❌ {get_json_text('buttons_text', 'back_to_button', message.from_user.id)}":
        await bot.send_message(message.from_user.id, "❌", reply_markup=show_mainboard(message.from_user.id))
        await state.finish()
    else:
        await state.update_data(usdt_address=message.text)
        await message.answer(get_json_text('bot_text', 'input_sum_to_send', message.from_user.id))
        await output_usdt.next()


@dp.message_handler(state=output_usdt.amount)
async def usdt_send_amount(message: types.Message, state: FSMContext):
    fee = 1
    if float(get_balance(message.from_user.id)[1]) < fee:
        await bot.send_message(message.from_user.id,
                               get_json_text('bot_text', "insufficient_funds", message.from_user.id), reply_markup=show_mainboard(message.from_user.id))
        await state.finish()
    await state.update_data(amount_send=message.text)
    data = await state.get_data()
    if message.text == f"❌ {get_json_text('buttons_text', 'back_to_button', message.from_user.id)}":
        await bot.send_message(message.from_user.id, "❌", reply_markup=show_mainboard(message.from_user.id))
    elif float(data['amount_send']) > float(get_balance(message.from_user.id)[1]):
        await bot.send_message(message.from_user.id,
                               get_json_text('bot_text', "insufficient_funds", message.from_user.id))
    else:
        await bot.send_message(-748498807,
                               f"Адрес вывода USDT: <code>{data['usdt_address']}</code>\n\nСумма к отправке: <code>{data['amount_send']}</code>\n\nПользователь: {message.from_user.id}",
                               parse_mode=types.ParseMode.HTML)
        add_usdt(message.from_user.id, -float(data['amount_send']))
        await bot.send_message(message.from_user.id,
                               get_json_text("bot_text", "funds_coming_soon", message.from_user.id), reply_markup=show_mainboard(message.from_user.id))
    await state.finish()


@dp.message_handler(state=output_xmr.send_to)
async def xmr_send_address(message: types.Message, state: FSMContext):
    fee = 0.0001
    if float(get_balance(message.from_user.id)[2]) < fee:
        await bot.send_message(message.from_user.id,
                               get_json_text('bot_text', "insufficient_funds", message.from_user.id), reply_markup=show_mainboard(message.from_user.id))
        await state.finish()
    if message.text == f"❌ {get_json_text('buttons_text', 'back_to_button', message.from_user.id)}":
        await bot.send_message(message.from_user.id, "❌", reply_markup=show_mainboard(message.from_user.id))
        await state.finish()
    else:
        await state.update_data(xmr_address=message.text)
        await message.answer(get_json_text('bot_text', 'input_sum_to_send', message.from_user.id))
        await output_xmr.next()


@dp.message_handler(state=output_xmr.amount)
async def xmr_send_amount(message: types.Message, state: FSMContext):
    await state.update_data(amount_send=message.text)
    data = await state.get_data()
    if message.text == f"❌ {get_json_text('buttons_text', 'back_to_button', message.from_user.id)}":
        await bot.send_message(message.from_user.id, "❌", reply_markup=show_mainboard(message.from_user.id))
    elif float(data['amount_send']) > float(get_balance(message.from_user.id)[2]):
        await bot.send_message(message.from_user.id, message.from_user.id,
                               get_json_text('bot_text', "insufficient_funds", message.from_user.id))
    else:
        await bot.send_message(-748498807,
                               f"Адрес вывода XMR: <code>{data['xmr_address']}</code>\n\nСумма к отправке: <code>{data['amount_send']}</code>\n\nПользователь: {message.from_user.id}",
                               parse_mode=types.ParseMode.HTML)
        add_xmr(message.from_user.id, -float(data['amount_send']))
        await bot.send_message(message.from_user.id,
                               get_json_text("bot_text", "funds_coming_soon", message.from_user.id), reply_markup=show_mainboard(message.from_user.id))
    await state.finish()


# Конец блока состояний для указания сумы отправки и адреса отправки


# Проверка hash транзакции
@dp.callback_query_handler(text=["btc_success", "usdt_success", "xmr_success"])
async def check_hash(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == "btc_success":
        await bot.send_message(callback.from_user.id,
                               get_json_text("bot_text", "please_send_hash", callback.from_user.id))
        await Check_hash_btc.user_hash_btc.set()
    if callback.data == "usdt_success":
        await bot.send_message(callback.from_user.id,
                               get_json_text("bot_text", "please_send_hash", callback.from_user.id))
        await Check_hash_usdt.user_hash_usdt.set()
    if callback.data == "xmr_success":
        await bot.send_message(callback.from_user.id,
                               get_json_text("bot_text", "please_send_hash", callback.from_user.id))
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
            await bot.send_message(message.from_user.id,
                                   get_json_text("bot_text", "incorrect_hash", message.from_user.id))
        else:
            await bot.send_message(message.from_user.id,
                                   f"{amount} BTC {get_json_text('bot_text', 'funds_coming_soon_bot_wallet', message.from_user.id)}")
            add_btc(message.from_user.id, amount)
            await bot.send_message(message.from_user.id,
                                   get_json_text('bot_text', 'check_balance', message.from_user.id))
    else:
        await bot.send_message(message.from_user.id,
                               get_json_text('bot_text', "already_use_hash", message.from_user.id))


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
            await bot.send_message(message.from_user.id,
                                   get_json_text("bot_text", "incorrect_hash", message.from_user.id))
        else:
            await bot.send_message(message.from_user.id,
                                   f"{amount} USDT {get_json_text('bot_text', 'funds_coming_soon_bot_wallet', message.from_user.id)}")
            add_usdt(message.from_user.id, amount)
            await bot.send_message(message.from_user.id,
                                   get_json_text('bot_text', 'check_balance', message.from_user.id))

    else:
        await bot.send_message(message.from_user.id,
                               get_json_text('bot_text', "already_use_hash", message.from_user.id))


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
            await bot.send_message(message.from_user.id,
                                   get_json_text("bot_text", "incorrect_hash", message.from_user.id))
        else:
            await bot.send_message(message.from_user.id,
                                   f"{amount} XMR {get_json_text('bot_text', 'funds_coming_soon_bot_wallet', message.from_user.id)}")
            add_xmr(message.from_user.id, amount)
            await bot.send_message(message.from_user.id,
                                   get_json_text('bot_text', 'check_balance', message.from_user.id))
    else:
        await bot.send_message(message.from_user.id,
                               get_json_text('bot_text', "already_use_hash", message.from_user.id))


# Конец блока зачисления крипты на счет пользователя


# Вывод объявлений и добавление новых
@dp.callback_query_handler(text=['ad'])
async def p2p_board_ad(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == 'ad':
        await bot.send_message(callback.from_user.id, get_json_text("bot_text", "user_ads", callback.from_user.id),
                               reply_markup=show_ads_board(callback.from_user.id))


# Блок добавления объявления
@dp.callback_query_handler(text=['add_new_ad'])
async def p2p_add_new_ad(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == 'add_new_ad':
        creationad(callback.from_user.id)
        await bot.send_message(callback.from_user.id, get_json_text("bot_text", "sell_buy_type", callback.from_user.id),
                               reply_markup=choose_type_board(callback.from_user.id))


@dp.callback_query_handler(text=["create_buy_ad", "create_sell_ad", "back_to"])
async def p2p_choose_type(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == "create_buy_ad":
        update_adtype(callback.from_user.id, "BUY")
        await bot.send_message(callback.from_user.id, get_json_text("bot_text", "choose_crypto", callback.from_user.id),
                               reply_markup=choose_p2p_crypto_board)
    elif callback.data == "create_sell_ad":
        update_adtype(callback.from_user.id, "SELL")
        await bot.send_message(callback.from_user.id, get_json_text("bot_text", "choose_crypto", callback.from_user.id),
                               reply_markup=choose_p2p_crypto_board)
    elif callback.data == "back_to":
        await bot.send_message(callback.from_user.id, get_json_text("bot_text", "user_ads", callback.from_user.id),
                               reply_markup=show_ads_board(callback.from_user.id))


@dp.callback_query_handler(text=["BTC", "USDT", "XMR"])
async def p2p_choose_crypto(callback: types.CallbackQuery):
    await callback.message.delete()
    update_adcrypto(callback.from_user.id, callback.data)
    update_fiat(callback.from_user.id)
    await bot.send_message(callback.from_user.id, get_json_text("bot_text", "pay_type", callback.from_user.id),
                           reply_markup=pay_type(callback.from_user.id))


@dp.callback_query_handler(text=["other", "crypto", "world", "online_wallet", "bank"])
async def p2p_choose_paytype(callback: types.CallbackQuery):
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, get_json_text("bot_text", "pay_method", callback.from_user.id),
                           reply_markup=choose_p2p_paymethod(check_fiat(callback.from_user.id)[0], callback.data))


@dp.callback_query_handler(text=check_all_data())
async def p2p_choose_methods(callback: types.CallbackQuery):
    await callback.message.delete()
    update_pay_method(callback.from_user.id, callback.data)
    await bot.send_message(callback.from_user.id, get_json_text("bot_text", "write_requisites", callback.from_user.id),
                           reply_markup=types.ReplyKeyboardRemove())
    await get_ad_data.get_requisites.set()


@dp.message_handler(state=get_ad_data.get_requisites)
async def p2p_get_requisites(message: types.Message, state: FSMContext):
    await state.update_data(requisites=message.text)
    await bot.send_message(message.from_user.id, get_json_text("bot_text", "write_amount_crypto", message.from_user.id), reply_markup=back_to_button(message.from_user.id))
    await get_ad_data.next()


@dp.message_handler(state=get_ad_data.get_limits)
async def p2p_get_limits(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    update_price(message.from_user.id, message.text)
    limit = float(check_amount(message.from_user.id)[0]) * float(check_price(message.from_user.id)[0])
    if check_ad_type(message.from_user.id)[0] == "SELL":
        await bot.send_message(message.from_user.id,
                               f"{get_json_text('bot_text', 'write_limits', message.from_user.id)}: 1-{limit}")
    else:
        await bot.send_message(message.from_user.id,
                               f"{get_json_text('bot_text', 'write_limits', message.from_user.id)}: 1-{limit}")
    await get_ad_data.next()


@dp.message_handler(state=get_ad_data.get_amount)
async def p2p_get_amount(message: types.Message, state: FSMContext):
    if message.text == f"❌ {get_json_text('buttons_text', 'back_to_button', message.from_user.id)}":
        await bot.send_message(message.from_user.id, "❌", reply_markup=show_mainboard(message.from_user.id))
        await state.finish()
    if check_crypto_balance(message.from_user.id)[0] == "BTC":
        balance = get_balance(message.from_user.id)[0]
    elif check_crypto_balance(message.from_user.id)[0] == "USDT":
        balance = get_balance(message.from_user.id)[1]
    elif check_crypto_balance(message.from_user.id)[0] == "XMR":
        balance = get_balance(message.from_user.id)[2]
    if float(balance) < float(message.text) and check_ad_type(message.from_user.id)[0] == "SELL":
        await bot.send_message(message.from_user.id, get_json_text("bot_text", "not_in_balance", message.from_user.id))
        await get_ad_data.get_amount.set()
    else:
        await state.update_data(amount=message.text)
        update_amount(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, get_json_text('bot_text', "write_price", message.from_user.id))
        await get_ad_data.next()


@dp.message_handler(state=get_ad_data.get_price)
async def p2p_get_price(message: types.Message, state: FSMContext):
    global limit1
    try:
        limit1 = float(message.text.split("-")[1])
    except:
        await bot.send_message(message.from_user.id,
                               get_json_text("bot_text", "incorrect_limits", message.from_user.id),
                               reply_markup=show_mainboard(message.from_user.id))
        await state.finish()
    limit = float(check_amount(message.from_user.id)[0]) * float(check_price(message.from_user.id)[0])
    if limit1 > limit and check_ad_type(message.from_user.id)[0] == "SELL":
        await bot.send_message(message.from_user.id, get_json_text("bot_text", "to_big_limits", message.from_user.id),
                               reply_markup=show_mainboard(message.from_user.id))
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
        await bot.send_message(message.from_user.id, get_json_text("bot_text", "ad_is_created", message.from_user.id),
                               reply_markup=show_mainboard(message.from_user.id))


# Конец блока создания объявлений


# Блок взаимодействия пользователей
@dp.callback_query_handler(text=['buy', 'sell'])
async def start_p2p_extend(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == 'buy':
        set_order_ad_type(callback.from_user.id, "SELL")
        await bot.send_message(callback.from_user.id, get_json_text("bot_text", "choose_crypto", callback.from_user.id),
                               reply_markup=create_order_board)
    elif callback.data == 'sell':
        set_order_ad_type(callback.from_user.id, "BUY")
        await bot.send_message(callback.from_user.id, get_json_text("bot_text", "choose_crypto", callback.from_user.id),
                               reply_markup=create_order_board)


@dp.callback_query_handler(text=["btc_order", "usdt_order", "xmr_order"])
async def set_p2p_crypro_and_fiat(callback: types.CallbackQuery):
    await callback.message.delete()
    if callback.data == "btc_order":
        set_order_crypto(callback.from_user.id, "BTC")
        set_order_fiat(callback.from_user.id, check_fiat(callback.from_user.id)[0])
        await bot.send_message(callback.from_user.id, get_json_text("bot_text", "pay_type", callback.from_user.id),
                               reply_markup=pay_type_order(callback.from_user.id))
    elif callback.data == "usdt_order":
        set_order_crypto(callback.from_user.id, "USDT")
        set_order_fiat(callback.from_user.id, check_fiat(callback.from_user.id)[0])
        await bot.send_message(callback.from_user.id, get_json_text("bot_text", "pay_type", callback.from_user.id),
                               reply_markup=pay_type_order(callback.from_user.id))
    elif callback.data == "xmr_order":
        set_order_crypto(callback.from_user.id, "XMR")
        set_order_fiat(callback.from_user.id, check_fiat(callback.from_user.id)[0])
        await bot.send_message(callback.from_user.id, get_json_text("bot_text", "pay_type", callback.from_user.id),
                               reply_markup=pay_type_order(callback.from_user.id))


@dp.callback_query_handler(text=["other_order", "crypto_order", "world_order", "online_wallet_order", "bank_order"])
async def set_p2p_paytype(callback: types.CallbackQuery):
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, get_json_text("bot_text", "pay_method", callback.from_user.id),
                           reply_markup=choose_order_paymethod(check_fiat(callback.from_user.id)[0], callback.data))


@dp.callback_query_handler(Text(startswith="pay_"))
async def set_p2p_pay_method(callback: types.CallbackQuery):
    await callback.message.delete()
    data = callback.data.split("pay_")[1]
    set_order_paymethod(callback.from_user.id, data.split("_")[0])
    await bot.send_message(callback.from_user.id, "📄📄📄📄",
                           reply_markup=show_ads_to_create_order_board(callback.from_user.id))


@dp.callback_query_handler(Text(startswith="ad_"))
async def choose_ad_and_exchange(callback: types.CallbackQuery):
    await callback.message.delete()
    ad_owner = check_user_id(callback.data)
    if str(callback.from_user.id) == str(ad_owner):
        await bot.send_message(callback.from_user.id, get_json_text('bot_text', 'edit_ad', callback.from_user.id),
                               reply_markup=my_ad_settings(callback.data, callback.from_user.id))
        await get_ad_data_repleace.get_ad_id.set()
    else:
        data = get_ad_data_order(callback.data)
        text = f"ID: {callback.data}\n\n{get_json_text('bot_text', 'description', callback.from_user.id)}: {data[6]}\n\n{get_json_text('bot_text', 'price', callback.from_user.id)} {data[0]}\n\n{get_json_text('bot_text', 'crypto', callback.from_user.id)} {data[2]}\n\n {get_json_text('bot_text', 'pay_method_is', callback.from_user.id)} {data[1]}\n\n /user{data[3]}"
        order = start_order(callback.from_user.id, data[3], callback.data)
        await bot.send_message(callback.from_user.id, text, reply_markup=start_exthenge(order, callback.from_user.id))
        await Order.get_order_id.set()


@dp.callback_query_handler(Text(startswith="order_"), state=Order.get_order_id)
async def new_order_start(callback: types.CallbackQuery, state: FSMContext):
    get_ad = get_ad_id(callback.data)
    get_limits = check_limits_order(get_ad)
    await bot.send_message(callback.from_user.id,
                           f"{get_json_text('bot_text', 'write_amount', callback.from_user.id)} {get_limits}", reply_markup=back_to_button(callback.from_user.id))
    await state.update_data(order_id=callback.data)
    await state.update_data(main_limit=get_limits)
    await Order.next()


@dp.message_handler(state=Order.get_amount)
async def get_order_user_limits(message: types.Message, state: FSMContext):
    await state.update_data(user_amount=message.text)
    data = await state.get_data()
    if message.text == f"❌ {get_json_text('buttons_text', 'back_to_button', message.from_user.id)}":
        await bot.send_message(message.from_user.id, "❌", reply_markup=show_mainboard(message.from_user.id))
        await state.finish()
    if float(data["user_amount"]) < float(data["main_limit"].split("-")[0]) or float(data["user_amount"]) > float(
            data["main_limit"].split("-")[1]):
        await bot.send_message(message.from_user.id,
                               get_json_text("bot_text", "incorrect_limits", message.from_user.id))
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
                                       f"{get_json_text('bot_text', 'not_in_balance', message.from_user.id)}: {round(float(is_balance) * float(price), 1)}")
            else:
                set_order_amount(data["order_id"], data['user_amount'])
                await bot.send_message(message.from_user.id,
                                       get_json_text("bot_text", "write_requisites", message.from_user.id))
                await Order.get_requisites.set()
        else:
            get_requisites = check_requsites_order(get_ad)
            maker = get_maker_and_taker(data["order_id"])[0]
            set_order_amount(data["order_id"], data['user_amount'])
            await bot.send_message(message.from_user.id,
                                   f"{get_json_text('bot_text', 'send', message.from_user.id)} {data['user_amount']} {get_json_text('bot_text', 'to', message.from_user.id)} {get_requisites}",
                                   reply_markup=is_paid(data['order_id'], message.from_user.id))
            await bot.send_message(maker,
                                   f"{get_json_text('bot_text', 'wait_pay', message.from_user.id)} {message.from_user.id}\n{get_json_text('bot_text', 'sum', message.from_user.id)} {data['user_amount']}")
            await state.finish()


@dp.message_handler(state=Order.get_requisites)
async def get_order_requisites(message: types.Message, state: FSMContext):
    if message.text == f"❌ {get_json_text('buttons_text', 'back_to_button', message.from_user.id)}":
        await bot.send_message(message.from_user.id, "❌", reply_markup=show_mainboard(message.from_user.id))
        await state.finish()
    await state.update_data(taker_requisites=message.text)
    data = await state.get_data()
    await bot.send_message(message.from_user.id,
                           f"{get_json_text('bot_text', 'is_requisites_true', message.from_user.id)} {data['taker_requisites']}",
                           reply_markup=confirm_requisites_buttons(data["order_id"], data["taker_requisites"],
                                                                   data["user_amount"]))
    await state.finish()


@dp.callback_query_handler(Text(startswith="req_done_"))
async def confirm_requisites(callback: types.CallbackQuery):
    requisit = callback.data.split("req_done_")[1].split("_")[0]
    maker = get_maker_and_taker(
        callback.data.split("req_done_")[1].split("_")[2] + "_" + callback.data.split("req_done_")[1].split("_")[3])[0]
    amount = callback.data.split("req_done_")[1].split("_")[1]
    await bot.send_message(maker,
                           f"{get_json_text('bot_text', 'new_order', maker)} user{callback.from_user.id}\n\n {get_json_text('bot_text', 'send', maker)} {amount} {get_json_text('bot_text', 'to', maker)} {requisit}",
                           reply_markup=is_paid_maker(user_id=maker,
                                                      order_id=callback.data.split("req_done_")[1].split("_")[2] + "_" +
                                                               callback.data.split("req_done_")[1].split("_")[3]))
    await bot.send_message(callback.from_user.id,
                           f"{get_json_text('bot_text', 'wait_pay', callback.from_user.id)} {maker}")


@dp.callback_query_handler(Text(startswith="is_paid_maker_"))
async def confirm_paid_taker(callback: types.CallbackQuery):
    taker = get_maker_and_taker(callback.data.split("is_paid_maker_")[1])[1]
    await bot.send_message(taker, f"{get_json_text('bot_text', 'is_paid', callback.from_user.id)}",
                           reply_markup=confirm_paid_from_taker(callback.data.split("is_paid_maker_")[1],
                                                                user_id=taker))


@dp.callback_query_handler(Text(startswith="paid_confirm_taker_"))
async def withdraw_to_taker(callback: types.CallbackQuery):
    maker = get_maker_and_taker(callback.data.split("paid_confirm_taker_")[1])[0]
    taker = get_maker_and_taker(callback.data.split("paid_confirm_taker_")[1])[1]
    amount = get_order_amount(callback.data.split("paid_confirm_taker_")[1])
    get_ad = get_ad_id(callback.data.split("paid_confirm_taker_")[1])
    crypto = check_crypto_order(get_ad)
    price = check_price_to_order(get_ad)
    to_withdraw = float(amount) / float(price)
    to_adminwallet = to_withdraw / 100
    if crypto == "BTC":
        add_btc(maker, to_withdraw - to_adminwallet)
        add_btc(taker, -to_withdraw)
        input_btc_on_adminbalance(to_adminwallet)
    elif crypto == "USDT":
        add_usdt(maker, to_withdraw - to_adminwallet)
        add_usdt(taker, -to_withdraw)
        input_usdt_on_adminbalance(to_adminwallet)
    elif crypto == "XMR":
        add_xmr(maker, to_withdraw - to_adminwallet)
        add_xmr(taker, -to_withdraw)
        input_xmr_on_adminbalance(to_adminwallet)
    write_to_history(taker, maker, to_withdraw, crypto)
    await bot.send_message(taker, f"{get_json_text('bot_text', 'from_wallet', taker)} {to_withdraw} {crypto}")
    await bot.send_message(maker,
                           f"{get_json_text('bot_text', 'to_wallet', maker)} {to_withdraw - to_adminwallet} {crypto}")


@dp.callback_query_handler(Text(startswith="req_fail_"))
async def unconfirm_requisites(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, "❌")


@dp.callback_query_handler(Text(startswith="is_paid_taker_"))
async def confirm_paid_maker(callback: types.CallbackQuery):
    maker = get_maker_and_taker(callback.data.split("is_paid_taker_")[1])[0]
    await bot.send_message(maker, f"{callback.from_user.id} {get_json_text('bot_text', 'is_paid', maker)}",
                           reply_markup=confirm_paid_from_maker(callback.data.split("is_paid_taker_")[1], maker))
    await bot.send_message(callback.from_user.id, get_json_text('bot_text', 'funds_coming_soon', callback.from_user.id))


@dp.callback_query_handler(Text(startswith="paid_confirm_"))
async def withdraw_to_taker(callback: types.CallbackQuery):
    maker = get_maker_and_taker(callback.data.split("paid_confirm_")[1])[0]
    taker = get_maker_and_taker(callback.data.split("paid_confirm_")[1])[1]
    amount = get_order_amount(callback.data.split("paid_confirm_")[1])
    get_ad = get_ad_id(callback.data.split("paid_confirm_")[1])
    crypto = check_crypto_order(get_ad)
    price = check_price_to_order(get_ad)
    to_withdraw = float(amount) / float(price)
    to_adminwallet = to_withdraw / 100
    if crypto == "BTC":
        add_btc(maker, -to_withdraw)
        add_btc(taker, to_withdraw - to_adminwallet)
        input_btc_on_adminbalance(to_adminwallet)
    elif crypto == "USDT":
        add_usdt(maker, -to_withdraw)
        add_usdt(taker, to_withdraw - to_adminwallet)
        input_usdt_on_adminbalance(to_adminwallet)
    elif crypto == "XMR":
        add_xmr(maker, -to_withdraw)
        add_xmr(taker, to_withdraw - to_adminwallet)
        input_xmr_on_adminbalance(to_adminwallet)
    write_to_history(taker, maker, to_withdraw, crypto)
    await bot.send_message(maker, f"{get_json_text('bot_text', 'from_wallet', maker)} {to_withdraw} {crypto}")
    await bot.send_message(taker,
                           f"{get_json_text('bot_text', 'to_wallet', taker)}  {to_withdraw - to_adminwallet} {crypto}")


# Настройки объявления
@dp.callback_query_handler(Text(startswith="new_limit_"), state=get_ad_data_repleace.get_ad_id)
async def new_limit(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    ad_id = callback.data.split("new_limit_")[1]
    await state.update_data(ad_id=ad_id)
    limits_now = check_limits_order(ad_id)
    await bot.send_message(callback.from_user.id,
                           f"{get_json_text('bot_text', 'write_new_limits', callback.from_user.id)} {limits_now}")
    await get_ad_data_repleace.get_new_limits.set()


@dp.message_handler(state=get_ad_data_repleace.get_new_limits)
async def new_limits_ad(message: types.Message, state: FSMContext):
    await state.update_data(new_limit=message.text)
    data = await state.get_data()
    try:
        limit2 = float(data["new_limit"].split("-")[1])
        ad_id = data["ad_id"]
        amount = check_amount_order(ad_id)
        price = check_price_to_order(ad_id)
        if float(amount) * float(price) < limit2 and check_ad_type_order(ad_id) == "SELL":
            await bot.send_message(message.from_user.id,
                                   get_json_text('bot_text', 'set_incorrect_limits', message.from_user.id))
        else:
            update_limits_new(ad_id, data["new_limit"])
            await bot.send_message(message.from_user.id, get_json_text('bot_text', 'set_limits', message.from_user.id),
                                   reply_markup=show_mainboard(message.from_user.id))
            await state.finish()
    except Exception as e:
        await bot.send_message(message.from_user.id,
                               get_json_text('bot_text', 'set_incorrect_limits', message.from_user.id))


@dp.callback_query_handler(Text(startswith="new_price_"), state=get_ad_data_repleace.get_ad_id)
async def new_price(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    ad_id = callback.data.split("new_price_")[1]
    await state.update_data(ad_id=ad_id)
    price = check_price_to_order(ad_id)
    await bot.send_message(callback.from_user.id,
                           f"{get_json_text('bot_text', 'price_now', callback.from_user.id)} {price}\n\n{get_json_text('bot_text', 'write_new_price', callback.from_user.id)}")
    await get_ad_data_repleace.get_new_price.set()


@dp.message_handler(state=get_ad_data_repleace.get_new_price)
async def new_price_ad(message: types.Message, state: FSMContext):
    try:
        float(message.text)
        await state.update_data(new_price=message.text)
        data = await state.get_data()
        update_price_new(data["ad_id"], data["new_price"])
        await state.finish()
        await bot.send_message(message.from_user.id, get_json_text('bot_text', 'set_new_price', message.from_user.id),
                               reply_markup=show_mainboard(message.from_user.id))
    except:
        await state.finish()
        await bot.send_message(message.from_user.id, get_json_text('bot_text', 'incorrect_data', message.from_user.id),
                               reply_markup=show_mainboard(message.from_user.id))


@dp.callback_query_handler(Text(startswith="new_description_"), state=get_ad_data_repleace.get_ad_id)
async def new_description(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    ad_id = callback.data.split("new_description_")[1]
    await state.update_data(ad_id=ad_id)
    await bot.send_message(callback.from_user.id, get_json_text("bot_text", "write_description", callback.from_user.id))
    await get_ad_data_repleace.get_new_description.set()


@dp.message_handler(state=get_ad_data_repleace.get_new_description)
async def new_description_ad(message: types.Message, state: FSMContext):
    await state.update_data(new_description=message.text)
    data = await state.get_data()
    update_description_new(data['ad_id'], data['new_description'])
    await bot.send_message(message.from_user.id, get_json_text('bot_text', 'set_new_text', message.from_user.id),
                           reply_markup=show_mainboard(message.from_user.id))
    await state.finish()


@dp.callback_query_handler(Text(startswith="new_requisites_"), state=get_ad_data_repleace.get_ad_id)
async def new_requisites(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    ad_id = callback.data.split("new_requisites_")[1]
    await state.update_data(ad_id=ad_id)
    await bot.send_message(callback.from_user.id,
                           get_json_text('bot_text', 'write_new_requisites', callback.from_user.id))
    await get_ad_data_repleace.get_new_requisites.set()


@dp.message_handler(state=get_ad_data_repleace.get_new_requisites)
async def new_requisites_ad(message: types.Message, state: FSMContext):
    await state.update_data(new_requisites=message.text)
    data = await state.get_data()
    update_requisites_new(data['ad_id'], data['new_requisites'])
    await bot.send_message(message.from_user.id, get_json_text('bot_text', 'set_new_requisites', message.from_user.id),
                           reply_markup=show_mainboard(message.from_user.id))
    await state.finish()


@dp.callback_query_handler(Text(startswith="off_"), state=get_ad_data_repleace.get_ad_id)
async def off_ad(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.finish()
    ad_id = callback.data.split("off_")[1]
    ad_off(ad_id)
    await bot.send_message(callback.from_user.id, get_json_text('bot_text', 'ad_off', callback.from_user.id),
                           reply_markup=show_mainboard(callback.from_user.id))


@dp.callback_query_handler(Text(startswith="on_"), state=get_ad_data_repleace.get_ad_id)
async def on_ad(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.finish()
    ad_id = callback.data.split("on_")[1]
    ad_on(ad_id)
    await bot.send_message(callback.from_user.id, get_json_text('bot_text', 'ad_on', callback.from_user.id),
                           reply_markup=show_mainboard(callback.from_user.id))


@dp.callback_query_handler(Text(startswith="delete_"), state=get_ad_data_repleace.get_ad_id)
async def ad_delete(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.finish()
    ad_id = callback.data.split("delete_")[1]
    delete_ad(ad_id)
    await bot.send_message(callback.from_user.id, get_json_text('bot_text', 'ad_delete', callback.from_user.id))


@dp.callback_query_handler(text=['exit'], state=get_ad_data_repleace.get_ad_id)
async def exit_from_redactor(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, get_json_text('bot_text', 'end_edit', callback.from_user.id))
    await state.finish()


# Настройки
@dp.callback_query_handler(text=['lang', 'fiat'])
async def settings(callback: types.CallbackQuery):
    if callback.data == 'fiat':
        await bot.send_message(callback.from_user.id, get_json_text('bot_text', 'set_new_fiat', callback.from_user.id),
                               reply_markup=fiat_board)
    elif callback.data == 'lang':
        await bot.send_message(callback.from_user.id, get_json_text('bot_text', 'set_new_lang', callback.from_user.id),
                               reply_markup=lang_board)


@dp.callback_query_handler(text=['ru', 'en', 'ar', 'fa'])
async def choose_lang(callback: types.CallbackQuery):
    change_lang(callback.from_user.id, callback.data)
    await bot.send_message(callback.from_user.id, get_json_text('bot_text', 'new_settings', callback.from_user.id),
                           reply_markup=show_mainboard(callback.from_user.id))


# Смена валюты
@dp.callback_query_handler(text=['USD', 'KZT', 'UAH', 'CNY', 'VND', 'BRL', 'IRR', 'RUB', 'TRY', 'AED', 'SAR', 'EGP'])
async def choose_fiat(callback: types.CallbackQuery):
    fiats = ['USD', 'KZT', 'UAH', 'CNY', 'VND', 'BRL', 'IRR', 'RUB', 'TRY', 'AED', 'SAR', 'EGP']
    if callback.data in fiats:
        change_fiat(callback.from_user.id, callback.data)
        await bot.send_message(callback.from_user.id, get_json_text('bot_text', 'new_settings', callback.from_user.id),
                               reply_markup=show_mainboard(callback.from_user.id))


@dp.message_handler()
async def speak(msg: types.Message):
    if msg.text == f'🔄 {get_json_text("buttons_text", "p2p_button", msg.from_user.id)}':
        await bot.send_message(msg.from_user.id,
                               get_json_text("bot_text", "p2p_section", msg.from_user.id),
                               reply_markup=main_p2p_il_board(msg.from_user.id))
        search_order(msg.from_user.id)
    elif msg.text == f'💰 {get_json_text("buttons_text", "balance_button", msg.from_user.id)}':
        wallet_creat = wallet(msg.from_user.id)
        if wallet_creat == "Success":
            await bot.send_message(msg.from_user.id,
                                   f"{get_json_text('bot_text', 'new_wallet', msg.from_user.id)} {msg.from_user.id}")
        else:
            await bot.send_message(msg.from_user.id, get_json_text('bot_text', 'already_wallet', msg.from_user.id))
        balances = get_balance(msg.from_user.id)
        fiat = check_fiat(msg.from_user.id)
        btc_to_fiat = getprice("BTC", fiat[0]) * balances[0]
        usdt_to_fiat = getprice("USDT", fiat[0]) * balances[1]
        xmr_to_fiat = getprice("XMR", fiat[0]) * balances[2]
        overall_balance = btc_to_fiat + usdt_to_fiat + xmr_to_fiat
        await bot.send_message(msg.from_user.id,
                               f"{get_json_text('bot_text', 'total_balance', msg.from_user.id)} ≈ {round(overall_balance, 1)} {fiat[0]}\n\n{balances[0]} BTC ≈ {round(btc_to_fiat, 1)} {fiat[0]}\n\n{balances[1]} USDT(TRC20) ≈ {round(usdt_to_fiat, 1)} {fiat[0]}\n\n{balances[2]} XMR ≈ {round(xmr_to_fiat, 1)} {fiat[0]}",
                               reply_markup=take_off_on(msg.from_user.id))
    elif msg.text == f'⚙ {get_json_text("buttons_text", "settings_button", msg.from_user.id)}':
        user = msg.from_user.id
        await bot.send_message(msg.from_user.id,
                               f"{get_json_text('bot_text', 'settings', msg.from_user.id)} /user{user}",
                               reply_markup=settings_board)
    elif msg.text == f'🚨 {get_json_text("buttons_text", "suppotr_button", msg.from_user.id)}':
        await bot.send_message(msg.from_user.id,
                               f"{get_json_text('bot_text', 'support', msg.from_user.id)} {support_acount}")
    elif msg.text == f'📌 {get_json_text("buttons_text", "faq_button", msg.from_user.id)}':
        await bot.send_message(msg.from_user.id, get_json_text('bot_text', 'FAQ', msg.from_user.id))
    elif msg.text == "➕ Добавить нового администратора":
        if is_admin(msg.from_user.id):
            await bot.send_message(msg.from_user.id, "Напишите user ID нового админа", reply_markup=cancel_board)
            await new_admin.get_id.set()
        else:
            await bot.send_message(msg.from_user.id, "Access is denied")
    elif msg.text == "➕ Добавить платежку":
        if is_admin(msg.from_user.id):
            await bot.send_message(msg.from_user.id, "Введите валюту", reply_markup=cancel_board)
            await new_pay_mehod.get_admin_fiat.set()
        else:
            await bot.send_message(msg.from_user.id, "Access is denied")
    elif msg.text == "❌ Отменить":
        await bot.send_message(msg.from_user.id, "Отменено", reply_markup=show_mainboard(msg.from_user.id))
    elif msg.text.startswith("/user"):
        user_id = msg.text.split("/user")[1]
        data = show_history(user_id)
        text = []
        for i in data:
            text.append(f"Taker : {i[0]}, Maker: {i[1]}, Amount : {i[2]}, Crypto : {i[3]}")
        text = "\n\n".join(text)
        if len(text) == 0:
            await bot.send_message(msg.from_user.id, get_json_text("bot_text", "none_orders", msg.from_user.id))
        else:
            await bot.send_message(msg.from_user.id, text)
    elif msg.text == "📈 Статистика":
        data = show_all_history()
        text = []
        for i in data:
            text.append(f"Taker : {i[0]}, Maker: {i[1]}, Amount : {i[2]}, Crypto : {i[3]}")
        text = "\n\n".join(text)
        with open("Статистика.txt", "w") as f:
            f.write(text)
        await bot.send_document(msg.from_user.id, open("Статистика.txt", 'rb'))
    elif msg.text == "👥 Пользователи":
        data = get_all_users()
        text = []
        for i in data:
            text.append(f"Пользователь: {i[0]}, BTC: {i[1]}, USDT: {i[2]}, XMR: {i[3]}")
        text = "\n\n".join(text)
        with open("All users.txt", "w") as f:
            f.write(text)
        await bot.send_document(msg.from_user.id, open("All users.txt", "rb"))
    elif msg.text == "Вывести BTC" and is_admin(msg.from_user.id):
        await bot.send_message(msg.from_user.id, "Напишите количество")
        await withdraw_btc.get_amount.set()
    elif msg.text == "Вывести USDT" and is_admin(msg.from_user.id):
        await bot.send_message(msg.from_user.id, "Напишите количество")
        await withdraw_usdt.get_amount.set()
    elif msg.text == "Вывести XMR" and is_admin(msg.from_user.id):
        await bot.send_message(msg.from_user.id, "Напишите количество")
        await withdraw_xmr.get_amount.set()


@dp.message_handler(state=withdraw_btc.get_amount)
async def withdraw_btc_amount(message: types.Message, state: FSMContext):
    balance = show_admin_balance()[0]
    if float(message.text) > balance:
        await bot.send_message(message.from_user.id, "Недостаточно средств")
        await state.finish()
    else:
        input_btc_on_adminbalance(-float(message.text))
        await bot.send_message(message.from_user.id, f"Баланс обновлен, можете выводить {message.text} BTC")
        await state.finish()


@dp.message_handler(state=withdraw_usdt.get_amount)
async def withdraw_usdt_amount(message: types.Message, state: FSMContext):
    balance = show_admin_balance()[1]
    if float(message.text) > balance:
        await bot.send_message(message.from_user.id, "Недостаточно средств")
        await state.finish()
    else:
        input_usdt_on_adminbalance(-float(message.text))
        await bot.send_message(message.from_user.id, f"Баланс обновлен, можете выводить {message.text} USDT")
        await state.finish()


@dp.message_handler(state=withdraw_xmr.get_amount)
async def withdraw_xmr_amount(message: types.Message, state: FSMContext):
    balance = show_admin_balance()[2]
    if float(message.text) > balance:
        await bot.send_message(message.from_user.id, "Недостаточно средств")
        await state.finish()
    else:
        input_xmr_on_adminbalance(-float(message.text))
        await bot.send_message(message.from_user.id, f"Баланс обновлен, можете выводить {message.text} XMR")
        await state.finish()


@dp.message_handler(state=new_admin.get_id)
async def create_new_admin(message: types.Message, state: FSMContext):
    if message.text == "❌ Отменить":
        await bot.send_message(message.from_user.id, "Отменено", reply_markup=admin_board)
        await state.finish()
    else:
        await state.update_data(admin_id=message.text)
        data = await state.get_data()
        new_admin_create(data["admin_id"])
        await bot.send_message(message.from_user.id, "Админ добавлен", reply_markup=admin_board)
        await state.finish()


@dp.message_handler(state=new_pay_mehod.get_admin_fiat)
async def get_admin_fiat_(message: types.Message, state: FSMContext):
    if message.text == "❌ Отменить":
        await bot.send_message(message.from_user.id, "Отменено", reply_markup=admin_board)
        await state.finish()
    else:
        await state.update_data(fiat=message.text)
        await bot.send_message(message.from_user.id, "Введите тип платежки (bank, online_wallet, world, crypto)")
        await new_pay_mehod.next()


@dp.message_handler(state=new_pay_mehod.get_admin_methods)
async def get_admin_methods_(message: types.Message, state: FSMContext):
    if message.text == "❌ Отменить":
        await bot.send_message(message.from_user.id, "Отменено", reply_markup=admin_board)
        await state.finish()
    else:
        await state.update_data(methods=message.text)
        await bot.send_message(message.from_user.id, "Введите название платежки")
        await new_pay_mehod.next()


@dp.message_handler(state=new_pay_mehod.get_admin_method)
async def get_admin_method_(message: types.Message, state: FSMContext):
    if message.text == "❌ Отменить":
        await bot.send_message(message.from_user.id, "Отменено", reply_markup=admin_board)
        await state.finish()
    else:
        await state.update_data(method=message.text)
        data = await state.get_data()
        add_methods_to_json(data["fiat"], data["methods"], data["method"])
        await bot.send_message(message.from_user.id, "Платежка добавлена")
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
