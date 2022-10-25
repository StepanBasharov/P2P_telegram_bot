import sqlite3


def is_admin(user_id):
    db = sqlite3.connect('database/admins.db')
    sql = db.cursor()
    sql.execute(f"SELECT admin FROM admins WHERE admin = {user_id}")
    if sql.fetchone() is None:
        return False
    else:
        return True


def new_admin_create(user_id):
    db = sqlite3.connect('database/admins.db')
    sql = db.cursor()
    sql.execute("INSERT INTO admins VALUES (?)", (user_id,))
    db.commit()
    db.close()


def input_btc_on_adminbalance(amount):
    db = sqlite3.connect('database/admins.db')
    sql = db.cursor()
    sql.execute('SELECT BTC FROM adminbalance WHERE wallet = "wallet1"')
    data = sql.fetchone()[0]
    amount = data + amount
    sql.execute(f'UPDATE adminbalance SET BTC = (?) WHERE wallet = "wallet1"', (amount,))
    db.commit()
    db.close()


def input_usdt_on_adminbalance(amount):
    db = sqlite3.connect('database/admins.db')
    sql = db.cursor()
    sql.execute('SELECT USDT FROM adminbalance WHERE wallet = "wallet1"')
    data = sql.fetchone()[0]
    amount = data + amount
    sql.execute(f'UPDATE adminbalance SET USDT = (?) WHERE wallet = "wallet1"', (amount,))
    db.commit()
    db.close()


def input_xmr_on_adminbalance(amount):
    db = sqlite3.connect('database/admins.db')
    sql = db.cursor()
    sql.execute('SELECT XMR FROM adminbalance WHERE wallet = "wallet1"')
    data = sql.fetchone()[0]
    amount = data + amount
    sql.execute(f'UPDATE adminbalance SET XMR = (?) WHERE wallet = "wallet1"', (amount,))
    db.commit()
    db.close()


def show_admin_balance():
    db = sqlite3.connect('database/admins.db')
    sql = db.cursor()
    sql.execute('SELECT BTC, USDT, XMR FROM adminbalance WHERE wallet = "wallet1"')
    data = sql.fetchone()
    db.close()
    return data

def get_all_users():
    db = sqlite3.connect('database/db.db')
    sql = db.cursor()
    sql.execute(f"SELECT user_id, btc, usdt, xmr FROM wallets")
    data = sql.fetchall()
    db.close()
    return data
