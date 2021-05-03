import os
import time
import datetime
import numpy as np
import pandas as pd
import win32process
import wmi
from win32gui import GetWindowText, GetForegroundWindow

from config import delay, data_file

c = wmi.WMI()

def get_app_name(hwnd):
    """Get applicatin filename given hwnd."""
    exe = ""
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
            exe = p.Name
            break
    except:
        return None
    else:
        return exe


def write_to_csv(app_name, date_time, window_name):
    data = pd.DataFrame({"app_name": [app_name],
                         "date_time": [date_time],
                         "window_name": [window_name]})

    print(data)

    if not os.path.isfile(data_file):
        # creating new file
        data.to_csv(data_file, index=False)
    else:
        # append exsisting file
        data.to_csv(data_file, mode='a', header=False, index=False)
    pass


def main():
    print("====== time tracking started ======")

    last_app_name = None

    while True:
        curr_window_id = GetForegroundWindow()
        app_name = get_app_name(curr_window_id)

        if app_name != last_app_name:

            last_app_name = app_name
            window_name = GetWindowText(curr_window_id)
            date_time = datetime.datetime.now()

            if(app_name == "explorer.exe" and window_name == ""):
                # no window
                app_name = "None"

            write_to_csv(app_name, date_time, window_name)

        time.sleep(delay)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("====== time tracking stopped ======")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
        pass
