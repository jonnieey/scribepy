import sys
import time
from pathlib import Path
from pybass.pybass import *

class Player:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        if not BASS_Init(-1, 44100, 0, 0, 0):
            print("BASS INITIALIZATION ERROR", get_error_description(BASS_ErrorGetCode()))
            sys.exit(0)

        self.stream = BASS_StreamCreateFile(False, bytes(self.file_path), 0, 0, 0)

    def __del__(self):
        self.destructor()

    def destructor(self):
        BASS_StreamFree(self.stream)
        BASS_Free()

    def play(self):
        BASS_ChannelPlay(self.stream, False)

    def pause(self):
        BASS_ChannelPause(self.stream)

    def stop(self):
        BASS_ChannelStop(self.stream)

    def get_length(self):
        _len = BASS_ChannelGetLength(self.stream, BASS_POS_BYTE)
        slen = BASS_ChannelBytes2Seconds(self.stream, _len)
        return slen

    def get_position(self):
        buf = BASS_ChannelGetPosition(self.stream, BASS_POS_BYTE)
        sbuf = BASS_ChannelBytes2Seconds(self.stream, buf)
        return sbuf

