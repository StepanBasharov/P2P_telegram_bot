import sqlite3

db = sqlite3.connect('database/hash.db')

sql = db.cursor()


def checker_hash(hash, user_id):
    sql.execute(f"SELECT hash FROM hashes WHERE hash = (?)", (hash,))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO hashes VALUES (?, ?)", (user_id, hash))
        db.commit()
        return True
    else:
        return False
