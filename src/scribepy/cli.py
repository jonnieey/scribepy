import subprocess, sys
import argparse
from pathlib import Path
from time import sleep
import shutil

import pyfiglet
from loguru import logger
from pynput import keyboard

from asciimatics.exceptions import ResizeScreenError
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from scribepy.player import Player
from scribepy.connector import Connector

from scribepy.tui.browser import BrowserFrame
from scribepy.tui.mainwindow import MainWindowFrame
from scribepy.tui.progressbar import ProgressBar

from scribepy import custom_logger

def get_parser():
    """
    Create custom parser

    Returns: parser -> ArgumentParser
    """
    usage = "scribepy [OPTIONS] [COMMAND] [COMMAND_OPTIONS]"
    description = "Command line audio player for transcription"
    parser = argparse.ArgumentParser(prog="scribepy", usage=usage, description=description, add_help=False,)

    main_help = "Show this help message and exit."
    subcommand_help = "Show this help message and exit."

    global_options = parser.add_argument_group(title="Global options")
    global_options.add_argument("-h", "--help", action="help", help=main_help)
    global_options.add_argument("-L", "--log-level", type=str.upper, help="Log level to use", choices=("TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"), )

    global_options.add_argument("-P", "--log-path", metavar="", help="Log file to use",)
    subparsers = parser.add_subparsers(dest="subcommand", metavar="", title="Commands", prog="scribepy")

    def subparser(command, text, **kwargs):
        sub = subparsers.add_parser(command, help=text, description=text, add_help=False, **kwargs)
        sub.add_argument("-h", "--help", action="help", help=subcommand_help)
        return sub

    play_parser = subparser("play", "Play media file from terminal")
    tui_parser = subparser("tui", "Launch interactive text user interface",)

    play_parser.add_argument("file", help="File to play")

    return parser

def progressBar(player, prefix = 'Progress: ', suffix = 'Complete', decimals = 0, length = 100, fill = '█', printEnd = "\r", autosize=False):
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
    def printProgressBar (position, length=length):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (position / total))
        styling = f"{prefix} |{fill}| {percent}% {suffix}"

        if autosize:
            cols, _ = shutil.get_terminal_size(fallback=(length, 1))
            length = cols - len(styling)

        filledLength = int(length * position // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        # print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        print(f"\r{styling.replace(fill, bar)}", end ='\r')
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
    F2 - Rewind (-10)           F3 - Play fast speed
    F4 - Pause                  F5 - Restore tempo
    F6 - Fast Forward (+10)     F7 - Rewind (-2)
    F8 - Fast Forward (+2)      F9 - Toggle play/pause
    F11 - Decrease Tempo
    """

    player = Player()
    connector = Connector()
    connector.set_player(player)
    connector.player_play(file)

    while connector.player.position <= connector.player.length:
        try:
            subprocess.call("clear")
            try:
                pyfiglet.print_figlet("SCRIBEPY", 'cyberlarge', justify="center")
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

def init(screen, old_scene):
    """
    Initialize scenes to play

    Arguments:
        screen: Screen instance.
        old_scene: Initial scene.

    Return:
        None
    """
    player = Player()
    connector = Connector()
    connector.set_player(player)
    mainwindow = MainWindowFrame(screen)

    browser = BrowserFrame(screen)
    browser.set_connector(connector)
    connector.set_browser(browser)

    progressbar = ProgressBar(screen)
    progressbar.set_connector(connector)

    scenes = []
    scenes.append(Scene([mainwindow], -1, name="Main Window"))
    scenes.append(Scene([browser], -1, name="Scribepy File Browser"))
    scenes.append(Scene([progressbar], -1, clear=False, name="Progress Bar"))
    screen.play(scenes, start_scene = old_scene)

def launch_tui(**kwargs):
    last_scene = None
    while True:
        try:
            Screen.wrapper(init, catch_interrupt=False, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene

def main(args=None):
    commands = {
        None: launch_tui,
        "tui": launch_tui,
        "play": play_file,
    }

    parser = get_parser()
    opts = parser.parse_args(args=args)
    kwargs = opts.__dict__

    log_level = kwargs.pop("log_level")
    log_path = kwargs.pop("log_path")

    if log_path:
        log_path = Path(log_path)
        if log_path.is_dir():
            log_path = log_path / "scribepy-{time}.log"
        custom_logger(sink=log_path, level=log_level or "WARNING")
    elif log_level:
        custom_logger(sink=sys.stderr, level="WARNING")

    subcommand = kwargs.pop("subcommand")

    try:
        return commands[subcommand](**kwargs)
    except Exception as error:
        logger.exception(error)
        print(error)
        sys.exit(0)

if __name__ == "__main__":
    main()
