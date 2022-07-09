import psutil, win32process, win32gui
import time
import sqlite3
import pyperclip


def getForegroundWindowName():
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[-1]
    return psutil.Process(pid).name().lower().split(".")[0] if pid >= 0 else ""


def getForegroundWindowTitle():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())


def pushToDbJournal(current_window_name, current_window_title, runtime):
    con = sqlite3.connect("19g4.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO journal (timestamp, name, title, time)" "VALUES(?, ?, ?, ?)",
        (int(time.time()), current_window_name, current_window_title, runtime),
    )
    con.commit()
    con.close()


def getDbJournalId():
    con = sqlite3.connect("19g4.db")
    cur = con.cursor()
    cur.execute("SELECT id FROM journal WHERE id = (SELECT MAX(id) FROM journal)")
    id_journal = cur.fetchone()[0]
    con.commit()
    con.close()
    return id_journal


def pushToDbClipboard(cb, id_journal):
    con = sqlite3.connect("19g4.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO clipboard (timestamp, id_journal, cb)" "VALUES( ?, ?, ?)",
        (int(time.time()), id_journal, cb),
    )
    con.commit()
    con.close()


def getClipboard():
    try:
        clipboard = pyperclip.paste()
    except pyperclip.exceptions.PyperclipException:
        clipboard = ""
    return clipboard


time_seconds = time.time()
current_window_title = getForegroundWindowTitle()
current_window_name = getForegroundWindowName()
cb_last = ''

while True:

    if current_window_title == getForegroundWindowTitle():
        time.sleep(1)
    else:
        runtime = int(time.time() - time_seconds)
        print(current_window_name, current_window_title, runtime)

        pushToDbJournal(current_window_name, current_window_title, runtime)

        time_seconds = time.time()
        current_window_title = getForegroundWindowTitle()
        current_window_name = getForegroundWindowName()

    cb = getClipboard()
    if cb != "" and cb_last != cb:
        id_journal = getDbJournalId()
        pushToDbClipboard(cb, id_journal)
        cb_last = cb
