from utilities import get_active_window_x, get_chrome_url_x, get_active_window_raw
from time import time, sleep
import getpass
import json

TERMINAL_ALIAS = "guille@honor-lap" + ": "
TIMEOUT = 0.1


def get_time_passed(old_time):
    return time() - old_time


def add_or_set_attribute(dictionary_, name, time):
    try:
        dictionary_[name] += time
    except KeyError:
        dictionary_[name] = 0
    return dictionary_


def main():
    window_arr = {}
    window_arr = {"Projects": {}, "Tabs": {}, "Songs": {}}
    timer = time()
    while True:
        current_window = str(get_active_window_x())
        current_window_raw = str(get_active_window_raw())

        is_terminal = False
        is_brave = False
        is_spotify = False
        current_url = ""
        current_song = ""

        if TERMINAL_ALIAS in current_window:
            current_window = current_window.replace(TERMINAL_ALIAS, "")
            is_terminal = True
        elif "Brave" in current_window:
            is_brave = True
            current_url = " ".join(get_chrome_url_x())
        elif " - " in current_window_raw:
            current_window = "Spotify"
            current_song = current_window_raw
            is_spotify = True

        # If it has already been registered
        if is_terminal:
            window_arr = add_or_set_attribute(
                window_arr, "Terminal", get_time_passed(timer))
            window_arr["Projects"] = add_or_set_attribute(
                window_arr["Projects"], current_window, get_time_passed(timer))
        elif is_brave:
            window_arr = add_or_set_attribute(
                window_arr, "Brave", get_time_passed(timer))
            window_arr["Tabs"] = add_or_set_attribute(
                window_arr["Tabs"], current_url, get_time_passed(timer))
        elif is_spotify:
            window_arr = add_or_set_attribute(
                window_arr, "Spotify", get_time_passed(timer))
            window_arr["Songs"] = add_or_set_attribute(
                window_arr["Songs"], current_song, get_time_passed(timer))
        else:
            window_arr = add_or_set_attribute(
                window_arr, current_window, get_time_passed(timer))

        timer = time()

        with open("time_tracked.json", "w") as f:
            json.dump(window_arr, f, indent=2)

        sleep(TIMEOUT)


main()
