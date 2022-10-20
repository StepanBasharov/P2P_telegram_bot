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
    sql.execute("INSERT INTO admins VALUES (?)", (user_id, ))
    db.commit()
    db.close()
