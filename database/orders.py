import sqlite3
from database.addb import show_ads_to_order

db = sqlite3.connect('database/order_search.db')

sql = db.cursor()


def search_order(user_id):
    sql.execute(f"SELECT user_id FROM orders WHERE user_id = (?)", (user_id,))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", (user_id, "USD", "BTC", "Wise", "BUY"))
        db.commit()
        return "Success"
    else:
        return "Already"


def start_order(taker, maker, ad_id):
    sql.execute(f"SELECT ad_id FROM orders_now WHERE ad_id = (?)", (ad_id,))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO orders_now VALUES (?, ?, ?, ?, ?, ?)", (taker, maker, ad_id, 0, 0, 9))
        db.commit()
        return True
    else:
        return False


def set_order_fiat(user_id, fiat):
    sql.execute(f"UPDATE orders SET fiat = (?) WHERE user_id = (?)", (fiat, user_id))
    db.commit()


def set_order_crypto(user_id, crypto):
    sql.execute(f"UPDATE orders SET crypto = (?) WHERE user_id = (?)", (crypto, user_id))
    db.commit()


def set_order_paymethod(user_id, pay_method):
    sql.execute(f"UPDATE orders SET pay_method = (?) WHERE user_id = (?)", (pay_method, user_id))
    db.commit()


def set_order_ad_type(user_id, ad_type):
    sql.execute(f"UPDATE orders SET ad_type = (?) WHERE user_id = (?)", (ad_type, user_id))
    db.commit()


def send_data_to_order(user_id):
    sql.execute("SELECT crypto, fiat, pay_method, ad_type FROM orders WHERE user_id = (?)", (user_id,))
    data = sql.fetchone()
    return show_ads_to_order(data[1], data[0], data[2], data[3])
