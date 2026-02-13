"""mp3 player designed for playing lo-fi music in the background while studying.

Author: SketchyRock
Date: 1/4/2026
"""

import os
import sys
from time import sleep

try:
    import curses
except ImportError:
    print("curses lib is required as a dependency")
    sys.exit(1)

try:
    import pygame
except ImportError:
    print("pygame lib is required as a dependency")
    sys.exit(1)

from settings import create_settings, display_settings, save_settings_to_player
from ui import refresh_screen, screen_init


class Player:
    """A class representing an MP3 player.

    Attributes:
        music_path (str): path to the music folder
        playing (bool): whether music is currently playing
        paused (bool): whether music is currently paused
        volume (float): volume of the music (0.0 to 1.0)
        idx (int): index of the current song in the music folder
        mp3_files (list): list of MP3 files in the music folder
        lock (threading.Lock): lock for thread-safe access to player attributes

    Methods:
        __init__(music_path=None, playing=False, paused=False, volume=2, idx=0, mp3_files=None): constructor for the Player class
        _play_song(): private method to play a song from the music folder
        play_song(): starts playing a song from the music folder
        toggle_pause(): toggles the pause state of the currently playing song
        next_song(): unloads the currently playing song and loads the next one
        prev_song(): unloads the currently playing song and loads the previous one
        increase_volume(): increases the volume of the music
        decrease_volume(): decreases the volume of the music
        quit(): stops playing the music and quits the player
        print_info(song, volume, paused): prints information about the music player
    """

    def __init__(
        self,
        music_path: str = None,
        paused: bool = False,
        volume: int = 1,
        idx: int = 0,
        mp3_files: list[str] = None,
    ):
        """Constructor for Player class.

        Initializes the player with the specified attributes.

        Parameters:
            music_path (str): path to the music folder
            playing (bool): whether music is currently playing
            paused (bool): whether music is currently paused
            volume (float): volume of the music (0.0 to 1.0)
            idx (int): index of the current song in the music folder
            mp3_files (list): list of MP3 files in the music folder
        """
        self.music_path = music_path
        self.paused = paused
        self.volume = volume
        self.idx = idx
        self.mp3_files = mp3_files

    def play_song(self):
        """Private method to play a song from the music folder.

        Prints the path of the music folder and the path of the song being played.
        Sets the `playing` attribute to True and updates the [song] attribute.
        Loads the song from the music folder and plays it using `pygame.mixer.music`.
        """
        self.update_mp3_files()
        pygame.mixer.music.load(os.path.join(self.music_path, self.mp3_files[self.idx]))
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(self.volume / 10)

    def toggle_pause(self):
        """Toggle pause for the currently playing song.

        If the song is currently playing, pause the song.
        If the song is currently paused, unpause the song.
        """
        if self.paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.paused = not self.paused

    def next_song(self):
        """Unload the currently playing song and load the next one.

        If the current song is the last one in the music folder, go back to the first song.
        Otherwise, increment the index and load the next song.
        """
        self.idx = (self.idx + 1) % len(self.mp3_files)
        self.play_song()

    def prev_song(self):
        """Unload the currently playing song and load the previous one.

        If the current song is the first one in the music folder, go to the last song.
        Otherwise, decrement the index and load the previous song.
        """
        self.idx = (self.idx - 1) % len(self.mp3_files)
        self.play_song()

    def increase_volume(self):
        """Increase the volume of the music.

        If the volume is less than 10, increase the volume by 1 and set it for pygame.mixer.music.
        """
        if self.volume < 10:
            self.volume += 1
            pygame.mixer.music.set_volume(self.volume / 10)

    def decrease_volume(self):
        """Decrease the volume of the music.

        If the volume is greater than 0, decrease the volume by 1 and set it for pygame.mixer.music.
        """
        if self.volume > 0:
            self.volume -= 1
            pygame.mixer.music.set_volume(self.volume / 10)

    def update_mp3_files(self):
        """Update the list of MP3 files in the music folder.

        Scans the music folder for MP3 files and updates the self.mp3_files attribute.
        If no MP3 files are found, print a message and exit the program.
        """
        self.mp3_files = [
            file for file in os.listdir(self.music_path) if file.endswith(".mp3")
        ]
        self.mp3_files.sort()
        if not self.mp3_files:
            print("No MP3 files found in the music folder")
            sleep(2)
            sys.exit(1)

    def quit(self):
        """Quit the music player.

        Stops the music player and exits the program.
        """
        pygame.quit()
        sys.exit(0)


def input_handler_loop(stdscr, player):
    LOOP_HANDLERS = {
        ord("q"): lambda: player.quit(),
        ord(" "): lambda: player.toggle_pause(),
        ord("n"): lambda: player.next_song(),
        ord("b"): lambda: player.prev_song(),
        ord("="): lambda: player.increase_volume(),
        ord("-"): lambda: player.decrease_volume(),
        ord("s"): lambda: (
            display_settings(stdscr),
            save_settings_to_player(player),
            screen_init(stdscr, player),
        ),
    }

    while True:
        usr_input = stdscr.getch()

        if usr_input in LOOP_HANDLERS:
            LOOP_HANDLERS[usr_input]()
            refresh_screen(stdscr, player, usr_input)
            stdscr.refresh()

        if not player.paused and pygame.mixer.music.get_pos() == -1:
            player.next_song()

        sleep(1 / 24)


def main(stdscr):
    """Main function for the program.

    Initializes pygame and creates a Player object with the music folder path.
    Updates the list of MP3 files in the music folder and plays the first song.
    Enters an infinite loop to handle events and update the display.
    """
    pygame.init()
    pygame.mixer.init()

    if not os.path.exists("lofi.json"):
        create_settings(stdscr)

    player = Player()
    save_settings_to_player(player)
    player.update_mp3_files()
    player.play_song()
    screen_init(stdscr, player)

    input_handler_loop(stdscr, player)


if __name__ == "__main__":
    curses.wrapper(main)
