import sqlite3

con = sqlite3.connect("19g4.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS journal (id INTEGER PRIMARY KEY, timestamp INTEGER, name TEXT, title TEXT, time INTEGER)"
)
con.commit()
con.close()
