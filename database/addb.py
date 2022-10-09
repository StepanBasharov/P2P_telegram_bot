import sqlite3

db = sqlite3.connect('database/adsdb.db')

sql = db.cursor()

from random import randint


def new_ad_sell(user_id, crypto, fiat, pay_method, requisites, limits, amount):

    generate_id = str(randint(1, 999999999999))

    sql.execute(f"SELECT ad_id FROM ads WHERE ad_id = (?)", (generate_id, ))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO ads VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (generate_id, user_id, crypto, fiat, pay_method, requisites, limits, amount, "SELL"))
        db.commit()
        return True
    else:
        return False


def new_ad_buy(user_id, crypto, fiat, pay_method, requisites, limits, amount):

    generate_id = str(randint(1, 999999999999))

    sql.execute(f"SELECT ad_id FROM ads WHERE ad_id = (?)", (generate_id, ))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO ads VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (generate_id, user_id, crypto, fiat, pay_method, requisites, limits, amount, "BUY"))
        db.commit()
        return True
    else:
        return False
