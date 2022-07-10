import asyncio
import psutil, win32process, win32gui
import time
import sqlite3
import pyperclip
from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
)


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


async def getMediaInfo():
    sessions = await MediaManager.request_async()

    current_session = sessions.get_current_session()

    if current_session:  # there needs to be a media session running
        if current_session.source_app_user_model_id == "chrome.exe":
            info = await current_session.try_get_media_properties_async()

            # song_attr[0] != '_' ignores system attributes
            info_dict = {
                song_attr: info.__getattribute__(song_attr)
                for song_attr in dir(info)
                if song_attr[0] != "_"
            }

            info_dict["genres"] = list(info_dict["genres"])
            return info_dict["artist"], info_dict["title"]


time_seconds = time.time()
current_window_title = getForegroundWindowTitle()
current_window_name = getForegroundWindowName()
cb_last = ""
media_artist_last = ""
media_title_last = ""


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

    media_artist, media_title = asyncio.run(getMediaInfo())
    if (
        media_artist != ""
        and media_title != ""
        and media_artist != media_artist_last
        and media_title != media_title_last
    ):
        print("MEDIA: ", media_title, media_artist)

        media_title_last = media_title
        media_artist_last = media_artist
