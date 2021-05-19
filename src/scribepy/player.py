import sys
import time
from pathlib import Path

from magic import from_file

from scribepy.pybass.pybass import *
from scribepy.pybass.pybass_aac import BASS_AAC_StreamCreateFile, BASS_MP4_StreamCreateFile
from scribepy.pybass.pybassflac import BASS_FLAC_StreamCreateFile
from scribepy.pybass.pybass_tta import BASS_TTA_StreamCreateFile
from scribepy.pybass.pybass_alac import BASS_ALAC_StreamCreateFile
from scribepy.pybass.pybass_ac3 import BASS_AC3_StreamCreateFile

player_module = Path(__file__).parent
fx_module = ctypes.CDLL(f"{player_module}/BASS_modules/libbass_fx.so")
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
    return {
        "audio/x-hx-aac-adts": BASS_AAC_StreamCreateFile,
        "audio/flac": BASS_FLAC_StreamCreateFile,
        "audio/x-m4a": BASS_ALAC_StreamCreateFile,
        "audio/x-wav": BASS_StreamCreateFile,
        "audio/ogg": BASS_StreamCreateFile,
        "audio/mpegapplication/octet-stream": BASS_StreamCreateFile,
        "video/mp4": BASS_MP4_StreamCreateFile,
        "application/octet-stream": BASS_TTA_StreamCreateFile,
        "audio/vnd.dolby.dd-raw": BASS_AC3_StreamCreateFile,
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
            None if successful or error dictionary if unsuccessful.
        """
        f = Path(file)
        # stream = BASS_StreamCreateFile(False, bytes(file), 0, 0, BASS_STREAM_DECODE)

        file_extension = from_file(str(f), mime=True)
        try:
            module = get_module_to_use(file_extension)
            stream = module(False, bytes(f), 0, 0, BASS_STREAM_DECODE or BASS_UNICODE)
            # stream = BASS_AAC_StreamCreateFile(False, bytes(file), 0, 0, 0)
            self.stream = BASS_FX_TempoCreate(stream, BASS_FX_FREESOURCE)
        except KeyError as error:
            # Log error.
            # Show popup screen to show error.
            self.destruct()
            return {"error": f"{f.suffix} files are not supported"}

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
            True if successful else False.
        """
        self.isPlaying = 1
        self.isPaused = 0
        return BASS_ChannelPlay(self.stream, restart)

    def pause(self):
        """
        Pause the stream.

        Returns:
            True if successful else False.
        """
        self.isPaused = 1
        self.isPlaying = 1
        return BASS_ChannelPause(self.handle)

    def stop(self):
        """
        Stop the stream.

        Returns:
            True if successful else False.
        """
        self.isPlaying = 0
        self.isPaused = 0
        return BASS_ChannelStop(self.handle)

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
        return BASS_ChannelGetPosition(self.handle, BASS_POS_BYTE)

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
            True if successful else False.
        """
        return BASS_ChannelSetPosition(self.handle,  pos, BASS_POS_BYTE)

    def move_to_position_seconds(self, pos):
        """
        Set the playback position.

        Arguments:
            pos: Position to set to (using seconds as units).

        Returns:
            True if successful else False.
        """

        bytes = BASS_ChannelSeconds2Bytes(self.handle, pos)
        return BASS_ChannelSetPosition(self.handle,  bytes, BASS_POS_BYTE)

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
        self.move_to_position_seconds(self.position + s )

    def change_tempo(self, s):
        """
        Change tempo of stream.

        Arguments:
            s: Add tempo by

        Returns:
            True if successful else False.
        """
        self.tempo += s
        return BASS_ChannelSetAttribute(self.stream, BASS_ATTRIB_TEMPO, self.tempo)

    def restore_tempo(self):
        """
        Restore tempo of stream.

        Returns:
            True if successful else False.
        """
        self.tempo = 0
        return BASS_ChannelSetAttribute(self.stream, BASS_ATTRIB_TEMPO, self.tempo)

    @property
    def volume(self):
        """
        Master Output Volume.

        Returns:
            Master current volume level.
        """
        return BASS_GetVolume()

    def set_volume(self, volume):
        """
        Set Output Master Volume.

        Arguments:
            volume: The volume level to set to.

        Returns:
            True if successful else False.
        """
        return BASS_SetVolume(volume)
