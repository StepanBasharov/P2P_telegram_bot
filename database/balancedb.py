import sqlite3


def wallet(user_id):
    db = sqlite3.connect('database/db.db')
    sql = db.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS wallets(
        user_id INTEGER,
        BTC REAL, 
        USDT REAL,
        XMR REAL
    )""")
    db.commit()

    sql.execute(f"SELECT user_id FROM wallets WHERE user_id = {user_id}")
    if sql.fetchone() is None:
        sql.execute("INSERT INTO wallets VALUES (?, ?, ?, ?)", (user_id, 0.0, 0.0, 0.0))
        db.commit()
        db.close()
        return "Success"
    else:
        db.close()
        return "Already"


def get_balance(user_id):
    db = sqlite3.connect('database/db.db')
    sql = db.cursor()
    sql.execute(f"SELECT btc, usdt, xmr FROM wallets where user_id = {int(user_id)}")
    data = sql.fetchone()
    db.close()
    return data


def add_btc(user_id, amount):
    db = sqlite3.connect('database/db.db')
    sql = db.cursor()
    sql.execute(f"SELECT btc FROM wallets where user_id = {int(user_id)}")
    btc = sql.fetchone()[0] + amount
    sql.execute(f"UPDATE wallets SET btc = {btc} WHERE user_id = {int(user_id)}")
    db.commit()
    db.close()


def add_usdt(user_id, amount):
    db = sqlite3.connect('database/db.db')
    sql = db.cursor()
    sql.execute(f"SELECT usdt FROM wallets where user_id = {int(user_id)}")
    usdt = sql.fetchone()[0] + amount
    sql.execute(f"UPDATE wallets SET usdt = {usdt} WHERE user_id = {int(user_id)}")
    db.commit()
    db.close()


def add_xmr(user_id, amount):
    db = sqlite3.connect('database/db.db')
    sql = db.cursor()
    sql.execute(f"SELECT xmr FROM wallets where user_id = {int(user_id)}")
    xmr = sql.fetchone()[0] + amount
    sql.execute(f"UPDATE wallets SET xmr = {xmr} WHERE user_id = {int(user_id)}")
    db.commit()
    db.close()
