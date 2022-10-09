import sqlite3

db = sqlite3.connect('database/settings.db')

sql = db.cursor()



def settings_starts(user_id):
    sql.execute(f"SELECT user_id FROM settings WHERE user_id = (?)", (user_id,))
    if sql.fetchone() is None:
        print("work")
        sql.execute("INSERT INTO settings VALUES (?, ?, ?)", (user_id, "ru", "RUB"))
        db.commit()
        return True
    else:
        return False


def change_fiat(user_id, fiat):
    sql.execute(f"UPDATE settings SET fiat = (?) WHERE user_id = (?)", (fiat, user_id))
    db.commit()

def check_fiat(user_id):
    sql.execute("SELECT fiat FROM settings WHERE user_id = (?)", (user_id, ))
    return sql.fetchone()