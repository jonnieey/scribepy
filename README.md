# Scribepy

Command line audio player for transcription.

> Features:
    - Play audio from terminal (CLI or curses interface).
    - Control playback with hotkeys.
    - Supports multiple audio/video types (wma, m4a, mkv, mp4, etc)

## Setup

`git clone https://www.github.com/jonnieey/scribepy`
`pdm run install`

## Run

`pdm run scribepy`

or

`pdm run scribpy play -f [FILENAME]` to play in command line

## Limitations

### Suppressing of key events.
when using hotkeys the keypress are sent to active application/focused
application. Xorg does not allow suppressing of events
[https://github.com/moses-palmer/pynput/issues/47].

