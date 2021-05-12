import sys
import time
from pathlib import Path
from pybass.pybass import *

class Player:
    isPlaying = 0
    isPaused = 0

    def __init__(self):

        if not BASS_Init(-1, 44100, 0, 0, 0):
            #log exceptions
            print("BASS INITIALIZATION ERROR", get_error_description(BASS_ErrorGetCode()))
            sys.exit(0)

        self.stream = None

    def __del__(self):
        self.destruct()

    @property
    def handle(self):
        if self.stream is None:
            self.create_file_stream("")
        return self.stream

    @handle.deleter
    def handle(self):
        self.destruct()

    def create_file_stream(self, file):
        self.file_path = Path(file)
        self.stream = BASS_StreamCreateFile(False, bytes(self.file_path), 0, 0, 0)

    def destruct(self):
        if self.isPlaying or self.isPaused:
            self.stop()
            retval = BASS_StreamFree(self.handle)

        self.stream = None

    def play(self, restart=False):
        self.isPlaying = 1
        self.isPaused = 0
        BASS_ChannelPlay(self.handle, restart)

    def pause(self):
        self.isPaused = 1
        self.isPlaying = 1
        BASS_ChannelPause(self.handle)

    def stop(self):
        self.isPlaying = 0
        self.isPaused = 0
        BASS_ChannelStop(self.handle)

    @property
    def length(self):
        _len = BASS_ChannelGetLength(self.handle, BASS_POS_BYTE)
        slen = BASS_ChannelBytes2Seconds(self.handle, _len)
        return slen

    @property
    def position(self):
        buf = BASS_ChannelGetPosition(self.handle, BASS_POS_BYTE)
        sbuf = BASS_ChannelBytes2Seconds(self.handle, buf)
        return sbuf

    @property
    def remaining(self):
        return self.length - self.position

    @property
    def position_time(self):
        seconds = int(self.position % 60)
        minutes = int(self.position // 60)

        return f"{minutes:02}:{seconds:02}"

    def length_time(self):
        seconds = int(self.length % 60)
        minutes = int(self.length // 60)

        return f"{minutes:02}:{seconds:02}"

    @property
    def remaining_time(self):
        seconds = int(self.remaining % 60)
        minutes = int(self.remaining // 60)

        return f"{minutes:02}:{seconds:02}"

    @property
    def pause_play_toggle(self):
        status = BASS_ChannelIsActive(self.handle)
        if status == BASS_ACTIVE_PAUSED:
            return self.play()
        else:
            return self.pause()

    def move_to_position_seconds(self, pos):
        bytes = BASS_ChannelSeconds2Bytes(self.handle, pos)
        pos = BASS_ChannelSetPosition(self.handle,  bytes, BASS_POS_BYTE)
        return pos
