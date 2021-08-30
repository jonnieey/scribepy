from scribepy.player import Player
from pathlib import Path
try:
    import pyfiglet
except ImportError:
    pass
import shutil
from time import sleep
from scribepy.connector import Connector
import subprocess, sys
from loguru import logger

def progressBar(
    player,
    prefix="Progress: ",
    suffix="Complete",
    decimals=0,
    length=100,
    fill="█",
    printEnd="\r",
    autosize=False,
):

    """
    Command line interface progress bar.

    Arguments:
        player: Instance of Player.
        prefix: Prefix to add to the progress bar.
        suffix: Suffix to add to the progress bar.
        decimals: Decimal places used on progress bar time.
        length: Length of bar
        fill: Character to fill the bar.
        printEnd: end character (eg '\r\n', '\n')

    Returns:
        None
    """

    position = player.position
    total = player.length
    # Progress Bar Printing Function
    def printProgressBar(position, length=length):
        percent = ("{0:." + str(decimals) + "f}").format(
            100 * (position / total)
        )
        styling = f"{prefix} |{fill}| {percent}% {suffix}"

        if autosize:
            cols, _ = shutil.get_terminal_size(fallback=(length, 1))
            length = cols - len(styling)

        filledLength = int(length * position // total)
        bar = fill * filledLength + "-" * (length - filledLength)
        # print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        print(f"\r{styling.replace(fill, bar)}", end="\r")
        print()
        timer = f"{player.position_time}/{player.length_time}"
        timer_pos = len(timer) + len(bar)
        print(f"{timer:>{timer_pos}}")

    # Update Progress Bar
    if position <= total:
        printProgressBar(position)
    # Print New Line on Complete
    print()

def play_file(file):
    """
    Play file from the command line.

    Arguments:
        file: File to play.

    Returns:
        None
    """

    KEYBINDS = """
    F2 - Rewind (-10)           F3 - Increase tempo
    F4 - Pause                  F5 - Restore tempo
    F6 - Fast Forward (+10)     F7 - Rewind (-2)
    F8 - Fast Forward (+2)      F9 - Toggle play/pause
    F11 - Decrease Tempo
    """

    player = Player()
    connector = Connector()
    connector.set_player(player)
    connector.player_play(file)

    while True:
        try:
            subprocess.call("clear")
            try:
                pyfiglet.print_figlet(
                    "SCRIBEPY", "cyberlarge", justify="center"
                )
            except Exception as error:
                logger.exception(error)
                print("                                         SCRIBEPY")
            print("Playing: ")
            print()
            print(Path(file).absolute())
            print()
            progressBar(connector.player, autosize=True)
            print(KEYBINDS)
            print("\nPress Ctrl-c to exit")
            sleep(0.1)
        except KeyboardInterrupt as error:
            sys.exit("\nExiting scribepy!!!")

