import sqlite3

con = sqlite3.connect("19g4.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS journal (id INTEGER PRIMARY KEY, timestamp INTEGER, name TEXT, title TEXT, time INTEGER)"
)

cur.execute(
    "CREATE TABLE IF NOT EXISTS clipboard (id INTEGER PRIMARY KEY, id_journal INTEGER, timestamp INTEGER, cb TEXT)"
)
con.commit()
con.close()
