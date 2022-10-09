import sqlite3

db = sqlite3.connect('database/db.db')

sql = db.cursor()



def wallet(user_id):
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
        return "Success"
    else:
        return "Already"

def get_balance(user_id):
    sql.execute(f"SELECT btc, usdt, xmr FROM wallets where user_id = {int(user_id)}")
    return sql.fetchone()

def add_btc(user_id, amount):
    sql.execute(f"SELECT btc FROM wallets where user_id = {int(user_id)}")
    btc = sql.fetchone()[0] + amount
    sql.execute(f"UPDATE wallets SET btc = {btc} WHERE user_id = {int(user_id)}")
    db.commit()

def add_usdt(user_id, amount):
    sql.execute(f"SELECT usdt FROM wallets where user_id = {int(user_id)}")
    usdt = sql.fetchone()[0] + amount
    sql.execute(f"UPDATE wallets SET usdt = {usdt} WHERE user_id = {int(user_id)}")
    db.commit()

def add_xmr(user_id, amount):
    sql.execute(f"SELECT xmr FROM wallets where user_id = {int(user_id)}")
    xmr = sql.fetchone()[0] + amount
    sql.execute(f"UPDATE wallets SET xmr = {xmr} WHERE user_id = {int(user_id)}")
    db.commit()

