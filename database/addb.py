import sqlite3
from random import randint
from database.settingsdb import check_fiat


def creationad(user_id):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute(f"SELECT user_id FROM ad_creation WHERE user_id = {user_id}")
    if sql.fetchone() is None:
        sql.execute("INSERT INTO ad_creation VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (user_id, "", "", "", "", "", "", "", ""))
        db.commit()
        db.close()
        return True
    else:
        db.close()
        return False


def check_crypto_balance(user_id):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("SELECT crypto FROM ad_creation WHERE user_id = (?)", (user_id,))
    data = sql.fetchone()
    db.close()
    return data


def check_price(user_id):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("SELECT price FROM ad_creation WHERE user_id = (?)", (user_id,))
    data = sql.fetchone()
    db.close()
    return data


def check_price_to_order(ad_id):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("SELECT price FROM ads WHERE ad_id = (?)", (ad_id,))
    data = sql.fetchone()[0]
    db.close()
    return data


def check_amount(user_id):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("SELECT amount FROM ad_creation WHERE user_id = (?)", (user_id,))
    data = sql.fetchone()
    db.close()
    return data


def check_limits_order(ad_id):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("SELECT limits FROM ads WHERE ad_id = (?)", (ad_id,))
    data = sql.fetchone()[0]
    db.close()
    return data


def check_ad_type_order(ad_id):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("SELECT ad_type FROM ads WHERE ad_id = (?)", (ad_id,))
    data = sql.fetchone()[0]
    db.close()
    return data


def check_requsites_order(ad_id):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("SELECT requisites FROM ads WHERE ad_id = (?)", (ad_id,))
    data = sql.fetchone()[0]
    db.close()
    return data


def check_crypto_order(ad_id):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("SELECT crypto FROM ads WHERE ad_id = (?)", (ad_id,))
    data = sql.fetchone()[0]
    db.close()
    return data


def check_ad_type(user_id):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("SELECT ad_type FROM ad_creation WHERE user_id = (?)", (user_id,))
    data = sql.fetchone()
    db.close()
    return data


def update_adtype(user_id, adtype):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute(f"UPDATE ad_creation SET ad_type = (?) WHERE user_id = (?)", (adtype, user_id))
    db.commit()
    db.close()


def update_adcrypto(user_id, crypto):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute(f"UPDATE ad_creation SET crypto = (?) WHERE user_id = (?)", (crypto, user_id))
    db.commit()
    db.close()


def update_fiat(user_id):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    fiat = check_fiat(user_id)[0]
    sql.execute(f"UPDATE ad_creation SET fiat = (?) WHERE user_id = (?)", (fiat, user_id))
    db.commit()
    db.close()


def update_pay_method(user_id, method):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("UPDATE ad_creation SET pay_method = (?) WHERE user_id = (?)", (method, user_id))
    db.commit()
    db.close()


def update_requisites(user_id, requisites):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("UPDATE ad_creation SET requisites = (?) WHERE user_id = (?)", (requisites, user_id))
    db.commit()
    db.close()


def update_limits(user_id, limits):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("UPDATE ad_creation SET limits = (?) WHERE user_id = (?)", (limits, user_id))
    db.commit()
    db.close()


def update_amount(user_id, amount):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("UPDATE ad_creation SET amount = (?) WHERE user_id = (?)", (amount, user_id))
    db.commit()
    db.close()


def update_price(user_id, price):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("UPDATE ad_creation SET price = (?) WHERE user_id = (?)", (price, user_id))
    db.commit()
    db.close()


def new_ad(user_id):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute(
        f"SELECT ad_type, crypto, fiat, pay_method, requisites, limits, amount, price FROM ad_creation WHERE user_id = (?)",
        (user_id,))
    data = sql.fetchone()
    if data[0] == "BUY":
        new_ad_buy(user_id, data[1], data[2], data[3], data[4], data[5], data[6], data[7])
    else:
        new_ad_sell(user_id, data[1], data[2], data[3], data[4], data[5], data[6], data[7])
    db.close()


def new_ad_sell(user_id, crypto, fiat, pay_method, requisites, limits, amount, price):
    generate_id = f"ad_{str(randint(1, 999999999999))}"
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute(f"SELECT ad_id FROM ads WHERE ad_id = (?)", (generate_id,))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO ads VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (generate_id, user_id, crypto, fiat, pay_method, requisites, limits, amount, "SELL", price))
        db.commit()
        db.close()
        return True
    else:
        db.close()
        return False


def new_ad_buy(user_id, crypto, fiat, pay_method, requisites, limits, amount, price):
    generate_id = f"ad_{str(randint(1, 999999999999))}"
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute(f"SELECT ad_id FROM ads WHERE ad_id = (?)", (generate_id,))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO ads VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (generate_id, user_id, crypto, fiat, pay_method, requisites, limits, amount, "BUY", price))
        db.commit()
        db.close()
        return True
    else:
        db.close()
        return False


def show_ads(user_id):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("SELECT ad_id, price, pay_method, crypto, ad_type FROM ads WHERE user_id = (?)", (user_id,))
    data = sql.fetchall()
    db.close()
    return data


def show_ads_to_order(fiat, crypto, pay_method, ad_type):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute(
        "SELECT ad_id, price, pay_method, crypto, ad_type, limits FROM ads WHERE crypto = (?) AND fiat = (?) AND pay_method = (?) AND ad_type = (?)",
        (crypto, fiat, pay_method, ad_type))
    data = sql.fetchall()
    db.close()
    return data


def get_all_ads():
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("SELECT ad_id FROM ads")
    data = sql.fetchall()
    new_data = [i[0] for i in data]
    db.close()
    return new_data


def get_ad_data_order(ad_id):
    db = sqlite3.connect('database/adsdb.db')
    sql = db.cursor()
    sql.execute("SELECT price, pay_method, crypto, user_id, limits, amount FROM ads WHERE ad_id = (?)", (ad_id,))
    data = sql.fetchall()
    db.close()
    return data[0]
