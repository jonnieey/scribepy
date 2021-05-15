import sys
import time
from pathlib import Path
from pybass.pybass import *
from pybass.pybass_aac import *
from pybass.pybassflac import *
from pybass.pybass_alac import *
from pybass.pybass_tta import *
from pybass.pybass_mpc import *
from pybass.pybass_ape import *

fx_module = ctypes.CDLL('./libbass_fx.so')
fx_func_type = ctypes.CFUNCTYPE
BASS_ATTRIB_TEMPO = 0x10000
BASS_FX_FREESOURCE = 0x10000
BASS_FX_TempoCreate = func_type(HSTREAM, ctypes.c_ulong, ctypes.c_ulong)(('BASS_FX_TempoCreate', fx_module))

def get_module_to_use(ext):
    #Crude (Replace with magic)
    return {
        ".mp3": BASS_StreamCreateFile,
        ".m4a": BASS_MP4_StreamCreateFile,
        ".mp4": BASS_MP4_StreamCreateFile,
        ".aac": BASS_AAC_StreamCreateFile,
        ".flac": BASS_FLAC_StreamCreateFile,
        ".alac": BASS_ALAC_StreamCreateFile,
        ".tta": BASS_TTA_StreamCreateFile,
        ".mpc": BASS_MPC_StreamCreateFile,
        ".ape": BASS_APE_StreamCreateFile,
    }[ext]

class Player:
    isPlaying = 0
    isPaused = 0

    def __init__(self):

        if not BASS_Init(-1, 44100, 0, 0, 0):
            #log exceptions
            print("BASS INITIALIZATION ERROR", get_error_description(BASS_ErrorGetCode()))
            sys.exit(0)

        self.stream = None
        self.tempo = 0

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

    def create_file_stream(self, f):
        file = Path(f)
        # stream = BASS_StreamCreateFile(False, bytes(file), 0, 0, BASS_STREAM_DECODE)

        file_extension = file.suffix.lower()
        module = get_module_to_use(file_extension)
        stream = module(False, bytes(file), 0, 0, BASS_STREAM_DECODE)

        # stream = BASS_AAC_StreamCreateFile(False, bytes(file), 0, 0, 0)
        self.stream = BASS_FX_TempoCreate(stream, BASS_FX_FREESOURCE)

    def destruct(self):
        if self.isPlaying or self.isPaused:
            self.stop()
            retval = BASS_StreamFree(self.handle)

        self.stream = None

    def play(self, restart=False):
        self.isPlaying = 1
        self.isPaused = 0
        BASS_ChannelPlay(self.stream, restart)

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
    def position_bytes(self):
        buf = BASS_ChannelGetPosition(self.handle, BASS_POS_BYTE)
        return buf

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

    def move_to_position_bytes(self, pos):
        pos = BASS_ChannelSetPosition(self.handle,  pos, BASS_POS_BYTE)
        return pos

    def move_to_position_seconds(self, pos):
        bytes = BASS_ChannelSeconds2Bytes(self.handle, pos)
        pos = BASS_ChannelSetPosition(self.handle,  bytes, BASS_POS_BYTE)
        return pos

    def seek_by_bytes(self, s):
        return self.move_to_position_bytes(self.position_bytes + (s * 124000 ) )

    def seek(self, s):
        return self.move_to_position_seconds(self.position + s )

    def change_tempo(self, speed):
        self.tempo += speed
        BASS_ChannelSetAttribute(self.stream, BASS_ATTRIB_TEMPO, self.tempo)

    def restore_tempo(self):
        self.tempo = 0
        BASS_ChannelSetAttribute(self.stream, BASS_ATTRIB_TEMPO, self.tempo)
