import sqlite3
from random import randint
from database.settingsdb import check_fiat

db = sqlite3.connect('database/adsdb.db')

sql = db.cursor()


def creationad(user_id):
    sql.execute(f"SELECT user_id FROM ad_creation WHERE user_id = {user_id}")
    if sql.fetchone() is None:
        sql.execute("INSERT INTO ad_creation VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (user_id, "", "", "", "", "", "", "", ""))
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


def update_pay_method(user_id, method):
    sql.execute("UPDATE ad_creation SET pay_method = (?) WHERE user_id = (?)", (method, user_id))
    db.commit()


def update_requisites(user_id, requisites):
    sql.execute("UPDATE ad_creation SET requisites = (?) WHERE user_id = (?)", (requisites, user_id))
    db.commit()


def update_limits(user_id, limits):
    sql.execute("UPDATE ad_creation SET limits = (?) WHERE user_id = (?)", (limits, user_id))
    db.commit()


def update_amount(user_id, amount):
    sql.execute("UPDATE ad_creation SET amount = (?) WHERE user_id = (?)", (amount, user_id))
    db.commit()


def update_price(user_id, price):
    sql.execute("UPDATE ad_creation SET price = (?) WHERE user_id = (?)", (price, user_id))
    db.commit()


def new_ad(user_id):
    sql.execute(
        f"SELECT ad_type, crypto, fiat, pay_method, requisites, limits, amount, price FROM ad_creation WHERE user_id = (?)",
        (user_id,))
    data = sql.fetchone()
    if data[0] == "BUY":
        new_ad_buy(user_id, data[1], data[2], data[3], data[4], data[5], data[6], data[7])
    else:
        new_ad_sell(user_id, data[1], data[2], data[3], data[4], data[5], data[6], data[7])


def new_ad_sell(user_id, crypto, fiat, pay_method, requisites, limits, amount, price):
    generate_id = str(randint(1, 999999999999))

    sql.execute(f"SELECT ad_id FROM ads WHERE ad_id = (?)", (generate_id,))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO ads VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (generate_id, user_id, crypto, fiat, pay_method, requisites, limits, amount, "SELL", price))
        db.commit()
        return True
    else:
        return False


def new_ad_buy(user_id, crypto, fiat, pay_method, requisites, limits, amount, price):
    generate_id = str(randint(1, 999999999999))

    sql.execute(f"SELECT ad_id FROM ads WHERE ad_id = (?)", (generate_id,))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO ads VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (generate_id, user_id, crypto, fiat, pay_method, requisites, limits, amount, "BUY", price))
        db.commit()
        return True
    else:
        return False


def show_ads(user_id):
    sql.execute("SELECT ad_id, price, pay_method, crypto, ad_type FROM ads WHERE user_id = (?)", (user_id,))
    return sql.fetchall()


def show_ads_to_order(fiat, crypto, pay_method, ad_type):
    sql.execute(
        "SELECT ad_id, price, pay_method, crypto, ad_type FROM ads WHERE crypto = (?) AND fiat = (?) AND pay_method = (?) AND ad_type = (?)",
        (crypto, fiat, pay_method, ad_type))
    return sql.fetchall()


def get_all_ads():
    sql.execute("SELECT ad_id FROM ads")
    data = sql.fetchall()
    new_data = [i[0] for i in data]
    return new_data


def get_ad_data_order(ad_id):
    sql.execute("SELECT price, pay_method, crypto, user_id FROM ads WHERE ad_id = (?)", (ad_id,))
    return sql.fetchone()
