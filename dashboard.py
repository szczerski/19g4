import sqlite3


con = sqlite3.connect("19g4.db")
cur = con.cursor()
cur.execute(
    "SELECT name, title, time FROM journal WHERE date(datetime(timestamp , 'unixepoch')) = date('now') ",
)
data = cur.fetchall()
for i in data:
    print(f"{i[0]} {i[1]} : {i[2]} seconds")
    
con.commit()
con.close()
