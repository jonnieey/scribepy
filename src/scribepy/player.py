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
    """
    Get module to use according to file extension.

    Arguments:
        ext: Extension of the file.

    Returns:
        BASS module to use to create stream
    """
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
    """
    A class to interact with pybass module.
    """

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
        """
        Return a file stream if exists or create one if it doesn't already exist.

        Returns:
            BASS channel stream.
        """
        if self.stream is None:
            self.create_file_stream("")
        return self.stream

    @handle.deleter
    def handle(self):
        self.destruct()

    def create_file_stream(self, file):
        """
        Create sample stream from file and add Tempo effect to it.

        Arguments:
            file: File to create stream from.
            ( MP3, MP2, MP1, OGG, WAV, AIFF or plugin supported file).

        Returns:
            None.
        """
        f = Path(file)
        # stream = BASS_StreamCreateFile(False, bytes(file), 0, 0, BASS_STREAM_DECODE)

        file_extension = f.suffix.lower()
        module = get_module_to_use(file_extension)
        stream = module(False, bytes(f), 0, 0, BASS_STREAM_DECODE)

        # stream = BASS_AAC_StreamCreateFile(False, bytes(file), 0, 0, 0)
        self.stream = BASS_FX_TempoCreate(stream, BASS_FX_FREESOURCE)

    def destruct(self):
        """
        Stop stream if playing or paused and free the sample stream's resources.

        Returns:
            None.
        """
        if self.isPlaying or self.isPaused:
            self.stop()
            retval = BASS_StreamFree(self.handle)

        self.stream = None

    def play(self, restart=False):
        """
        Start (or resume) playback of a sample.

        Arguments:
            restart: Whether to restart playback from beginning.

        Returns:
            None
        """
        self.isPlaying = 1
        self.isPaused = 0
        BASS_ChannelPlay(self.stream, restart)

    def pause(self):
        """
        Pause the stream.

        Returns:
            None.
        """
        self.isPaused = 1
        self.isPlaying = 1
        BASS_ChannelPause(self.handle)

    def stop(self):
        """
        Stop the stream.

        Returns:
            None.
        """
        self.isPlaying = 0
        self.isPaused = 0
        BASS_ChannelStop(self.handle)

    @property
    def length(self):
        """
        Get length of stream in Seconds.

        Returns:
            Length of stream.
        """
        _len = BASS_ChannelGetLength(self.handle, BASS_POS_BYTE)
        slen = BASS_ChannelBytes2Seconds(self.handle, _len)
        return slen

    @property
    def length_time(self):
        """
        Get length of stream in human readable format (MM:SS) .

        Returns:
            Length of stream.
        """
        seconds = int(self.length % 60)
        minutes = int(self.length // 60)

        return f"{minutes:02}:{seconds:02}"

    @property
    def position(self):
        """
        Get the position of the stream in seconds.

        Returns:
            Position of stream.
        """
        buf = BASS_ChannelGetPosition(self.handle, BASS_POS_BYTE)
        sbuf = BASS_ChannelBytes2Seconds(self.handle, buf)
        return sbuf

    @property
    def position_time(self):
        """
        Get the position of the stream in human readable format (MM:SS)

        Returns:
            Position of stream.
        """
        seconds = int(self.position % 60)
        minutes = int(self.position // 60)

        return f"{minutes:02}:{seconds:02}"

    @property
    def position_bytes(self):
        """
        Get the position of the stream in bytes.

        Returns:
            Position of stream in bytes.
        """
        buf = BASS_ChannelGetPosition(self.handle, BASS_POS_BYTE)
        return buf

    @property
    def remaining(self):
        """
        Get remaining time.

        Return:
            Remaining time in seconds
        """
        return self.length - self.position

    @property
    def remaining_time(self):
        """
        Get remaining time in human readable format.

        Return:
            Remaining time in human readable format (MM:SS)
        """
        seconds = int(self.remaining % 60)
        minutes = int(self.remaining // 60)

        return f"{minutes:02}:{seconds:02}"

    @property
    def pause_play_toggle(self):
        """
        Toggle play/pause

        Returns:
            None.
        """
        status = BASS_ChannelIsActive(self.handle)
        if status == BASS_ACTIVE_PAUSED:
            self.play()
        else:
            self.pause()

    def move_to_position_bytes(self, pos):
        """
        Set the playback position.

        Arguments:
            pos: Position to set to (using bytes as units).

        Returns:
            None
        """
        pos = BASS_ChannelSetPosition(self.handle,  pos, BASS_POS_BYTE)

    def move_to_position_seconds(self, pos):
        """
        Set the playback position.

        Arguments:
            pos: Position to set to (using seconds as units).

        Returns:
            None
        """

        bytes = BASS_ChannelSeconds2Bytes(self.handle, pos)
        pos = BASS_ChannelSetPosition(self.handle,  bytes, BASS_POS_BYTE)

    def seek_by_bytes(self, s):
        """
        Seek playback from current position.

        Arguments:
            s: Bytes to seek.

        returns:
            None.

        """
        self.move_to_position_bytes(self.position_bytes + (s * 124000 ) )

    def seek(self, s):
        """
        Seek playback from current position.

        Arguments:
            s: Seconds to seek.

        returns:
            None.

        """
        return self.move_to_position_seconds(self.position + s )

    def change_tempo(self, s):
        """
        Change tempo of stream.

        Arguments:
            s: Add tempo by

        Returns:
            None.
        """
        self.tempo += s
        BASS_ChannelSetAttribute(self.stream, BASS_ATTRIB_TEMPO, self.tempo)

    def restore_tempo(self):
        """
        Restore tempo of stream.

        Returns:
            None.
        """
        self.tempo = 0
        BASS_ChannelSetAttribute(self.stream, BASS_ATTRIB_TEMPO, self.tempo)
