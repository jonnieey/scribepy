from asciimatics.exceptions import ResizeScreenError
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from gui.browser import BrowserFrame
from gui.mainwindow import MainWindowFrame
from gui.progressbar import ProgressBar

from player import Player
import sys

player = Player()

def demo(screen, old_scene):
    mainwindow = MainWindowFrame(screen)
    browser = BrowserFrame(screen)
    browser.setPlayer(player)
    progressbar = ProgressBar(screen)
    progressbar.setPlayer(player)

    scenes = []
    scenes.append(Scene([mainwindow], -1, name="Main Window"))
    scenes.append(Scene([browser], -1, name="Scribepy File Browser"))
    scenes.append(Scene([progressbar], -1, name="Progress Bar"))
    screen.play(scenes, start_scene = old_scene)

last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene


