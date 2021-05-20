import sys

from asciimatics.exceptions import ResizeScreenError
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from scribepy.tui.browser import BrowserFrame
from scribepy.tui.mainwindow import MainWindowFrame
from scribepy.tui.progressbar import ProgressBar
from scribepy.connector import Connector

from scribepy.player import Player

player = Player()
connector = Connector()
connector.set_player(player)

def init(screen, old_scene):
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

last_scene = None
while True:
    try:
        Screen.wrapper(init, catch_interrupt=False, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
