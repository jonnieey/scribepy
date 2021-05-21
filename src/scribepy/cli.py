import subprocess, sys
import argparse
from time import sleep
import pyfiglet

from asciimatics.exceptions import ResizeScreenError
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from scribepy.player import Player
from scribepy.connector import Connector

from scribepy.tui.browser import BrowserFrame
from scribepy.tui.mainwindow import MainWindowFrame
from scribepy.tui.progressbar import ProgressBar

def get_parser():
    usage = "scribepy [OPTIONS] [COMMAND] [COMMAND_OPTIONS]"
    description = "Command line audio player for transcription"
    parser = argparse.ArgumentParser(prog="scribepy", usage=usage, description=description, add_help=False,)

    main_help = "Show this help message and exit."
    subcommand_help = "Show this help message and exit."

    global_options = parser.add_argument_group(title="Global options")
    global_options.add_argument("-h", "--help", action="help", help=main_help)

    subparsers = parser.add_subparsers(dest="subcommand", metavar="", title="Commands", prog="scribepy")

    def subparser(command, text, **kwargs):
        sub = subparsers.add_parser(command, help=text, description=text, add_help=False, **kwargs)
        sub.add_argument("-h", "--help", action="help", help=subcommand_help)
        return sub

    play_parser = subparser("play", "Play media file from terminal")
    tui_parser = subparser("tui", "Launch interactive text user interface",)

    play_parser.add_argument("file", help="File to play")

    return parser

def play_file(file):
    player = Player()
    connector = Connector()
    connector.set_player(player)
    connector.player_play(file)

    while connector.player.position <= connector.player.length:
        try:
            subprocess.call("clear")
            pyfiglet.print_figlet("SCRIBEPY", 'cyberlarge', justify="center")
            print(file, f"{connector.player.position_time}/{connector.player.length_time}", sep="\t" * 2)
            sleep(1)
        except KeyboardInterrupt as error:
            sys.exit("\nExiting scribepy!!!")

def init(screen, old_scene):
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

    subcommand = kwargs.pop("subcommand")

    try:
        return commands[subcommand](**kwargs)
    except Exception as error:
        #Log error
        print(error)

if __name__ == "__main__":
    main()
