import sqlite3
import pandas as pd


def getFromDb(sql):
    return pd.read_sql_query(
        sql,
        sqlite3.connect("19g4.db"),
    )


sql = "SELECT name, title, time FROM journal WHERE date(datetime(timestamp , 'unixepoch')) = date('now') "
todayByName = getFromDb(sql)
print(todayByName.groupby("name").sum())
