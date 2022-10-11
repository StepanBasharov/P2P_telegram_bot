import sqlite3
from random import randint
from database.settingsdb import check_fiat

db = sqlite3.connect('database/adsdb.db')

sql = db.cursor()


def creationad(user_id):

    sql.execute(f"SELECT user_id FROM ad_creation WHERE user_id = {user_id}")
    if sql.fetchone() is None:
        sql.execute("INSERT INTO ad_creation VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, "", "", "", "", "", "", "", ""))
        db.commit()
        return True
    else:
        return False


def update_adtype(user_id, adtype):
    sql.execute(f"UPDATE ad_creation SET ad_type = (?) WHERE user_id = (?)", (adtype, user_id))
    db.commit()


def update_adcrypto(user_id, crypto):
    sql.execute(f"UPDATE ad_creation SET crypto = (?) WHERE user_id = (?)", (crypto, user_id))
    db.commit()

def update_fiat(user_id):
    fiat = check_fiat(user_id)[0]
    sql.execute(f"UPDATE ad_creation SET fiat = (?) WHERE user_id = (?)", (fiat, user_id))
    db.commit()

def new_ad_sell(user_id, crypto, fiat, pay_method, requisites, limits, amount, price):

    generate_id = str(randint(1, 999999999999))

    sql.execute(f"SELECT ad_id FROM ads WHERE ad_id = (?)", (generate_id, ))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO ads VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (generate_id, user_id, crypto, fiat, price, pay_method, requisites, limits, amount, "SELL"))
        db.commit()
        return True
    else:
        return False


def new_ad_buy(user_id, crypto, fiat, pay_method, requisites, limits, amount, price):

    generate_id = str(randint(1, 999999999999))

    sql.execute(f"SELECT ad_id FROM ads WHERE ad_id = (?)", (generate_id, ))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO ads VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (generate_id, user_id, crypto, price, fiat, pay_method, requisites, limits, amount, "BUY"))
        db.commit()
        return True
    else:
        return False

