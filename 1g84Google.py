from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
)
from googleapiclient.discovery import build
from google.oauth2 import service_account
import psutil, win32process, win32gui
import win32api
import time
import datetime
import asyncio
import pyperclip
import pyautogui


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# SERVICE_ACCOUNT_FILE = "./secret/keys.json"
SERVICE_ACCOUNT_FILE = "D:/OneDrive/Backup/1g84/secret/keys.json"


creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

SPREADSHEET_ID = "1GbNCz0vv7o9p_kKRL4RuZHvQpUYSLF0I4mF116xSLWU"

service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()


def start_script(
    cb_last="",
    current_window_name="",
    current_window_title="",
    runtime=0,
    media_artist_last="",
    media_title_last="",
    time_idle = time.time(),
    # session = 1
):
    try:
        # log_path = "./logs/log_google_crash.txt"
        log_path = "D:/OneDrive/Backup/1g84/logs/log_google_crash.txt"

        def getForegroundWindowName():
            pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[
                -1
            ]
            return psutil.Process(pid).name().lower().split(".")[0] if pid >= 0 else ""

        def getForegroundWindowTitle():
            return win32gui.GetWindowText(win32gui.GetForegroundWindow())

        def pushToDbJournal(
            current_window_name, current_window_title, runtime, sheet_name
        ):
            row = [
                [
                    int(time.time()),
                    datetime.date.today().strftime("%d/%m/%Y"),
                    time.strftime("%H:%M"),
                    runtime,
                    current_window_name,
                    current_window_title,
                ]
            ]

            request = (
                sheet.values()
                .append(
                    spreadsheetId=SPREADSHEET_ID,
                    range=sheet_name + "!A1",
                    valueInputOption="USER_ENTERED",
                    insertDataOption="INSERT_ROWS",
                    body={"values": row},
                )
                .execute()
            )

        def getDbJournalId():
            rows = (
                service.spreadsheets()
                .values()
                .get(spreadsheetId=SPREADSHEET_ID, range="journal!A:A")
                .execute()
                .get("values", [])
            )
            last_row_id = len(rows) + 1
            return last_row_id

        def pushToDbClipboard(cb, id_journal):
            row = [
                [
                    datetime.date.today().strftime("%d/%m/%Y"),
                    time.strftime("%H:%M"),
                    id_journal - 1,
                    cb,
                ],
            ]

            request = (
                sheet.values()
                .append(
                    spreadsheetId=SPREADSHEET_ID,
                    range="clipboard!A1",
                    valueInputOption="USER_ENTERED",
                    insertDataOption="INSERT_ROWS",
                    body={"values": row},
                )
                .execute()
            )

        def pushToDbMedia(media_title, media_artist, id_journal):
            row = [
                [
                    datetime.date.today().strftime("%d/%m/%Y"),
                    time.strftime("%H:%M"),
                    id_journal,
                    media_artist,
                    media_title,
                ]
            ]
            request = (
                sheet.values()
                .append(
                    spreadsheetId=SPREADSHEET_ID,
                    range="media!A1",
                    valueInputOption="USER_ENTERED",
                    insertDataOption="INSERT_ROWS",
                    body={"values": row},
                )
                .execute()
            )

        def getClipboard():
            try:
                clipboard = pyperclip.paste()
            except pyperclip.exceptions.PyperclipException:
                clipboard = ""
            except:
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
        # time_idle = time.time()
        current_window_title = getForegroundWindowTitle()
        current_window_name = getForegroundWindowName()
        # cb_last = ""
        # media_artist_last = ""
        # media_title_last = ""
        # today = datetime.date.today()

        while True:

            if current_window_title == getForegroundWindowTitle():
                time.sleep(1)
                if int(time.time() - time_idle) > 60 * 5 and current_window_title != "":
                    # pyautogui.screenshot(
                    #     screenshot_path
                    #     + str(today)
                    #     + "_"
                    #     + str(int(time.time()))
                    #     + ".png"
                    # )
                    sheet_name = "focus"
                    pushToDbJournal(
                        current_window_name,
                        current_window_title,
                        int(time.time() - time_idle),
                        sheet_name,
                    )
                    time_idle = time.time()
                    # session += 1

            else:
                time_idle = time.time()
                # session = 1
                runtime = int(time.time() - time_seconds)
                print(current_window_name, current_window_title, runtime)
                if runtime > 10:
                    sheet_name = "journal"
                    pushToDbJournal(
                        current_window_name, current_window_title, runtime, sheet_name
                    )

                time_seconds = time.time()
                current_window_title = getForegroundWindowTitle()
                current_window_name = getForegroundWindowName()

            cb = getClipboard()
            if cb != "" and cb_last != cb:
                id_journal = getDbJournalId()
                pushToDbClipboard(cb, id_journal)
                cb_last = cb

            if int(time.time()) % 5 == 0:
                if asyncio.run(getMediaInfo()):
                    media_artist, media_title = asyncio.run(getMediaInfo())
                else:
                    media_artist, media_title = "", ""

                if (
                    media_artist != ""
                    and media_title != ""
                    and media_title != media_title_last
                ):

                    id_journal = getDbJournalId()
                    pushToDbMedia(media_title, media_artist, id_journal)

                    media_title_last = media_title
                    media_artist_last = media_artist
    except Exception as e:
        with open(log_path, "a") as f:
            txt = f'{datetime.date.today()}, {datetime.datetime.now().strftime("%H:%M")} - {current_window_title} : {e} \n'
            f.write(txt)
        time.sleep(10)

        start_script(
            cb_last=cb_last,
            current_window_name=current_window_name,
            current_window_title=current_window_title,
            runtime=runtime,
            media_artist_last=media_artist_last,
            media_title_last=media_title_last,
            time_idle = time_idle,
            # session = session
        )


start_script()
