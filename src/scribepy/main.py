from asciimatics.exceptions import ResizeScreenError
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from tui.browser import BrowserFrame
from tui.mainwindow import MainWindowFrame
from tui.progressbar import ProgressBar
from connector import Connector

from player import Player
import sys

player = Player()
connector = Connector()
connector.setPlayer(player)

def init(screen, old_scene):
    mainwindow = MainWindowFrame(screen)
    browser = BrowserFrame(screen)
    browser.setPlayer(player)
    browser.setConnector(connector)
    progressbar = ProgressBar(screen)
    progressbar.setPlayer(player)
    connector.setBrowser(browser)
    connector.run()

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
