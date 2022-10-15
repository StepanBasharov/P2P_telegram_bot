import sqlite3

db = sqlite3.connect('order_search.db')

sql = db.cursor()


def search_order(user_id):

    sql.execute(f"SELECT user_id FROM orders WHERE user_id = (?)", (user_id, ))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO orders VALUES (?, ?, ?, ?)", (user_id, "USD", "BTC", "Wise"))
        db.commit()
        return "Success"
    else:
        return "Already"

def set_order_fiat(user_id, fiat):
    sql.execute(f"UPDATE orders SET fiat = (?) WHERE user_id = (?)", (fiat, user_id))
    db.commit()

def set_order_crypto(user_id, crypto):
    sql.execute(f"UPDATE orders SET crypto = (?) WHERE user_id = (?)", (crypto, user_id))
    db.commit()

def set_order_paymethod(user_id, pay_method):
    sql.execute(f"UPDATE orders SET pay_method = (?) WHERE user_id = (?)", (pay_method, user_id))
    db.commit()

set_order_paymethod(53134324231, "USA bank")