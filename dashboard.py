import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def getFromDb(sql):
    return pd.read_sql_query(
        sql,
        sqlite3.connect("1g84.db"),
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

# make a plot of the top used name grouped by name
sql = "SELECT name, time FROM journal"
todayByName = getFromDb(sql)
todayByName["time"] = pd.to_timedelta(todayByName["time"], unit="s")
print(todayByName.groupby("name").sum()[:5])
plt.bar(
    todayByName.groupby("name").sum()[:5].index,
    todayByName.groupby("name").sum()[:5]["time"],
)
plt.show()


sql = "SELECT name,  time FROM journal WHERE date(datetime(timestamp , 'unixepoch')) = date('now') "
todayByName = getFromDb(sql)
todayByName["time"] = pd.to_timedelta(todayByName["time"], unit="s")
print(todayByName.groupby("name").sum()[:5])
plt.pie(
    todayByName.groupby("name").sum()[:5]["time"],
    labels=todayByName.groupby("name").sum()[:5].index,
    autopct="%1.1f%%",
)
plt.show()


sql = "SELECT title,  time FROM journal WHERE date(datetime(timestamp , 'unixepoch')) = date('now') "
todayByName = getFromDb(sql)
todayByName["time"] = pd.to_timedelta(todayByName["time"], unit="s")
print(todayByName.groupby("title").sum()[:5])
plt.pie(
    todayByName.groupby("title").sum()[:5]["time"],
    labels=todayByName.groupby("title").sum()[:5].index,
    autopct="%1.1f%%",
)
plt.show()
