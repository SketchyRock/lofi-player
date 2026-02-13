"""Settings module for mp3 player.

Author: SketchyRock
Date: 2/12/2026
"""

import json
import os
from time import sleep

try:
    import curses
except ImportError:
    print("curses lib is required as a dependency")
    # By exiting here, we are assuming this module won't be imported if curses is not available.
    # This is a reasonable assumption for this application structure.
    import sys

    sys.exit(1)


def create_settings(stdscr, settings_list=None):
    curses.echo()
    SETTINGS = {
        "music_path": {
            "variable name": "music_path",
            "description": "Enter the path to the music folder: ",
            "error message": "path to the music folder does not exist",
            "lambda": (lambda x: os.path.exists(x)),
        }
    }

    try:
        with open("lofi.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    for key, setting in SETTINGS.items():
        if settings_list is not None and key not in settings_list:
            continue

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, setting["description"])
            stdscr.refresh()

            settings_input = stdscr.getstr(1, 0, 100).decode("utf-8").strip()

            if setting["lambda"](settings_input):
                data[setting["variable name"]] = settings_input
                break

            stdscr.addstr(2, 0, setting["error message"])
            stdscr.refresh()
            sleep(1)

    curses.noecho()

    with open("lofi.json", "w") as f:
        json.dump(data, f)


def load_settings() -> dict:
    try:
        with open("lofi.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def choose_setting(stdscr):
    SETTINGS = list(load_settings().keys())

    stdscr.clear()
    stdscr.addstr(0, 0, "Choose a setting to change:\n")

    for i, key in enumerate(SETTINGS):
        stdscr.addstr(i + 2, 2, f"{i + 1}: {key}")

    stdscr.addstr(curses.LINES - 1, 0, "Press number or q to cancel")
    stdscr.refresh()

    while True:
        key = stdscr.getch()

        if key == ord("q"):
            return

        if ord("1") <= key <= ord(str(len(SETTINGS))):
            idx = key - ord("1")
            selected = SETTINGS[idx]
            create_settings(stdscr, settings_list=[selected])
            return


def display_settings(stdscr):
    SETTINGS_HANDLERS = {
        ord("c"): lambda: choose_setting(stdscr),
        ord("q"): lambda: None,
    }
    data = load_settings()
    stdscr.clear()
    stdscr.addstr(0, 0, "Settings:")
    for i, (key, value) in enumerate(data.items()):
        stdscr.addstr(i + 2, 2, f"{i + 1}: {key} - {value}")
    stdscr.addstr(curses.LINES - 1, 0, "change settings (c) or quit (q)")
    stdscr.refresh()

    while True:
        usr_input = stdscr.getch()

        if usr_input in SETTINGS_HANDLERS:
            SETTINGS_HANDLERS[usr_input]()
            break


def save_settings_to_player(player):
    data = load_settings()
    for key, value in data.items():
        setattr(player, key, value)
