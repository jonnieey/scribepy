from asciimatics.exceptions import ResizeScreenError
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from gui.mainwindow import MainWindow
from player import Player
import sys

player = Player("")

def demo(screen, old_scene):
    mainwindow = MainWindow(screen)

    scenes = []
    scenes.append(Scene([mainwindow], -1, name="Main Window"))
    screen.play(scenes, start_scene = old_scene)

last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene


