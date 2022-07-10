import sqlite3

con = sqlite3.connect("1g84.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS journal (id INTEGER PRIMARY KEY, timestamp INTEGER, name TEXT, title TEXT, time INTEGER)"
)

cur.execute(
    "CREATE TABLE IF NOT EXISTS clipboard (id INTEGER PRIMARY KEY, id_journal INTEGER, timestamp INTEGER, cb TEXT)"
)
cur.execute(
    "CREATE TABLE IF NOT EXISTS media (id INTEGER PRIMARY KEY, id_journal INTEGER, timestamp INTEGER, media_artist TEXT, media_title TEXT )"
)


con.commit()
con.close()
