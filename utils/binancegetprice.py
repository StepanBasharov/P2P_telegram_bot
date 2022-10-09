import requests

crypro_ids = {
    "BTC" : "1",
    "USDT" : "825",
    "XMR" : "328"
}
fiat_ids = {
    "EGP" : "3538",
    "SAR" : "3566",
    "AED" : "2813",
    "TRY" : "2810",
    "RUB" : "2806",
    "IRR" : "3544",
    "BRL" : "2783",
    "VND" : "2823",
    "CNY" : "2787",
    "UAH" : "2824",
    "KZT" : "3551",
    "USD" : "2781"
}


def getprice(crypto, fiat):
    resp = requests.get(f"https://api.coinmarketcap.com/data-api/v3/tools/price-conversion?amount=1&convert_id={fiat_ids[fiat]}&id={crypro_ids[crypto]}").json()
    return resp['data']['quote'][0]['price']
