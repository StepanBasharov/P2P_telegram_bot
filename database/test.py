import sqlite3

db = sqlite3.connect('adsdb.db')

sql = db.cursor()

sql.execute("SELECT ad_id, price FROM ads WHERE user_id = (?)", (596651102, ))
print(sql.fetchall())