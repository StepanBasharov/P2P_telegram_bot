import sqlite3
from database.addb import show_ads_to_order
from random import randint


def search_order(user_id):
    db = sqlite3.connect('database/order_search.db')
    sql = db.cursor()
    sql.execute(f"SELECT user_id FROM orders WHERE user_id = (?)", (user_id,))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", (user_id, "USD", "BTC", "Wise", "BUY"))
        db.commit()
        db.close()
        return "Success"
    else:
        db.close()
        return "Already"



def start_order(taker, maker, ad_id):
    db = sqlite3.connect('database/order_search.db')
    sql = db.cursor()
    generate_id = str(randint(1, 999999999999))
    sql.execute(f"SELECT order_id FROM orders_now WHERE order_id = (?)", (generate_id,))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO orders_now VALUES (?, ?, ?, ?, ?, ?, ?)", (taker, maker, ad_id, 0, 0, 0, generate_id))
        db.commit()
        db.close()
        return generate_id
    else:
        db.close()
        return sql.fetchone()[0]


def get_order_id(taker):
    db = sqlite3.connect('database/order_search.db')
    sql = db.cursor()
    sql.execute("SELECT order_id FROM orders_now WHERE taker = (?)", (taker,))
    data = sql.fetchone()[0]
    db.close()
    return data


def get_maker_and_taker(order_id):
    db = sqlite3.connect('database/order_search.db')
    sql = db.cursor()
    sql.execute("SELECT maker, taker FROM orders_now WHERE order_id = (?)", (order_id,))
    data = sql.fetchone()
    db.close()
    return data


def get_all_orders_ids():
    db = sqlite3.connect('database/order_search.db')
    sql = db.cursor()
    sql.execute("SELECT order_id FROM orders_now")
    data = sql.fetchall()
    orders_data = [i[0] for i in data]
    db.close()
    return orders_data


def set_order_fiat(user_id, fiat):
    db = sqlite3.connect('database/order_search.db')
    sql = db.cursor()
    sql.execute(f"UPDATE orders SET fiat = (?) WHERE user_id = (?)", (fiat, user_id))
    db.commit()
    db.close()


def set_order_crypto(user_id, crypto):
    db = sqlite3.connect('database/order_search.db')
    sql = db.cursor()
    sql.execute(f"UPDATE orders SET crypto = (?) WHERE user_id = (?)", (crypto, user_id))
    db.commit()
    db.close()


def set_order_paymethod(user_id, pay_method):
    db = sqlite3.connect('database/order_search.db')
    sql = db.cursor()
    sql.execute(f"UPDATE orders SET pay_method = (?) WHERE user_id = (?)", (pay_method, user_id))
    db.commit()
    db.close()


def set_order_ad_type(user_id, ad_type):
    db = sqlite3.connect('database/order_search.db')
    sql = db.cursor()
    sql.execute(f"UPDATE orders SET ad_type = (?) WHERE user_id = (?)", (ad_type, user_id))
    db.commit()
    db.close()


def send_data_to_order(user_id):
    db = sqlite3.connect('database/order_search.db')
    sql = db.cursor()
    sql.execute("SELECT crypto, fiat, pay_method, ad_type FROM orders WHERE user_id = (?)", (user_id,))
    data = sql.fetchone()
    data = show_ads_to_order(data[1], data[0], data[2], data[3])
    db.close()
    return data
