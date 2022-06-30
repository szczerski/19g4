import psutil, win32process, win32gui
import time


def getForegroundWindowName():
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    return psutil.Process(pid[-1]).name().lower().split(".")[0]


def getForegroundWindowTitle():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())


time_seconds = time.time()
current_window_title = getForegroundWindowTitle()
current_window_name = getForegroundWindowName()


while True:

    if current_window_title == getForegroundWindowTitle():
        time.sleep(1)
    else:
        runtime = int(time.time() - time_seconds)
        print(current_window_name, current_window_title, runtime)

        time_seconds = time.time()
        current_window_title = getForegroundWindowTitle()
        current_window_name = getForegroundWindowName()
