from config.config import TOKEN, support_acount
from config.addreses import BTC_address, USDT_address, XMR_address

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from adminpanel.admins import admins

from keyboards.mainboard import mainboard
from keyboards.p2p_board import p2p_base_board
from keyboards.balance_board import balance_base_board, take_off_crypto_board, take_on_crypro_board, board_success_btc, \
    board_success_usdt, board_success_xmr
from keyboards.settings_board import settings_board
from keyboards.fiat_board import fiat_board
from keyboards.p2p_board import add_ad_board, buy_or_sell_board, choose_p2p_crypto_board

from database.balancedb import wallet, get_balance, add_btc, add_usdt, add_xmr
from database.check_hash import checker_hash
from database.settingsdb import settings_starts, change_fiat, check_fiat
from database.addb import creationad, new_ad_buy, new_ad_sell, update_adtype, update_adcrypto, update_fiat

from states.hash_state import Check_hash_btc, Check_hash_usdt, Check_hash_xmr
from states.output_crypto import output_btc, output_xmr, output_usdt

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
    if callback.data == "take_on":
        await bot.send_message(callback.from_user.id, "Выберете валюту для ввода:", reply_markup=take_on_crypro_board)

    elif callback.data == "take_off":
        await bot.send_message(callback.from_user.id, "Выберете валюту для вывода:", reply_markup=take_off_crypto_board)


# Выбор крипты для ввода
@dp.callback_query_handler(text=['btc_on', 'btc_off', 'usdt_on', 'usdt_off', 'xmr_on', 'xmr_off'])
async def balance_change(callback: types.CallbackQuery):
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
        await bot.send_message(callback.from_user.id, f"{btc_output_balance} BTC доступно для вывода\n\nВведите адресс на который будут отправлены BTC: ")
        await output_btc.send_to.set()
    elif callback.data == "usdt_off":
        usdt_output_balance = get_balance(callback.from_user.id)[1]
        await bot.send_message(callback.from_user.id, f"{usdt_output_balance} USDT доступно для вывода\n\nВведите адресс на который будут отправлены USDT:")
        await output_usdt.send_to.set()
    elif callback.data == "xmr_off":
        xmr_output_balance = get_balance(callback.from_user.id)[2]
        await bot.send_message(callback.from_user.id, f"{xmr_output_balance} XMR доступно для вывода\n\nВведите адресс на который будут отправлены XMR:")
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
        await bot.send_message(-748498807, f"Адрес вывода BTC: <code>{data['btc_address']}</code>\n\nСумма к отправке: <code>{data['amount_send']}</code>\n\nПользователь: {message.from_user.id}", parse_mode=types.ParseMode.HTML)
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
        await bot.send_message(-748498807, f"Адрес вывода USDT: <code>{data['usdt_address']}</code>\n\nСумма к отправке: <code>{data['amount_send']}</code>\n\nПользователь: {message.from_user.id}", parse_mode=types.ParseMode.HTML)
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
        await bot.send_message(-748498807, f"Адрес вывода XMR: <code>{data['xmr_address']}</code>\n\nСумма к отправке: <code>{data['amount_send']}</code>\n\nПользователь: {message.from_user.id}", parse_mode=types.ParseMode.HTML)
        add_xmr(message.from_user.id, -float(data['amount_send']))
        await bot.send_message(message.from_user.id, "Скоро средства поступят на кошелек")
    await state.finish()
# Конец блока состояний для указания сумы отправки и адреса отправки


# Проверка hash транзакции
@dp.callback_query_handler(text=["btc_success", "usdt_success", "xmr_success"])
async def check_hash(callback: types.CallbackQuery):
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
    if callback.data == 'ad':
        await bot.send_message(callback.from_user.id, "Здесь находятся все ваши объявления", reply_markup=add_ad_board)


# Блок добавления объявления
@dp.callback_query_handler(text=['add_new_ad'])
async def p2p_add_new_ad(callback: types.CallbackQuery):
    if callback.data == 'add_new_ad':
        creationad(callback.from_user.id)
        await bot.send_message(callback.from_user.id, "Выберете тип объявления", reply_markup=buy_or_sell_board)


@dp.callback_query_handler(text=["create_buy_ad", "create_sell_ad", "back_to"])
async def p2p_choose_type(callback: types.CallbackQuery):
    if callback.data == "create_buy_ad":
        update_adtype(callback.from_user.id, "BUY")
        await bot.send_message(callback.from_user.id, "Выбор криптовалюты", reply_markup=choose_p2p_crypto_board)
    elif callback.data == "create_sell_ad":
        update_adtype(callback.from_user.id, "SELL")
        await bot.send_message(callback.from_user.id, "Выбор криптовалюты", reply_markup=choose_p2p_crypto_board)
    elif callback.data == "back_to":
        await bot.send_message(callback.from_user.id, "Здесь находятся все ваши объявления", reply_markup=add_ad_board)


@dp.callback_query_handler(text=["BTC", "USDT", "XMR"])
async def p2p_choose_crypto(callback: types.CallbackQuery):
    update_adcrypto(callback.from_user.id, callback.data)
    update_fiat(callback.from_user.id)
    await bot.send_message(callback.from_user.id, "Критпа выбрана")



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
