from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


egp = InlineKeyboardButton("🇪🇬 EGP", callback_data='EGP')
sar = InlineKeyboardButton("🇸🇦 SAR", callback_data='SAR')
aed = InlineKeyboardButton("🇦🇪 AED", callback_data='AED')
try_ = InlineKeyboardButton("🇹🇷 TRY", callback_data='TRY')
rub = InlineKeyboardButton("🇷🇺 RUB", callback_data='RUB')
irr = InlineKeyboardButton("🇮🇷 IRR", callback_data='IRR')
brl = InlineKeyboardButton("🇧🇷 BRL", callback_data='BRL')
vnd = InlineKeyboardButton("🇻🇳 VND", callback_data='VND')
cny = InlineKeyboardButton("🇨🇳 CNY", callback_data='CNY')
uah = InlineKeyboardButton("🇺🇦 UAH", callback_data='UAH')
kzt = InlineKeyboardButton("🇰🇿 KZT", callback_data='KZT')
usd = InlineKeyboardButton("🇺🇸 USD", callback_data='USD')

fiat_board = InlineKeyboardMarkup().row(egp, sar).row(aed, try_).row(rub, irr).row(brl, vnd).row(cny, uah).row(kzt, usd)
