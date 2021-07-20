# Scribepy

Command line audio player for transcription.

Features:

    - Play audio from terminal (CLI or curses interface).

    - Control playback with hotkeys.

    - Increase/Decrease audio tempo.

    - Supports multiple audio/video types (wma, m4a, mkv, mp4, etc)

## Setup

Install libbass in your linux distribution [libbass](https://www.un4seen.com).

install [PDM](https://github.com/pdm-project/pdm).

`git clone https://www.github.com/jonnieey/scribepy`

`pdm install`

## Run

`pdm run scribepy`

or

`pdm run scribpy play -f [FILENAME]` to play in command line

## Usage

### HotKeys
    F2 - Rewind (-10)           F3 - Increase tempo
    F4 - Pause                  F5 - Restore tempo
    F6 - Fast Forward (+10)     F7 - Rewind (-2)
    F8 - Fast Forward (+2)      F9 - Toggle play/pause
    F11 - Decrease Tempo

## Limitations

### Suppressing of key events.
when using hotkeys the keypress are sent to active application/focused
application. Xorg does not allow suppressing of events [issue47](https://github.com/moses-palmer/pynput/issues/47).

Due to this the hotkey button mappings should be removed in respective editor/writer (eg. Libreoffice).

