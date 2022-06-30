import psutil, win32process, win32gui
import time
import sqlite3


def getForegroundWindowName():
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    return psutil.Process(pid[-1]).name().lower().split(".")[0]


def getForegroundWindowTitle():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())


def pushToDb(current_window_name, current_window_title, runtime):
    con = sqlite3.connect("19g4.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO journal (timestamp, name, title, time)" "VALUES(?, ?, ?, ?)",
        (int(time.time()), current_window_name, current_window_title, runtime),
    )
    con.commit()
    con.close()

time_seconds = time.time()
current_window_title = getForegroundWindowTitle()
current_window_name = getForegroundWindowName()

while True:

    if current_window_title == getForegroundWindowTitle():
        time.sleep(1)
    else:
        runtime = int(time.time() - time_seconds)
        print(current_window_name, current_window_title, runtime)

        pushToDb(current_window_name, current_window_title, runtime)

        time_seconds = time.time()
        current_window_title = getForegroundWindowTitle()
        current_window_name = getForegroundWindowName()
