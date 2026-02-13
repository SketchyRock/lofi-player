try:
    import curses
except ImportError:
    print("curses lib is required as a dependency")
    import sys

    sys.exit(1)


def refresh_screen(stdscr, player, usr_input=None):
    SCREEN_HANDLERS = {
        ord(" "): lambda: (
            stdscr.move(8, 0),
            stdscr.clrtoeol(),
            stdscr.addstr(8, 2, "paused: " + ("⏸️" if player.paused else "▶️")),
        ),
        ord("n"): lambda: (
            stdscr.move(6, 0),
            stdscr.clrtoeol(),
            stdscr.addstr(6, 2, "song: " + player.mp3_files[player.idx]),
        ),
        ord("b"): lambda: (
            stdscr.move(6, 0),
            stdscr.clrtoeol(),
            stdscr.addstr(6, 2, "song: " + player.mp3_files[player.idx]),
        ),
        ord("="): lambda: (
            stdscr.move(7, 0),
            stdscr.clrtoeol(),
            stdscr.addstr(7, 2, "volume: " + str(player.volume)),
            stdscr.addstr(7, 9, " MUTE" if player.volume == 0 else ""),
        ),
        ord("-"): lambda: (
            stdscr.move(7, 0),
            stdscr.clrtoeol(),
            stdscr.addstr(7, 2, "volume: " + str(player.volume)),
            stdscr.addstr(7, 9, " MUTE" if player.volume == 0 else ""),
        ),
    }

    handler = SCREEN_HANDLERS.get(usr_input)
    if handler:
        handler()


def screen_init(stdscr, player):
    """Refresh the screen for the music player.

    Clears the screen and prints the information about the currently playing song and the controls for the music player.
    """
    stdscr.clear()
    try:
        curses.curs_set(0)
    except curses.error:
        pass

    stdscr.attron(curses.A_BOLD)
    stdscr.addstr(0, 0, "Lo-Fi Player")
    stdscr.attroff(curses.A_BOLD)

    stdscr.addstr(2, 2, "q: Quit")
    stdscr.addstr(3, 2, "n: Next")
    stdscr.addstr(4, 2, "b: Prev")

    stdscr.addstr(2, 12, "=: +volume")
    stdscr.addstr(3, 12, "-: -volume")
    stdscr.addstr(4, 12, "' ': Pause")

    stdscr.addstr(2, 24, "s: Settings")
    stdscr.addstr(3, 24, "c: Dancing Cat!")

    stdscr.addstr(6, 2, "song: " + player.mp3_files[player.idx])
    stdscr.addstr(7, 2, "volume: " + str(player.volume))
    stdscr.addstr(7, 9, " MUTE" if player.volume == 0 else "")
    stdscr.addstr(8, 2, "paused: " + ("⏸️" if player.paused else "▶️"))

    stdscr.refresh()
