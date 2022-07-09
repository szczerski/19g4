import sqlite3
import pandas as pd


def getFromDb(sql):
    return pd.read_sql_query(
        sql,
        sqlite3.connect("19g4.db"),
    )


# top 5 most used apps today
sql = "SELECT name, title, time FROM journal WHERE date(datetime(timestamp , 'unixepoch')) = date('now') "
todayByName = getFromDb(sql)
todayByName["time"] = pd.to_timedelta(todayByName["time"], unit="s")
print(todayByName[["name", "time"]].groupby("name").sum()[:5])

# top 5 most used apps all time
sql = "SELECT name, time FROM journal"
todayByName = getFromDb(sql)
todayByName["time"] = pd.to_timedelta(todayByName["time"], unit="s")
print(todayByName.groupby("name").sum()[:5])

# top 5 most task spent on today
sql = "SELECT title, time FROM journal"
todayByName = getFromDb(sql)
todayByName["time"] = pd.to_timedelta(todayByName["time"], unit="s")
print(todayByName.groupby("title").sum()[:5])
