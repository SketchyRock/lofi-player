# lofi-player
> A simple Python-based MP3 player designed for focused lofi sessions.

This project is a lightweight music player that automatically loads and plays audio files from a local directory, providing a distraction-free listening experience.

---

## Features:

* **Auto-Loading**: Scans the music/ folder automatically for MP3 files.

* **Minimalist**: A lightweight terminal-based player.

* **Local Playback**: No internet required; plays your personal MP3 collection.

---

## Setup & Installation

### 1. Prerequisites

* Python 3.13+
* `curses`
* `pygame`

### 2. Installation
```bash
python3 -m pip install -r requirements.txt
```

### 2. Music Configuration

For the program to find your music, you must point to the directory where mp3's are stored once the program is launched in order for them to be played.

---

## How to Run

Navigate to the project folder and run the script:
```bash
python3 lofi.py
```

---

## License

This project is open-source and available under the MIT License.

---

# TODO:
* add user friendly instructions for using the application
* add playlist functionality with sub dirs
* create better documentation for the new modules created
