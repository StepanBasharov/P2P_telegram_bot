import sqlite3


def checker_hash(hash, user_id):
    db = sqlite3.connect('database/hash.db')

    sql = db.cursor()
    sql.execute(f"SELECT hash FROM hashes WHERE hash = (?)", (hash,))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO hashes VALUES (?, ?)", (user_id, hash))
        db.commit()
        db.close()
        return True
    else:
        db.close()
        return False
